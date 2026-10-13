# Part 2 · The skeleton — process, configuration, sessions

**Level:** ⭐⭐⭐ · **Time:** ~5 h · **Requires:** part 1
**Produces:** a working gateway, configuration as data, an event log with replay

---

## 0. Why a gateway at all

Your loop from course 1 is a script. You run it, talk to it, close it — the state disappears.
Three agents working for weeks require something different: **a process that lives
longer than a conversation**.

The gateway gives you four things that a script cannot:

| What it gives | Why you cannot do without it |
| :-- | :-- |
| **One place for state** | Two processes writing to the same memory is a race. One process = no race |
| **One place for policy** | Access control scattered across the tools **always** has a hole. Centralised — there is nowhere to forget it |
| **One place for observation** | A trace scattered across scripts is useless (part 15) |
| **A hook for the scheduler** | Something has to be alive to wake the agent at 7:00 (part 11) |

> ⭐ **A rule that OpenClaw enforces and that I am stealing: exactly one gateway per host.**
> Not because it is prettier. Because with two instances **two copies of the
> scheduler will execute the same task twice**, and two processes appending to one
> log produce a file that cannot be replayed. You enforce this with a lock file
> — in §4.

---

## 1. Configuration as data, not as code

The most common mistake in the projects I have seen: configuration scattered across constants
in Python. It works until the moment you want to **change behaviour without a restart**,
**show someone what is set**, or **undo a change**.

### 1.1 · Three rules

1. **Configuration is one data file**, not a Python module. It can be validated,
   diffed and versioned.
2. **Every value has a sensible default.** An empty configuration file must yield a working
   system. (This is Steinberger's rule from the MCP Best Practices and it is very good.)
3. **Secrets are not in the configuration.** A separate layer, different file permissions (part 10).

### 1.2 · FROM SCRATCH

```bash
cat > $OSA/konfiguracja/system.json <<'EOF'
{
  "brama": {
    "host": "127.0.0.1",
    "port": 18789,
    "plik_blokady": "$OSA/brama.lock"
  },
  "modele": {
    "domyslny":  { "url": "http://127.0.0.1:8080/v1", "nazwa": "gpt-oss-20b" },
    "trudny":    { "url": "http://127.0.0.1:8080/v1", "nazwa": "qwen3-32b" },
    "limit_tokenow_wyjscia": 2048,
    "limit_sekund": 300
  },
  "sesje": {
    "katalog": "$OSA/dziennik",
    "max_zdarzen_na_plik": 50000
  },
  "zaufanie": {
    "konsola":  "host",
    "http":     "piaskownica",
    "kanal_dm": "piaskownica",
    "cron":     "host"
  }
}
EOF
```

⚠️ **Note the `zaufanie` section.** It looks innocent, and it is **the most important
part of the file**. It is the map "where the request came from" → "how much it is allowed". You will implement
it in §5, and enforce it in part 10.

Now loading — with defaults and `~` expansion:

```python
# $OSA/konfig.py
"""Configuration as data. An empty file = a working system."""
import json, os, pathlib

DOMYSLNE = {
    "brama":   {"host": "127.0.0.1", "port": 18789,
                "plik_blokady": "$OSA/brama.lock"},
    "modele":  {"domyslny": {"url": "http://127.0.0.1:8080/v1", "nazwa": "lokalny"},
                "limit_tokenow_wyjscia": 2048, "limit_sekund": 300},
    "sesje":   {"katalog": "$OSA/dziennik", "max_zdarzen_na_plik": 50000},
    "zaufanie": {"konsola": "host"},
}

def _scal(baza: dict, nowe: dict) -> dict:
    """Deep merge — the new overrides, but does not delete branches."""
    wynik = dict(baza)
    for k, v in nowe.items():
        if isinstance(v, dict) and isinstance(wynik.get(k), dict):
            wynik[k] = _scal(wynik[k], v)
        else:
            wynik[k] = v
    return wynik

def _rozwin(obiekt):
    """Expands ~ in every string that looks like a path."""
    if isinstance(obiekt, dict):
        return {k: _rozwin(v) for k, v in obiekt.items()}
    if isinstance(obiekt, list):
        return [_rozwin(v) for v in obiekt]
    if isinstance(obiekt, str) and obiekt.startswith("~"):
        return os.path.expanduser(os.path.expandvars(obiekt))
    return obiekt

def wczytaj(sciezka: str = "$OSA/konfiguracja/system.json") -> dict:
    p = pathlib.Path(os.path.expanduser(os.path.expandvars(sciezka)))
    z_pliku = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return _rozwin(_scal(DOMYSLNE, z_pliku))

if __name__ == "__main__":
    print(json.dumps(wczytaj(), indent=2, ensure_ascii=False))
```

```bash
python3 $OSA/konfig.py          # expect the full configuration with paths expanded
mv $OSA/konfiguracja/system.json /tmp/ && python3 $OSA/konfig.py
# ↑ still works — rule 2. Restore the file.
mv /tmp/system.json $OSA/konfiguracja/
```

---

## 2. A session as an event log

This is **the most important design decision in this part** and it is worth understanding before
you write the code.

### 2.1 · Why not a "list of messages"

The naive approach: a session is a list of messages, you keep it in memory, and write JSON at the
end. It breaks immediately:

| Problem | Why an event log does not have it |
| :-- | :-- |
| The process died halfway — you lose the whole session | Every event is written at once, you lose at most the last one |
| You do not know **when** something happened | Every event has a timestamp |
| You do not know **how much** a turn cost | A model event carries the token count |
| Compaction irreversibly destroys the history | Compaction is **also an event** — the original stays |
| You cannot "go back three turns and try differently" | A branch is a pointer to an event |

⭐ **The key difference:** a list of messages is **state**. An event log is **history,
from which state is computed**. State can always be reconstructed; history cannot
be reconstructed from state alone.

### 2.2 · The format

One event = one JSON line (JSONL). One file per session.

```json
{"seq":1,"ts":"2026-09-23T07:00:01.220Z","typ":"sesja.start","zaufanie":"host","zrodlo":"konsola"}
{"seq":2,"ts":"2026-09-23T07:00:01.221Z","typ":"wiadomosc","rola":"user","tresc":"how many files do I have in ~/dokumenty"}
{"seq":3,"ts":"2026-09-23T07:00:03.880Z","typ":"model.odpowiedz","tresc":"I'll check.","tokeny_we":412,"tokeny_wy":18,"ms":2659}
{"seq":4,"ts":"2026-09-23T07:00:03.881Z","typ":"narzedzie.wywolanie","narzedzie":"powloka","argumenty":{"cmd":"ls ~/dokumenty | wc -l"},"id":"w1"}
{"seq":5,"ts":"2026-09-23T07:00:04.010Z","typ":"narzedzie.wynik","id":"w1","kod":0,"tresc":"42"}
{"seq":6,"ts":"2026-09-23T07:00:05.900Z","typ":"model.odpowiedz","tresc":"You have 42 files.","tokeny_we":448,"tokeny_wy":9,"ms":1889}
```

**Eight event types are enough for the whole course:**

| Type | When | Carries |
| :-- | :-- | :-- |
| `sesja.start` | the session opens | trust level, source |
| `wiadomosc` | input from a human or a channel | role, content |
| `model.odpowiedz` | the model said something | content, tokens, time |
| `narzedzie.wywolanie` | the model wants to act | name, arguments, `id` |
| `narzedzie.wynik` | the tool replied | `id`, exit code, content |
| `blad` | anything went wrong | where, what |
| `kompakcja` | the history was summarised | `seq` range, summary |
| `galaz` | a rebound from an earlier point | parent `seq` |

> 💡 **Why `seq` next to `ts`.** Timestamps can repeat within the same
> millisecond and **are not monotonic** when the system clock changes. `seq` is
> monotonic by definition and it determines the order. `ts` is for humans to read and for metrics.
> **Never sort by `ts`.**

### 2.3 · FROM SCRATCH — the session store

```python
# $OSA/sesje.py
"""A session as an append-only event log. State = fold(events)."""
import json, os, pathlib, datetime, threading

TERAZ = lambda: datetime.datetime.now(datetime.UTC).isoformat(timespec="milliseconds").replace("+00:00", "Z")

class Dziennik:
    def __init__(self, katalog: str, sesja: str):
        self.sesja = sesja
        self.plik = pathlib.Path(katalog) / f"{sesja.replace(':', '~')}.jsonl"
        self.plik.parent.mkdir(parents=True, exist_ok=True)
        self._blokada = threading.Lock()
        self._seq = self._ostatni_seq()

    def _ostatni_seq(self) -> int:
        if not self.plik.exists():
            return 0
        ostatnia = 0
        with self.plik.open(encoding="utf-8") as f:
            for linia in f:
                if linia.strip():
                    ostatnia = json.loads(linia)["seq"]
        return ostatnia

    def dopisz(self, typ: str, **pola) -> dict:
        """The only way to change session state. Written immediately."""
        with self._blokada:
            self._seq += 1
            z = {"seq": self._seq, "ts": TERAZ(), "typ": typ, **pola}
            with self.plik.open("a", encoding="utf-8") as f:
                f.write(json.dumps(z, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())          # ← P64
            return z

    def zdarzenia(self, do_seq: int | None = None):
        if not self.plik.exists():
            return
        with self.plik.open(encoding="utf-8") as f:
            for linia in f:
                if not linia.strip():
                    continue
                z = json.loads(linia)
                if do_seq is not None and z["seq"] > do_seq:
                    return
                yield z
```

**The `os.fsync` on the write line is deliberate** — without it the event sits in the system buffer
and **is lost in a power failure**. It costs ~0.1 ms per event. For an agent doing
20 events per turn that is 2 ms. You pay it and do not argue (pitfall P64).

### 2.4 · Replay — state computed from history

```python
# $OSA/sesje.py (continued)

def odtworz(dziennik: Dziennik, do_seq: int | None = None) -> dict:
    """Assembles session state from events. This is the ONLY place where state is created."""
    stan = {"sesja": dziennik.sesja, "zaufanie": None, "zrodlo": None,
            "historia": [], "tokeny_we": 0, "tokeny_wy": 0, "bledy": 0,
            "kompakcje": [], "ostatni_seq": 0}

    for z in dziennik.zdarzenia(do_seq):
        stan["ostatni_seq"] = z["seq"]
        t = z["typ"]

        if t == "sesja.start":
            stan["zaufanie"], stan["zrodlo"] = z["zaufanie"], z["zrodlo"]

        elif t == "wiadomosc":
            stan["historia"].append({"rola": z["rola"], "tresc": z["tresc"]})

        elif t == "model.odpowiedz":
            stan["historia"].append({"rola": "assistant", "tresc": z["tresc"]})
            stan["tokeny_we"] += z.get("tokeny_we", 0)
            stan["tokeny_wy"] += z.get("tokeny_wy", 0)

        elif t == "narzedzie.wywolanie":
            stan["historia"].append({"rola": "assistant", "narzedzie": z["narzedzie"],
                                     "argumenty": z["argumenty"], "id": z["id"]})

        elif t == "narzedzie.wynik":
            stan["historia"].append({"rola": "tool", "id": z["id"], "tresc": z["tresc"]})

        elif t == "blad":
            stan["bledy"] += 1

        elif t == "kompakcja":
            # The history disappears from the CONTEXT, but STAYS in the file.
            ogon = stan["historia"][z["zachowaj_ostatnie"]:] if z.get("zachowaj_ostatnie") else []
            stan["historia"] = [{"rola": "system", "tresc": z["streszczenie"]}] + ogon
            stan["kompakcje"].append({"seq": z["seq"], "od": z["od_seq"], "do": z["do_seq"]})

    return stan
```

⭐ **Read the `kompakcja` branch again.** Compaction **deletes nothing from the file**
— it only changes what reaches the model's context. The original stays on disk forever.
That is why in part 15 you will be able to answer the question "what did the agent see in turn 40",
even if in turn 60 it compacted it long ago.

### 2.5 · Branches — "go back three turns and try differently"

```python
def odgalez(zrodlo: Dziennik, od_seq: int, nowa_nazwa: str) -> Dziennik:
    """A new session starting from the source session's state at event od_seq."""
    nowa = Dziennik(str(zrodlo.plik.parent), nowa_nazwa)
    nowa.dopisz("galaz", rodzic=zrodlo.sesja, rodzic_seq=od_seq)
    for z in zrodlo.zdarzenia(do_seq=od_seq):
        if z["typ"] != "sesja.start":
            nowa.dopisz(z["typ"], **{k: v for k, v in z.items()
                                     if k not in ("seq", "ts", "typ")})
    return nowa
```

**What you need it for.** In part 14 you build evaluation. Without branches the only way to
compare two variants is to run the task from scratch. With branches **you rebound
from turn 12 and test two different prompts on an identical initial state.** That is
the difference between an experiment and guessing.

---

## 3. IN PRODUCTION — JSONL or SQLite

You wrote JSONL. When does it stop being enough?

| Criterion | JSONL (yours) | SQLite WAL |
| :-- | :-- | :-- |
| Appending an event | ~0.1 ms + fsync | ~0.05 ms |
| Reading a whole session | linear, fast up to ~50k | linear, faster |
| **The query "all errors from the last week"** | ⚠️ a scan of all files | ⭐ an index, milliseconds |
| Multiple writers | ⚠️ needs an external lock | ⭐ built in |
| Readability with `cat` | ⭐ full | ✗ none |
| `grep` over the log | ⭐ works | ✗ does not work |
| Backup | `cp` | `.backup` |
| File corruption | you lose **one line** | risk to the whole file |

**Recommendation: stay with JSONL until part 15, then add SQLite as an index alongside,
not instead.** The log stays the source of truth (readable, `grep`-able,
resistant to corruption), SQLite is **a derivative that can be rebuilt** from the log
in a single pass. This is the same pattern as "log + materialized view" in databases.

> ⚠️ **The pitfall you will fall into if you do it the other way round.** When SQLite is the source
> of truth, one corrupted page of the file costs you the agent's entire history. When it is
> an index — you delete it and rebuild it in 10 seconds.

---

## 4. The gateway — one process, loopback, a lock

```python
# $OSA/brama.py
"""The gateway: the single source of truth about sessions. One per host."""
import json, os, sys, pathlib, http.server, socketserver
from konfig import wczytaj
from sesje import Dziennik, odtworz

K = wczytaj()

class JednaInstancja:
    """A lock file with a PID. Also detects a lock left by a dead process."""
    def __init__(self, sciezka): self.p = pathlib.Path(sciezka)
    def __enter__(self):
        if self.p.exists():
            pid = int(self.p.read_text().strip() or 0)
            try:
                os.kill(pid, 0)                       # alive?
                sys.exit(f"ERROR: the gateway is already running (PID {pid}). One per host.")
            except ProcessLookupError:
                print(f"WARNING: removing the lock left by a dead PID {pid}")
        self.p.write_text(str(os.getpid()))
        return self
    def __exit__(self, *a): self.p.unlink(missing_ok=True)

def poziom_zaufania(zrodlo: str) -> str:
    return K["zaufanie"].get(zrodlo, "piaskownica")   # ← P66: default to NARROWER

class Obsluga(http.server.BaseHTTPRequestHandler):
    def _odpowiedz(self, kod, dane):
        tresc = json.dumps(dane, ensure_ascii=False).encode()
        self.send_response(kod)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(tresc)))
        self.end_headers()
        self.wfile.write(tresc)

    def do_POST(self):
        if self.path != "/wiadomosc":
            return self._odpowiedz(404, {"blad": "unknown path"})
        n = int(self.headers.get("Content-Length", 0))
        zadanie = json.loads(self.rfile.read(n) or b"{}")

        sesja  = zadanie.get("sesja", "main")
        zrodlo = zadanie.get("zrodlo", "http")
        tresc  = zadanie.get("tresc", "")

        d = Dziennik(K["sesje"]["katalog"], sesja)
        if d._seq == 0:
            d.dopisz("sesja.start", zaufanie=poziom_zaufania(zrodlo), zrodlo=zrodlo)
        z = d.dopisz("wiadomosc", rola="user", tresc=tresc)

        stan = odtworz(d)
        self._odpowiedz(200, {"sesja": sesja, "seq": z["seq"],
                              "zaufanie": stan["zaufanie"],
                              "tur": len(stan["historia"])})

    def do_GET(self):
        if self.path.startswith("/sesja/"):
            d = Dziennik(K["sesje"]["katalog"], self.path.split("/", 2)[2])
            return self._odpowiedz(200, odtworz(d))
        self._odpowiedz(404, {"blad": "unknown path"})

    def log_message(self, *a): pass       # ← P63: silence on stdout

if __name__ == "__main__":
    with JednaInstancja(K["brama"]["plik_blokady"]):
        adres = (K["brama"]["host"], K["brama"]["port"])
        print(f"gateway: http://{adres[0]}:{adres[1]}  (loopback only)")
        socketserver.ThreadingTCPServer.allow_reuse_address = True
        with socketserver.ThreadingTCPServer(adres, Obsluga) as s:
            s.serve_forever()
```

**Run it and check:**

```bash
cd $OSA && python3 brama.py &
sleep 1

curl -s -X POST localhost:18789/wiadomosc \
  -H 'Content-Type: application/json' \
  -d '{"sesja":"test","zrodlo":"konsola","tresc":"hello"}' | python3 -m json.tool
# expect: {"sesja":"test","seq":2,"zaufanie":"host","tur":1}

curl -s -X POST localhost:18789/wiadomosc \
  -d '{"sesja":"test","zrodlo":"http","tresc":"second"}' | python3 -m json.tool
# expect: zaufanie STILL "host" — the session already exists, the level was fixed at the start

cat $OSA/dziennik/test.jsonl
python3 brama.py        # ← expect: ERROR: the gateway is already running
```

⭐ **Note the last test.** The trust level is **fixed once, when the session is opened**,
and does not change even when a subsequent message arrives from a more trusted source.
This is not a shortcoming — it is **a safeguard against escalation by swapping the
source**. A session opened from the network remains a session from the network forever.

---

## 5. EXPERIMENT 2 — replay fidelity

**Hypothesis:** the state replayed from the log is identical to the state of the process that
wrote it — for any point in the history.

**Procedure:**

```bash
cat > $OSA/testy/test_odtwarzanie.py <<'EOF'
import sys, json, random, hashlib
sys.path.insert(0, "/home/$USER/os-agenta")
from sesje import Dziennik, odtworz, odgalez

KAT = "/tmp/test-dziennik"
import shutil, pathlib; shutil.rmtree(KAT, ignore_errors=True)

d = Dziennik(KAT, "eksperyment")
d.dopisz("sesja.start", zaufanie="host", zrodlo="konsola")

# 200 synthetic turns
for i in range(200):
    d.dopisz("wiadomosc", rola="user", tresc=f"question {i}")
    d.dopisz("model.odpowiedz", tresc=f"answer {i}", tokeny_we=100+i, tokeny_wy=20, ms=900)
    if i % 7 == 0:
        d.dopisz("narzedzie.wywolanie", narzedzie="powloka",
                 argumenty={"cmd": f"echo {i}"}, id=f"w{i}")
        d.dopisz("narzedzie.wynik", id=f"w{i}", kod=0, tresc=str(i))

pelny = odtworz(d)
print(f"events: {pelny['ostatni_seq']}  turns: {len(pelny['historia'])}  "
      f"input tokens: {pelny['tokeny_we']}")

# 1. Does replaying twice give the same result?
h = lambda s: hashlib.sha256(json.dumps(s, sort_keys=True).encode()).hexdigest()[:16]
assert h(odtworz(d)) == h(odtworz(Dziennik(KAT, "eksperyment"))), "NON-DETERMINISTIC"
print("✓ replay is deterministic")

# 2. Does replay up to point N == the state after N events?
for punkt in random.sample(range(2, pelny["ostatni_seq"]), 20):
    czesc = odtworz(d, do_seq=punkt)
    assert czesc["ostatni_seq"] == punkt
    assert len(czesc["historia"]) <= len(pelny["historia"])
print("✓ partial replay consistent for 20 random points")

# 3. Does a branch from turn 50 share the prefix with the original?
g = odgalez(d, 100, "eksperyment-galaz")
assert odtworz(g)["tokeny_we"] == odtworz(d, do_seq=100)["tokeny_we"]
print("✓ the branch preserves the parent's state")
EOF

sed -i "s|/home/\$USER|$HOME|" $OSA/testy/test_odtwarzanie.py
python3 $OSA/testy/test_odtwarzanie.py
```

**Measure the cost too:**

| Measurement | Command | Your result |
| :-- | :-- | :-- |
| Time to append 1000 events | `time python3 -c "..."` | ___ ms |
| The same **without** `os.fsync` | comment out the line | ___ ms |
| Log size after 200 turns | `du -h ~/…/eksperyment.jsonl` | ___ KB |
| Time to replay 200 turns | `time` in the test | ___ ms |

⚠️ **Prediction to check:** `fsync` should cost ~10–30× more than a write without
it, but in absolute numbers **still under 1 ms per event on NVMe**. If
you get more than 5 ms — check whether the log happens to be on a network disk.

---

## 6. EXERCISE — `sesje` as a command-line tool

Write `$OSA/sesja-cli.py` with four commands. You will be using them **until the end of
the course**, so do it properly:

```bash
python3 sesja-cli.py lista                    # sessions, number of turns, last activity
python3 sesja-cli.py pokaz main               # a human-readable history
python3 sesja-cli.py pokaz main --do-seq 40   # the state at turn 40
python3 sesja-cli.py koszt main               # tokens in/out, errors, compactions
python3 sesja-cli.py odgalez main 40 proba-b  # a branch for an experiment
```

**Requirements that are not optional:**

1. `pokaz` without `--do-seq` shows the current state; with `--do-seq` the historical state.
2. `koszt` counts tokens **from the log**, it does not estimate.
3. No command modifies the log except `odgalez`.
4. Zero output on `stdout` other than the result — errors go to `stderr` (P63).

> 💡 **Why I make you write this now, and not in part 15.** Because from this moment every
> error you see in the course you will diagnose with this tool. If it appears
> late, for ten parts you will be debugging with `cat` and `grep`.

---

## 7. Pitfalls of this part

| ID | Pitfall | Symptom | How to avoid it |
| :-- | :-- | :-- | :-- |
| **P63** | **Printing to `stdout` in the gateway process** | The channel falls out of sync, the client gets garbage mixed into the JSON; with MCP — an immediate failure | Logging **only to a file or `stderr`**. `log_message` overridden with nothing |
| **P64** | **Writing without `fsync`** | After a power failure the last 2–3 turns vanish, and the session state is inconsistent with what the agent really did | `f.flush()` + `os.fsync()`. Cost <1 ms |
| **P65** | **Sorting events by `ts` instead of by `seq`** | Events from the same millisecond swap order; after a system clock change the history "goes back" | `seq` is the order. `ts` is for reading |
| **P66** | **The default trust level = the wider one** | A new channel that you forgot in the configuration gets host permissions | `K["zaufanie"].get(zrodlo, "piaskownica")` — **no entry means narrowest**, not widest |

---

## 8. Checkpoint

```bash
cd $OSA
python3 konfig.py > /dev/null            && echo "✓ configuration"
python3 testy/test_odtwarzanie.py        && echo "✓ replay"
pgrep -f brama.py > /dev/null            && echo "✓ the gateway is alive"
python3 sesja-cli.py lista               && echo "✓ cli"
git add -A && git commit -m "part 2: gateway, configuration, event log"
```

- [ ] The gateway runs, on `127.0.0.1` only, a single instance enforced by a lock
- [ ] Configuration is data; an empty file yields a working system
- [ ] A session is an event log; **state is computed, not stored**
- [ ] You can replay the state from any turn
- [ ] You can branch a session and compare two variants
- [ ] The trust level is fixed **when the session is opened** and does not escalate
- [ ] You have `sesja-cli.py` and will use it until the end of the course

---

**Next: `03-HARNESS-LONG-RUNNING-TASKS.md`** — the most important part of the course. A loop that
survives five context windows and knows what it did yesterday.
