# Part 18 · Release and maintenance

**Level:** ⭐⭐⭐⭐ · **Time:** ~4 h · **Requires:** parts 14 (gate), 15 (metrics), 16 (security)
**Produces:** system versioning, rollback, memory migration, backups, a runbook

---

## 0. What it means to "release" an agentic system

In ordinary software a release is code. Here behaviour depends on **seven things**,
and changing **any** of them changes the result:

```
   code       ██████░░░░░░░░░░░░░░   ~30% of the influence on behaviour
   prompts    ████████░░░░░░░░░░░░   ~25%
   tools      █████░░░░░░░░░░░░░░░   ~15%
   model      █████░░░░░░░░░░░░░░░   ~15%
   config     ███░░░░░░░░░░░░░░░░░   ~8%
   skills     ██░░░░░░░░░░░░░░░░░░   ~5%
   memory     █░░░░░░░░░░░░░░░░░░░   ~2%  ⚠️ but it grows over time
```

⚠️ **A prompt change without a code change is a full-fledged release.** It has the
same impact as a code change, and almost nobody treats it that way. This is **the
main cause of the "it worked last week" situation**.

⭐ **The rule: a release is the frozen state of ALL seven, with the golden-set result
recorded.** Without the result it is not a release, just a coincidence.

---

## 1. The release manifest

```python
# $OSA/wydanie/manifest.py
def zbuduj(wersja: str) -> dict:
    return {
        "wersja": wersja,
        "data": TERAZ(),
        "git": _git("rev-parse", "HEAD"),
        "czyste_repo": _git("status", "--porcelain") == "",   # ⚠️ P136
        "skladniki": {
            "prompty":     _sha_katalogu("agenci", "*.md"),
            "narzedzia":   _sha_katalogu("narzedzia", "*.py"),
            "umiejetnosci":_sha_katalogu("agenci/*/umiejetnosci", "SKILL.md"),
            "konfiguracja":_sha_pliku("konfiguracja/system.json"),
            "modele": {n: {"plik": s["model"], "sha256": _sha_modelu(s["model"])}
                       for n, s in SILNIKI.items() if "url" in s},
            "silnik": _wersja_llama_cpp(),
        },
        "ewaluacja": json.loads(pathlib.Path("pomiary/ewaluacja/biezacy.json").read_text()),
        "schemat_pamieci": _wersja_schematu_pamieci(),
    }
```

⭐ **The `sha256` of the GGUF file is non-obvious here, but necessary.** Re-downloading
"the same" version of a model can yield a different file — a different quantization, a
fix in the conversion, a different build. Without a checksum **a rollback will not
reproduce the behaviour** and you will be looking for the cause in code nobody touched.

---

## 2. The release pipeline

```bash
#!/usr/bin/env bash
# $OSA/wydanie/wydaj.sh
set -euo pipefail
WERSJA="${1:?version, e.g. 1.4.0}"

echo "1/7 · repository cleanliness"
[ -z "$(git status --porcelain)" ] || { echo "✗ uncommitted changes"; exit 1; }

echo "2/7 · unit tests"
python3 -m pytest testy/ -q

echo "3/7 · escape attempts (part 10)"
python3 testy/ucieczka/proby.py --poziom scisly --wymagaj-porazki-wszystkich

echo "4/7 · ASI attacks (part 16)"
python3 testy/ataki/ataki.py --wszystkie --min-zdanych 18

echo "5/7 · golden set — 3 runs"
python3 ewaluacja/uruchom.py --przebiegow 3 --zapisz pomiary/ewaluacja/biezacy.json

echo "6/7 · regression gate (part 14)"
python3 ewaluacja/bramka.py --wzgledem pomiary/ewaluacja/baza.json || {
  echo "✗ REGRESSION. Release halted."; exit 1; }

echo "7/7 · manifest and tag"
python3 wydanie/manifest.py "$WERSJA" > "wydania/$WERSJA.json"
git add wydania/ && git commit -q -m "release $WERSJA"
git tag -a "v$WERSJA" -m "$(python3 wydanie/podsumuj.py "$WERSJA")"
echo "✓ release $WERSJA ready.  Rollback: wydanie/wycofaj.sh <previous>"
```

⭐ **Step 6 is the heart of this pipeline.** Everything else is hygiene; the regression
gate is the only mechanism that will **stop you from making the system worse in good
faith**.

---

## 3. Rollback

```bash
#!/usr/bin/env bash
# $OSA/wydanie/wycofaj.sh — goal: under 5 minutes
set -euo pipefail
WERSJA="${1:?target version}"
M="wydania/$WERSJA.json"
[ -f "$M" ] || { echo "✗ manifest $M missing"; exit 1; }

echo "→ stopping"
systemctl --user stop osa-brama osa-planista

echo "→ copy of the current state (in case the rollback was a mistake)"
tar czf "/tmp/osa-przed-wycofaniem-$(date +%s).tgz" pamiec/ dziennik/ konfiguracja/

echo "→ code, prompts, configuration"
git checkout "v$WERSJA" -- agenci/ narzedzia/ konfiguracja/ *.py

echo "→ verifying models"
python3 wydanie/sprawdz_modele.py "$M" || {
  echo "⚠️ MODEL DOES NOT MATCH. Behaviour may deviate from release $WERSJA."; }

echo "→ memory migration backwards"
python3 pamiec/migruj.py --do-wersji "$(jq -r .schemat_pamieci "$M")"

echo "→ start and check"
systemctl --user start osa-brama osa-planista
sleep 5 && python3 wydanie/kontrola.py --szybka
echo "✓ rolled back to $WERSJA"
```

⚠️ **A copy of the state before the rollback** — because a rollback is sometimes a
wrong diagnosis, and then you want to return to what you have just overwritten.

### 3.1 · Memory does not roll back

⭐ **This is the most important thing in this part and the easiest to overlook.**

Code rolls back. Prompts roll back. **Memory accumulated between releases does not**,
and should not: those are real facts about you gathered over a week.

```python
# $OSA/pamiec/migruj.py
MIGRACJE = {
    (1, 2): lambda db: db.executescript("""
        ALTER TABLE fakty ADD COLUMN pewnosc REAL DEFAULT 1.0;
        UPDATE fakty SET pewnosc = 1.0 WHERE pewnosc IS NULL;"""),
    (2, 3): lambda db: db.executescript("""
        ALTER TABLE fakty ADD COLUMN cytat TEXT;"""),
}
WSTECZ = {
    (2, 1): lambda db: None,      # ⭐ the column stays — the old code does not read it
    (3, 2): lambda db: None,
}
```

⭐ **The "backward migration does nothing" pattern is correct and deliberate.** You do
not remove the column — the old code simply does not read it, and the data survives a
return to the newer version. **Removing a column on rollback is an irreversible loss of
data for a reason that was meant to be reversible.**

**The rule: the memory schema changes only by addition.** No `DROP COLUMN`, no type
changes, no changes to the meaning of an existing field.

---

## 4. Backups

| What | Frequency | Where | Why |
| :-- | :-- | :-- | :-- |
| `pamiec/pamiec.db` | ⭐ daily | local + external drive | **irreplaceable** |
| `agenci/**/*.md` | on change | git | system behaviour |
| `dziennik/*.jsonl` | weekly | local | source of evaluation and investigations |
| `pomiary/` | on change | git | without baselines there is no gate |
| GGUF models | ✗ no | — | can be re-downloaded; keep only the checksums |
| `sekrety.json` | ⭐ manually | ⚠️ **off the machine, encrypted** | the only thing you cannot recreate |

```bash
#!/usr/bin/env bash
# $OSA/kopia.sh — in the nightly job (part 11)
set -euo pipefail
CEL="${KOPIA_CEL:-$HOME/kopie/osa}"; mkdir -p "$CEL"
D=$(date +%Y%m%d)

sqlite3 $OSA/pamiec/pamiec.db ".backup '$CEL/pamiec-$D.db'"   # ⭐ not cp!
tar czf "$CEL/dziennik-$D.tgz" -C $OSA dziennik/
tar czf "$CEL/konfig-$D.tgz"  -C $OSA konfiguracja/ agenci/ wydania/

# ⭐ restore test — an unverified backup is not a backup
sqlite3 "$CEL/pamiec-$D.db" "SELECT count(*) FROM fakty" > /dev/null \
  || { echo "✗ BACKUP CORRUPTED"; exit 1; }

find "$CEL" -name 'pamiec-*.db' -mtime +30 -delete
echo "✓ backup $D ($(du -sh "$CEL" | cut -f1))"
```

⚠️ **`sqlite3 .backup`, not `cp`.** Copying a SQLite file during a write produces a
file **corrupted in a way that will only show up on restore** — that is, at the worst
possible moment.

---

## 5. Health check

```python
# $OSA/wydanie/kontrola.py
KONTROLE = [
    ("gateway responds",     lambda: _http("GET", "/zdrowie")["ok"]),
    ("scheduler alive",      lambda: _systemd("osa-planista") == "active"),
    ("model responds",       lambda: _model_echo() is not None),
    ("memory writable",      lambda: _test_zapisu_pamieci()),
    ("log writable",         lambda: _test_zapisu_dziennika()),
    ("disk space",           lambda: _wolne_gb() > 20),
    ("VRAM available",       lambda: _wolne_vram_gb() > 4),
    ("GRANICE.md 444",       lambda: _prawa_granic() == "444"),        # pt. 6
    ("secrets 600",          lambda: _prawa_sekretow() == "600"),      # pt. 10
    ("no network in the sandbox", lambda: not _piaskownica_ma_siec()), # pt. 10
    ("backup < 48 h",        lambda: _wiek_kopii_h() < 48),
    ("golden set < 7 days",  lambda: _wiek_ewaluacji_dni() < 7),
]
```

```bash
python3 wydanie/kontrola.py
# ✓ gateway responds          ✓ GRANICE.md 444
# ✓ scheduler alive           ✓ secrets 600
# ✓ model responds            ✓ no network in the sandbox
# ✓ memory writable           ⚠️ backup from 61 h ago
# ✓ log writable              ✓ golden set from 2 days ago
# ✓ space: 412 GB             ✓ VRAM: 58.1 GB
# 11/12 — 1 warning
```

---

## 6. The runbook for three in the morning

⭐ **Write it when you are rested and nothing is on fire.** When something is on fire,
you will not write it well.

```markdown
# RUNBOOK · Agent system

## First, always
    python3 $OSA/wydanie/kontrola.py
If you do not know what to do — `bash $OSA/STOP.sh`. You lose nothing.

## The agent does not respond
1. `systemctl --user status osa-brama`
2. `tail -50 $OSA/dziennik/brama.log`
3. Is the model alive? `curl -s localhost:8080/health`
4. A lock left by a dead process? `cat $OSA/brama.lock` → `kill -0 <PID>`
5. `systemctl --user restart osa-brama`

## The agent responds, but stupidly
1. `python3 ewaluacja/uruchom.py --szybki` — how bad is it?
2. `python3 sesja-cli.py metryki --okres 7d` — since when?
3. `git log --oneline -20 -- agenci/ narzedzia/ konfiguracja/` — what changed?
4. `python3 wydanie/wycofaj.sh <last good>`
5. Only then look for the cause. **Restore first, diagnose later.**

## The agent is doing something it should not
1. ⭐ `bash $OSA/STOP.sh` — IMMEDIATELY
2. `python3 sesja-cli.py sledztwo --ostatnie 10` (part 15)
3. `python3 bezpieczenstwo/dryf.py --agent <x>` (part 16)
4. `python3 testy/ataki/ataki.py --wszystkie`
5. Resume only after you understand

## The machine is crashing / the cards are on fire
1. `rocm-smi` — temperatures, power
2. `python3 sesja-cli.py flota --aktywne` — how many parallel sessions
3. Limit: `limit_rownoczesnych` in the configuration (part 13 §5.3)
4. In an emergency: `systemctl --user stop osa-planista` (leaves the gateway reactive)

## Disk full
1. `du -sh $OSA/*` — usually `dziennik/`
2. `python3 dziennik/kompaktuj.py --starsze-niz 30d`
3. `find /tmp/praca -mtime +1 -delete`

## Rebuild from scratch
1. `git clone` + `git checkout v<version>`
2. `bash init.sh`
3. `sqlite3 pamiec/pamiec.db ".restore '<backup>'"`
4. `python3 pamiec/migruj.py --do-biezacej`
5. `python3 wydanie/kontrola.py`
6. `python3 ewaluacja/uruchom.py --wzgledem-manifestu v<version>`
```

⚠️ **"Restore first, diagnose later" is counterintuitive for engineers** — the natural
reflex is to understand the cause. At 3 a.m. that is the wrong reflex. A rollback takes
5 minutes, a diagnosis two hours, and the evidence stays in the log and will not go
anywhere.

---

## 7. EXPERIMENT 18 — break it and roll back

⭐ **An exercise nobody does until they have to — and then it is too late.**

```bash
python3 ewaluacja/uruchom.py --przebiegow 3 --zapisz /tmp/przed.json
bash wydanie/wydaj.sh 1.0.0-test
```

**Introduce a failure (choose at random, without looking):**

```
A. remove one tool from the registry
B. change the Archivist's prompt to the version from three months ago
C. swap the model for a different quantization
D. break the memory schema (add NOT NULL without a default value)
E. change the compaction threshold to 20%
F. remove the Researcher's GRANICE.md
```

| Measure | Your result |
| :-- | --: |
| Time to **notice** (check/evaluation/metrics) | ___ min |
| Time to **diagnose** (which change) | ___ min |
| Time to **roll back** | ___ min |
| Did the memory survive? | yes / no |
| Did the score return to `/tmp/przed.json`? | yes / no |
| Was the runbook enough, or did you improvise? | |

⚠️ **Prediction:** A and C you will notice quickly (check, evaluation). B and E are
insidious — the system works, just worse. **D is the worst**, because it breaks writes,
and rolling back the code will not fix it without a migration. **F will not be noticed
by the evaluation at all** — only `kontrola.py` and the ASI attacks from part 16 will
catch it.

⭐ **Failure F is the most important lesson: evaluation measures quality, not
security.** Removing the boundaries will **improve** the golden-set score, because the
agent will be able to do more. That is why `kontrola.py` checks file permissions, and
the release pipeline runs the ASI attacks **alongside** the regression gate, not
instead of it.

**After the experiment: add to the runbook whatever it was missing.** That is the only
way it matures.

---

## 8. Ongoing hygiene

| Rhythm | What |
| :-- | :-- |
| **Every night** (part 11) | evaluation, memory audit, drift detection, backup, log compaction |
| **Every week** | metrics review (⭐ `sr_krokow`), egress audit, the queue of non-urgent items |
| **Every month** | 3 new golden-set questions from real failures; review of `SOUL.md` |
| **Every quarter** | escape attempts, supply registry, `eval`/`exec` audit, model updates |
| **Every six months** | ADR review: which decisions did not hold up and **why** |

⭐ **The monthly row is the one that keeps the system alive.** Three questions a month
is 36 a year — the golden set grows with your experience and **stops measuring things
you have long since mastered**, and starts measuring the ones that painfully surprised
you.

---

## 9. Traps of this part

| ID | Trap | Symptom | How to avoid |
| :-- | :-- | :-- | :-- |
| **P136** | **A release with uncommitted changes** | The manifest does not describe what is running; rollback does not reproduce behaviour | Pipeline step 1: `git status --porcelain` must be empty |
| **P137** | **Rolling back code without a backward memory migration** | Old code + new schema = write errors; data in an inconsistent state | Schema version in the manifest; backward migrations that **add, not remove** |
| **P138** | **`cp` instead of `sqlite3 .backup`** | Corrupted backup; you find out on restore | `.backup` + a read test **in the same script** |
| **P139** | **A model not versioned by checksum** | "The same" GGUF behaves differently after download; you hunt for the bug in the code | `sha256` of the model file in the manifest; `sprawdz_modele.py` on rollback |

---

## 10. Checkpoint

```bash
cd $OSA
bash wydanie/wydaj.sh 1.0.0-test
python3 wydanie/kontrola.py
bash wydanie/wycofaj.sh <previous> && python3 wydanie/kontrola.py --szybka
python3 - <<'EOF'
import json, pathlib
m = json.loads(sorted(pathlib.Path("wydania").glob("*.json"))[-1].read_text())
assert m["czyste_repo"],                              "P136"
assert all("sha256" in v for v in m["skladniki"]["modele"].values()), "P139"
assert "ewaluacja" in m and m["ewaluacja"]["ogolem"] > 0, "no evaluation result"
print("✓ manifest complete")
EOF
bash kopia.sh && echo "✓ backup with a restore test"
test -s RUNBOOK.md && echo "✓ runbook"
git add -A && git commit -m "part 18: release, rollback, backups, runbook"
```

- [ ] A release covers **seven** components, not just code
- [ ] A prompt is a full-fledged release
- [ ] The manifest contains the `sha256` of the **models**
- [ ] The release pipeline has the regression gate **and** the ASI attacks
- [ ] Rollback under 5 minutes, with a copy of the state beforehand
- [ ] The memory schema changes **only by addition**
- [ ] Backups via `.backup`, with a read test
- [ ] `kontrola.py` also checks **file permissions**
- [ ] The runbook written **before** the failure, corrected **after** the experiment
- [ ] ⭐ **You broke the system deliberately and rolled back — you know your times**

---

**Next: `19-CAPSTONE.md`** — you assemble everything into a single personal assistant
and measure how far you have come since part 1.
