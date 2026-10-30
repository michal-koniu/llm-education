# 03. What agents can and cannot do, and the pipeline designs

As of 30 October 2026. Numbers in brackets point to `SOURCES.md`.

---

## 1. Where "agents do everything" fails

The idea is attractive: a local rig with LLMs, TTS, image and video models, browser agents and publishing agents turns out guides, videos and translations around the clock. In this market it fails in six specific places.

| # | Failure point | Why | Evidence |
|---|---|---|---|
| 1 | **Agents cannot play the game** | GTA 6 is console-only and single-player. There is no API, no datamining on console, and automating play or account access is a terms-of-service problem. Every fact about the world has to come from a human playing, or from community submissions | (official / reported) [3, 26, 80] |
| 2 | **Platforms price in mass production** | YouTube's "inauthentic content" policy targets templated, mass-produced, low-commentary videos. A cluster system reportedly terminated about 130,000 channels in six months, judged on shared templates and infrastructure (deployment unconfirmed; a reported under-1% reversal rate is unverified). One rig, one template, many channels is the pattern it looks for | (official) [28]; (reported) [32, 33] |
| 3 | **Search prices in mass production** | Google's "scaled content abuse" applies "no matter how it's created", and names automated translation of scraped content | (official) [37] |
| 4 | **Rights holder enforcement** | Take-Two strikes AI-generated "gameplay" and fake leaks, ports, and anyone monetising its IP outside its channel. Agents that remix official trailers or invent footage walk into that | (reported) [22, 23, 25] |
| 5 | **Answer engines eat short facts** | AI Overviews roughly halve clicks on factual queries. Pages that only state a fact are being replaced by the same kind of model you would use to write them | (reported) [38] |
| 6 | **Saturation is symmetric** | Every competitor has the same models. Elden Ring had 183,670 channels streaming in 3.5 days; GTA 6 will have more. Cheaper output does not raise your probability if everyone's output gets cheaper. YouTube's free auto-dub [35] already removed translation as a video moat | (reported) [54]; (estimate) |

**What survives these six:** agents doing the work around a human core of first-hand play, editorial judgement and community trust. On the recommended combination, agents can carry roughly 60% to 75% of the hours (estimate). The remaining 25% to 40% is what the platforms pay for.

### What agents are good at here

| Task | Agent fit | Notes |
|---|---|---|
| Ingesting and transcoding capture, scene detection, OCR of on-screen text | High | Your own footage only |
| Transcribing and summarising your spoken notes | High | Turns a play session into structured notes |
| Structured data: schema, deduplication, validation, rendering pages from records | High | The core of W2 |
| Coordinate conversion from human-placed pins to map coordinates | High | The human places the pin; the agent normalises it |
| Draft scripts and guide text **from verified records and your notes** | Medium-high | Never from model memory: the game is new, so model memory about it is wrong by default |
| Translation with a fixed glossary, subtitles, hreflang | High | Needs native sample review |
| Thumbnails and title variants from your own frames | Medium | No official key art, no logos |
| Rough cuts, chapters, Shorts candidates | Medium-high | Human picks and approves |
| Community intake bots, moderation, duplicate detection | High | Within Discord's rules |
| Analytics, rank tracking, policy-change monitoring | High | Watch the policy pages, not just traffic |
| Lua / JS scripts for FiveM (P3) | High | Test on a local server |
| Playing the game, judging spoilers, voice, trust, legal replies | **None or low** | Human |

### What agents must not be used for

- Creating or warming many accounts, buying or faking views, upvotes, reviews or comments.
- Posting promotional content into Reddit, Discord servers or forums at volume. Community rules and spam filters treat this as spam, and one ban can cost you the community you need for data.
- Scraping competitors' guides, maps or wikis and rewriting them.
- Logging into players' Rockstar accounts or any automated access to Rockstar services.
- Auto-checkout on retailer sites.
- Generating "GTA 6 footage", character renders presented as real, or fake leaks.
- Cloning the voices of GTA characters or their voice actors, or generating real cast members' likeness. The Mod Guidelines ban Rockstar voice performances and real people's likeness without consent [10, 11]; with a TTS model at hand, this is the most tempting violation.
- Running "free GTA 6 code" or "PC beta key" giveaways to farm follows, or any giveaway you cannot fulfil.
- Naming the site, channel, domain or app with "GTA" or "Grand Theft Auto".

---

## 2. Recommended combination

**Core (launch window):**

1. **W2: Map and collectible tracker** as the durable asset.
2. **V1: Human-led YouTube guide channel** as the audience engine and the source of capture that also feeds W2.
3. **W3: Localised editions** of both: web pages in 3, then 6 to 8 languages; YouTube auto-dub reviewed by a human.
4. **W5: Free Discord** as the community data intake; paid tier later.
5. **V2: Shorts** cut from every long video, as a feeder only.
6. **C1: Gear affiliate** links, labelled, on the site and in descriptions, for the Black Friday to January window only.

**Cash engine (pick one; it is the #1 or #2 option by the selection rule in `02`):**

- Default: **S1, creator services**: subtitles, translations, Shorts cuts and thumbnails for other GTA creators, sold from the same pipeline (A1, A7, A9). Start in week 3, when your own launch capture slows.
- If you code: **S3, freelance FiveM development** now, and **P3, your own FiveM scripts** from month 2 or 3. Independent of the GTA 6 launch; positions you for a 2027 to 2028 creator platform.
- If you write and prefer certainty: **S2**, freelance guide or video work for a publisher. Highest probability (Prob 4) but the least agent leverage. Check that the contract doesn't claim your own data.

**Why this mix (estimate):**
- The channel and the tracker share **one capture effort**: each play session produces video, data records and screenshots.
- The tracker is the part AI Overviews and saturation hurt least, and the part agents help most.
- Localisation multiplies both, at near-zero marginal cost on a local rig.
- The cash engine pays something even if the channel and site stay in the low case, which is the most likely outcome for them.

### Expected outcome of the combination

Single operator, new entrant, months 4 to 12 average, net. All figures are estimates built from the per-option ranges and weights in `02-OPTIONS-RATED.md`, not reported results.

**Derivation.**
- Core (W2 + V1 + W3 + W5 + V2 + C1): W2 reaches its base case about 24% of the time, V1 about 22%. If they were independent, P(at least one) = 1 − 0.76 × 0.78 ≈ 41%. They are positively correlated (a growing channel feeds the site; both fail when the vertical is wrong), so use **≈ 35%**. Either part's high case (5% and 4%) gives ≈ 7% for the core reaching $3,500+.
- Cash engine (S1): 38% standalone; run part-time from week 3, assume ≈ 30%, roughly independent of the core. P(core or S1 reaches base) = 1 − 0.65 × 0.70 ≈ **55%**.

| Combined net / month (m4 to 12) | 12-month net | Core only | Core + S1 |
|---|---|---|---|
| Under $400 | -$1,500 to $3,000 | ~65% | ~45% |
| $400 to $3,500 | $3,000 to $30,000 | ~28% | ~45% |
| $3,500 to $10,000 | $25,000 to $80,000 | ~5% | ~7% |
| Over $10,000 | $80,000 to $250,000 | ~2% | ~3% |

The bands cover every outcome and each column sums to 100%. The weights assume the time commitment stated in `02` §1; with less time, shift weight to the first row.

---

## 3. Pipeline design

### 3.1 Overview

```
 HUMAN: play + capture + voice notes
        |
        v
 [A1 Ingest] --> [A2 Policy/spoiler gate] --(flags)--> HUMAN GATE H2
        |                                                 |
        v                                                 v
 [A3 Record builder] <-- [A4 Community intake bot] <-- Discord submissions
        |
        +--> HUMAN GATE H3 (verify new item types; sample others)
        |
        v
 Structured data store (records, coordinates, screenshots, status)
        |                         |                          |
        v                         v                          v
 [A5 Site builder]        [A6 Script drafter]         [A9 Localiser]
        |                         |                          |
        v                         v                          v
 Tracker + pages           HUMAN GATE H4 (voice,       HUMAN GATE H5
 (auto-publish if           record, edit, approve)     (native sample)
  verified)                       |                          |
        |                         v                          |
        |                  [A7 Edit assist] --> [A8 Publisher] <---+
        |                         |
        v                         v
 [A10 Monitor: analytics, ranks, policy pages, claims inbox, uptime]
        |
        v
 [A11 Comment & feedback triage] --> corrections back to A3
                                  --> HUMAN GATE H6 (claims, legal, money)
```

### 3.2 Agents

| Agent | Does | Inputs | Outputs | Hard limits |
|---|---|---|---|---|
| **A0 Orchestrator** | Queues jobs, retries, cost and time budgets, daily report | All agent states | Job graph, daily summary to the human | No publishing rights of its own |
| **A1 Ingest** | Transcodes capture, scene detection, OCR of HUD and on-screen text, transcribes your voice notes, timestamps | Raw capture, voice memos | Clips, frames, transcript, candidate events ("collectible pickup at 00:41:12") | Your own footage only |
| **A2 Policy and spoiler gate** | Classifies segments: story cutscene, ending, mission reveal, violence in the first ~15 seconds, raw cutscene runs | Clips, transcript, policy checklist | Pass / flag / block, with reasons | Cannot approve its own flags; anything flagged goes to H2 |
| **A3 Record builder** | Turns events and submissions into records: type, name, coordinates, screenshot, conditions, missable flag, confidence, source | A1 events, A4 submissions, human pins | Draft records | A record without a human-verified source stays "unverified" and is not shown as fact |
| **A4 Community intake bot** | Discord form for submissions, image checks, duplicate detection against existing records, credit to submitter, anti-spam | Discord | Submissions queue | Follows Discord and server rules; no DMs to non-members |
| **A5 Site builder** | Renders tracker UI and one page per record from templates, schema markup, sitemaps, internal links, deploys | Verified records | Static site and tracker | Pages only for records with real data; no filler pages; publishing rate capped (see 3.4) |
| **A6 Script drafter** | Drafts video scripts and guide copy **from records and your transcript**, with record IDs cited inline | Records, transcript, outline | Draft script | Never adds facts that are not in a record or transcript |
| **A7 Edit assist** | Rough cut against the approved script, chapters, captions, map overlays from records, thumbnail and title variants from your frames, Shorts candidates | Approved script, clips | Project file, variants | No official key art, logos or trailer footage |
| **A8 Publisher** | Uploads, schedules, sets metadata, enables auto-dub review, posts Shorts | Human-approved packages | Live videos | Only publishes packages with an H4 approval token |
| **A9 Localiser** | Translates pages and subtitles against a fixed glossary of in-game names; hreflang; flags low-confidence segments | Approved English | Localised pages, subtitle files | Sample of each batch goes to H5 before a language goes live; afterwards spot checks |
| **A10 Monitor** | Analytics, rank tracking, uptime, Partner Program progress toward the 31 Jan 2027 deadline, **diffs of policy pages** (Rockstar video and mod policy, YouTube monetisation, Google spam policy, Tebex/Cfx terms), claims and strikes inbox | APIs, page snapshots | Weekly report, instant alerts on claims or policy diffs | Read-only |
| **A11 Feedback triage** | Classifies comments and messages: correction, question, spam, abuse | Comments, Discord, email | Corrections to A3, FAQ candidates, moderation actions | Escalates anything legal, financial or personal to H6 |
| **A12 FiveM coder** (hedge, P3) | Writes and tests Lua/JS scripts on a local FiveM server, docs, changelogs, support drafts | Human product spec | Builds, docs | Never builds banned monetisation (loot boxes, currency sales); human reviews before release |

### 3.3 Human gates

| Gate | When | Time per day (estimate) | What the human decides |
|---|---|---|---|
| **H1 Play and capture** | Every session | 1.5 to 2 h at launch, 0.5 to 1 h later | What to capture; records spoken notes; places map pins |
| **H2 Spoiler and policy** | Every flagged segment | 10 to 20 min | Keep, blur, cut or delay |
| **H3 Data verification** | Every new item type; a sample of others; every community record before it is marked verified | 15 to 30 min | True or false; confidence |
| **H4 Voice and approval** | Every long video | 30 to 60 min | Narration (own voice, or disclosed synthetic voice with own script edits), final cut, title, thumbnail |
| **H5 Native review** | First batch of each language, then about 10% samples | Paid reviewers, a few hours a week | Quality pass or fix |
| **H6 Claims, legal, money** | When triggered | As needed | Responses to takedowns or claims; sponsor deals and their disclosure; paid tiers; anything involving payments |
| **H7 Weekly review** | Once a week | 30 to 60 min | Read A10's report; adjust plan; apply kill criteria (file 04) |

**Total:** about 2.5 to 4 h/day at launch for H1 to H4, plus community replies, which is the 3 to 4.5 h/day assumed in `02` §1. A cash engine (S1, S3 or S2) adds 0.5 to 1 h/day from week 3. See the budget in file 04.

### 3.4 Guard rails built into the pipeline

1. **No record, no page.** A5 can only render a page backed by a verified record or an original human-written guide. This keeps the site out of "scaled content abuse" [37].
2. **Publishing rate caps.** Pages per day tied to records verified that day. No bulk page generation.
3. **One channel, one voice.** Do not clone the channel into many language channels or niche channels run from the same template. Use auto-dub and subtitles on the main channel instead [33, 35].
4. **Model memory is not a source.** The game is new. A6 and A9 work only from records and transcripts. Anything else is a hallucination by default.
5. **Own assets only.** Your captures, a map drawn from your own observations (not traced from the in-game map or official art, which is arguably a derivative work and still a takedown risk), your icons. No ripped textures, no official art or logos, a not-affiliated line on every page, and no "GTA" in brand, domain or app names.
6. **Paid tiers sell features, never footage.** Sync, ad-free, early tool access and community roles only. No paywalled GTA videos, screenshots or galleries [14].
7. **Disclosure.** Sponsorships and affiliate links are labelled as advertising in the video, description and page.
8. **Spoiler policy as code.** A2 checks for the cases Rockstar removes: isolated cutscenes, endings, raw official videos [14, 15]. Story walkthroughs carry spoiler warnings and chapter separation.
9. **AI disclosure.** Label synthetic voice or AI-generated imagery where platforms require it. YouTube applies its own labels anyway [31].
10. **Policy diffs are alerts.** A10 snapshots the policy pages weekly; any change pings the human. The rules changed several times in 2025 to 2026.

### 3.5 Stack

Keep it boring: a console and capture card; local ASR, OCR, a mid-size LLM for drafting and classification, a glossary-driven translation model, an image model for thumbnail backgrounds from your own frames; records in a database or JSON/GeoJSON with status and source fields; a static site with a client-side tracker; one Discord with a submission bot; a job queue that checks approval tokens before any publish step. Reliability in launch week matters more than features.

---

## 4. Variant pipelines

### 4.1 Creator services (S1)

Same A1, A7, A9 agents, pointed at a client's footage. Human gates: client scoping, spoiler policy per client, final delivery approval. Price per video or per month. Do not reuse a client's footage or data in your own assets without a written agreement.

### 4.2 FiveM script shop (P3)

A12 builds and tests on a local server; the human writes the spec, chooses the market gap, reviews code and UX, and owns support. A10 watches the Creator Platform terms and Tebex fee pages. Use the platform's asset escrow. The storefront carries the required not-endorsed line [16].
