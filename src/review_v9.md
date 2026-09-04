# Review v9 — three-person panel, round three

Rendered with Playwright over `http://127.0.0.1:8899/` (file:// is blocked), Chromium, at **390×844** and **1440×900**.
Reveal animations were force-completed before every screenshot so nothing is judged as "missing" when it is only un-scrolled.
Read-only review. Nothing in the site was modified.

Out of scope, acknowledged, not counted against the site: `[ADD LINKEDIN / EMAIL]` contact placeholder, `noindex` meta.

---

## Headline: one root-cause defect explains most of what looks "generic"

**Every straight connector line in every custom illustration is invisible.** Not faint — not painted at all.

`banners.py:defs()` builds the wire gradients as
`<linearGradient id="{p}w" x1="0" x2="1">` — no `gradientUnits`, so it defaults to `objectBoundingBox`.
A perfectly horizontal `<polyline>` has a bounding box of height 0. Per the SVG spec an element with a degenerate
bounding box referencing an `objectBoundingBox` gradient **is not rendered**. Every wire whose points share one `y`
disappears; only the diagonal ones (`pipeline` fan-in, `loop`, `pulse`) survive.

Measured in the live DOM (`getBBox().height === 0` on a `stroke="url(...)"` element):

| Page | Illustration | Invisible connectors |
|---|---|---|
| index.html | landing card 01 `mini_system` | `96,60 140,60` · `270,60 312,60` · `432,60 470,60` |
| index.html | landing card 02 `mini_loop` | `60,60 500,60` — the entire six-stage spine |
| the-system.html | `pipeline` ("what it does") | `144,100 200,100` · `350,100 392,100` · `542,100 584,100` |
| the-system.html | `servers` ("infrastructure") | `360,92 418,92` (the WireGuard link) · `588,92 630,92` |
| how-i-ship.html | `layers` ("keeping AI in scope") | 4 box-to-box wires + `M60,150 L698,150` (the "one read path" rule) |
| how-i-ship.html | `chain` ("skills and harnesses") | `142,100 190,100` · `190,100 682,100` — the whole 7-checkpoint spine |
| how-i-ship.html | `gate` ("where it stops") | `190,60 330,60` · `190,140 330,140` · `346,140 560,140` |

**19 connectors, 8 of the 9 custom illustrations.** Pixel-confirmed: sampling `rv9_s1_1440.png` across x=700–780 at
every y in the pipeline banner's wire band returns a uniform `(8,14,22)` — background, no stroke.

Consequence: the illustrations that are supposed to be *flows* render as floating boxes and orphan dots. That is the
single biggest reason a design reviewer would call them "generic" — the diagram's whole argument is the arrow, and the
arrow is missing.

**Fix (one line, fixes all 19):** in `banners.py:defs()` give the wire gradients user-space coordinates —
`<linearGradient id="{p}w" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">` (pass `W` into `defs`).
Cheap alternative if you do not want to thread `W`: nudge one endpoint by `0.01` in `wire()` so the bbox is non-degenerate.

---

# Persona 1 — Non-technical tech recruiter, Warsaw, phone, 15 s then 3 min, never clicks

## What I understand, page by page, visible layer only

**index.html — 15 s.** On a 390-wide phone the first screen ends around the two buttons. I get: a name, one claim
— *"One person built a live trading system, then the workflow that ships it."* — a four-line explanation, and a
disclaimer. **No number is above the fold.** The first stat (`16`) starts at ~810 px, the fold is 844 px. So in 15
seconds I have a claim and no evidence.
**At 3 min** I scroll and it lands: 16 months / 1,300 trades / 1.3 s / 112 runs, then two cards. This page works.

**the-system.html.** I understand: he built a trading thing that runs by itself on two servers, it is fast, it trades
his own money, there are hard limits it cannot break, and three things once broke and now cannot. I do not understand
what "Solana", "TimescaleDB" or "17 exit strategies" are, and I do not need to. The section that lands hardest with me
is *"The controls that exist because something broke"* — that is a person who learns, which is what I sell to a hiring
manager.

**how-i-ship.html.** Weakest of the three for me, and it is the one aimed at my audience. I get: he made a process, AI
writes code, three AI companies check it, he decides. Then I hit the ten-phase list and stop — it looks like a table of
contents for a manual. **76 % of this page's words are behind a click** (6,739 of 8,877, measured by parsing
`<details>`). I click nothing, so I see a quarter of it. On the-system.html that figure is 40 %; on index.html, 0 %.

## Ranked findings

**1 — On the phone, case study 2's cover has no picture at all, and a 130 px hole where it should be.**
Current: the six-stage ribbon `<div class="fig rv ribbon">` renders at **height 0** at 390 px wide, and its text
fallback `<ol class="ribbon-list">` computes to `display:none`.
Cause is CSS source order, not the media query. `theme.py:130` says
`@media (max-width:640px){ .ribbon svg{display:none} .ribbon-list{display:grid} }`
but `theme.py:421` — **later in the file, same specificity** — says `.ribbon-list{display:none;gap:.5rem;...}` and wins.
Fix: move the `@media` block below line 425, or raise specificity to `.ribbon > .ribbon-list{display:grid}`.
This is the first thing a phone reader sees on the page written for people who hire builders like him.

**2 — The strongest proof is below the phone fold on the landing page.**
Current: `stats=[("16","months, one architect"), ("1,300","confirmed trades, my own funds"), ("1.3 s","median trade execution"), ("112","documented delivery runs")]` renders as four full-width stacked rows starting at y≈810.
Fix: on ≤640 px render the stat strip as a 2×2 grid directly under the H1 and move the two buttons below it. Two
numbers above the fold is the difference between "another portfolio" and "wait, 1,300 real trades?".

**3 — Wall of text, one place only: the run-section lead on case study 2.**
Current (59 words, 6 lines on a phone): *"The six stages on the cover unfold into ten phases plus a final one, below,
in the order the runbook's own to-do list executes them for a complex change. Open a phase, then a step, to see who
acts, what they must read first, what evidence they leave, and what stops the run. Step numbers are the runbook's own."*
Fix: cut to two sentences — *"The six stages unfold into eleven phases and 62 steps. Open one to see who acts, what
they must read first, and what stops the run."* Move the rest into the "About the numbering" dropdown that is already
right there.
(Every other lead on the site is fine. The landing lead is 42 words / 2 sentences and reads cleanly.)

**4 — Nothing else is a wall.** Measured visible-word counts per section on case study 2: 33–220, median ~110. Case
study 1: all leads are 1–2 sentences, 9–39 words. The "no walls of text" intent is met except for finding 3.

## Strongest and weakest visible sentence

**Strongest:** *"The price provider caps a connection at 100 addresses. I needed 552."*
A constraint and a number, in fourteen words, no jargon. I understand the problem and that he solved it without knowing
what a "connection" is. This is the sentence I would quote in a forwarding email.

**Weakest:** *"371K implementation lines and 5,066 commits across three repositories were generated under the delivery
workflow. They measure the workflow's output, not me."*
It is honest to the point of self-harm. It is also the only place on either page where he volunteers a number and then
tells me not to count it. A hiring manager skimming reads "371K lines" and then "not me" and comes away unsure what he
actually did.
Fix: *"371K lines and 5,066 commits across three repositories came out of this workflow. My work is the architecture,
the acceptance criteria and the release decision behind them."* Same honesty, ends on what he owns.

*(Runner-up weakest, and a cheaper fix: `"62 / 112 runs claiming zero post-deploy bugs"` — "claiming" undercuts his own
ledger. Use "recording".)*

## Would I forward it?

Yes — after finding 1 is fixed, because I forward links people open on a phone.

One-line message I would send: *"Polish architect, remote — built and runs a live automated trading system on his own
money solo, then built the AI delivery process that ships it. 112 documented releases. Worth 10 minutes:
<link>/how-i-ship.html"*

---

# Persona 2 — Head of engineering, laptop, 10 minutes, clicks

## Does the visible layer make me open things, and is the payload worth it?

Yes on both counts, with one caveat.

The dropdown labels are the reason it works: *"How the transaction is built and hardened"*, *"How the feed is sharded"*,
*"The full map, box by box"*, *"Where the numbers come from"*. These are questions I already had. I opened seven of ten
on case study 1.

The payload is genuinely good. Behind *"How the transaction is built and hardened"*:
*"Solana gives a transaction 1,232 bytes, and a fresh pump.fun route does not fit. Seven constant venue accounts are
pre-warmed into the engine's own lookup table, appended and never prepended, because prepending re-inflates every
healthy route."* That is a real engineer's sentence — a hard limit, a fix, and the reason the naive fix is wrong. Same
quality in the step detail: step 0.A carries *"a stale brief is recoverable, but a quietly broken skill bundle
invalidates the audit itself. Added after a 47-day silent degradation nobody noticed."*

**Caveat:** the affordance is too quiet for a reader who is not already curious. `details.more > summary` is 13 px
mono uppercase in `--ink-3` (#7d8ba3, contrast 5.8:1 — legible but recessive), no border, no fill, a 22 px hairline
chevron. On the phone it reads as a caption, not a control. Fix: give the summary a 1 px `--line-2` border and pill
radius so it reads as a button; keep the type as is.

## Are the phases and steps credible and understandable?

Yes. **11 phase accordions, 62 step accordions** — matches the stated "ten phases plus a final one … 62 steps"
exactly, which is itself a small credibility win.

Each opened step gives me: an actor chip (`SCRIPT`, `CLAUDE SONNET`, `OPENAI CODEX`, `XAI GROK`, `ME`), a body, and a
right-hand rail labelled `STOPS THE RUN WHEN` / `EVIDENCE LEFT BEHIND` / what it must read first. That structure is
the thing that makes this readable as a process rather than a brag. The step IDs are the runbook's own (`0.A`, `2✓`,
`4.5`, `7B`), which reads as real rather than reconstructed.

The credibility peak is `Phase 4 · Five-way plan audit — "Three vendors in parallel · quorum three of four · then my
approval"`. Quorum, named vendors, a human at the end. I believe that.

## Claims I would challenge

**1 — `"78 / 92 runs where the external review found what internal reviews missed"`. This number argues against your
own panel.**
Read plainly: in 85 % of the runs where you recorded the field, five-to-seven internal AI reviews missed something a
single external round caught. That is the strongest evidence on the page that lane count is theatre — and the page
never addresses it. You even anticipate the theme (*"Lane count is not lane diversity"*) and then leave the number
naked one screen later.
Fix: add one sentence under it — *"That ratio is why the external round has no timeout and cannot be skipped. Internal
lanes catch a different class: X of them are blocked before a line is written."* Turn it from an indictment into the
reason the external round exists.

**2 — `149` sources vs `300+` sources, both in the visible layer, no reconciliation.**
`what` section: *"Listen · 149 · sources watched: 63 groups, 86 wallets, 4 chains"*.
`intelligence` cube, four screens later: *"300+ sources"*.
I noticed inside 10 minutes. Fix: label the cube *"300+ sources ever tracked"* or the card *"149 live sources"* — one
word each.

**3 — `12M rows` vs `12.3M rows` in the same page.**
`infra` (behind the dropdown): *"TimescaleDB · 28 GB · 12M rows"*. `measured` (visible): *"12.3M rows in TimescaleDB /
28 GB · 95 tables"*. On a page whose whole thesis is *"Measured, with the populations printed"*, a rounded duplicate of
a printed number is the wrong place to be sloppy. Fix: use 12.3M in both.

**4 — `8 shards live` for `552 contracts` at a `100 address` cap.**
552 / 100 = 6. You run 8. The reason (headroom, hysteresis, "the scaler acts on the busiest shard, not the average")
is in the dropdown, but the visible layer shows 8 next to 552 next to 100 and invites the arithmetic. Fix: make the
visible stat `"8 shards live · 6 required, 2 headroom"`.

**5 — `"Twenty-two skill packages"` — the site's own source list has 21.**
`s2_v6.py:SKILLS` contains 21 entries. Not visible to a reader, so it costs nothing today, but it is the one number on
the page I could falsify from the artefact itself. Fix: recount, or derive the figure from `len(SKILLS)` at build time
so it cannot drift.

**6 — The boundary is promised and never delivered on case study 1.**
Current, on both close sections: *"And I will tell you where the boundary is: the changes I would not make this way,
and who I would bring in instead."*
Case study 2 pays it off once, in small type: *"Multiple AI reviewers are not an independent security audit; where
money or security is at stake, the boundary is a human specialist."* Case study 1 pays it off **not at all** — it makes
the promise and moves straight to the contact block. A sentence that promises candour and then withholds it costs more
than saying nothing.
Fix: on case study 1, replace the promise with the answer — *"Where I would not use this: a change to key custody or
withdrawal authority. That gets a human specialist and a formal audit, not a review panel."* One concrete refusal is
worth more than the offer to discuss refusals.

## Inconsistencies between sections and between the two case studies

**7 — The landing card for case study 2 describes a page that no longer exists.**
Landing (`content.py:LANDING`): *"Six stages. Five model reviews on every plan, up to seven on every code change, then
a separately run review. Gates that stop the run. A memory loop that turns failures into rules: 112 runs, 235 recorded
gaps, and the controls they produced."* — with tiles `112 documented runs` / `3 AI vendors on every review`.
The actual cover (`s2_v6.py`): *"One AI coordinates the job. Specialist agents research, plan, implement and test it…"*
— with tiles `112` / `3` / `4 days`.
`build_site.py:7` sets `C.S2 = s2_v6.S2`, so the old `content.py:S2` block is dead code, but `LANDING` still ships the
old pitch. Neither the "five/seven reviews" framing nor "235 gaps" is what the page now leads with.
Fix: rewrite the landing card 02 text against `s2_v6`, and delete the dead `content.py:S2` so the next editor does not
update the wrong file.

**8 — The same six stages are named differently in three places.**
Landing card graphic: `UNDERSTAND · ROUTE · PLAN · BUILD · REVIEW · DECIDE`.
Case study 2 cover ribbon: `Understand · Route · Research and plan · Approve, then build · Review · Decide and verify`.
Run section phase titles: `Understand and route` (one phase, not two) · `Research` · `Plan and validate` · …
Fix: pick one canonical set of six labels and use it verbatim in all three.

**9 — Case study 2's leads are twice as long as case study 1's.**
Case study 1: every lead is 1–2 sentences (max 39 words). Case study 2: **6 of 14 leads run 3–4 sentences** — cover
(4 sent / 45 w), `grew` (4 / 62), `scope` (3 / 47), `run` (3 / 59), `machinery` (3 / 42), `gaps` (3 / 39).
The stated intent is "a one- or two-sentence description". Case study 1 obeys it, case study 2 does not, and the two
pages read as different products.
Fix: cut each of those six to two sentences; the third sentence is usually the one that belongs in the dropdown.

**10 — Failure-card date formats disagree inside one row.**
Case study 2 `failures`: card 1 `RUN 31 · APR 2026`, card 3 `RUN 108 · JUL 2026`, card 2 `4 JUN · 2026` — no run
number, and a day where the others have none.
Fix: `OPERATOR-CAUGHT · JUN 2026` for card 2, so the row reads as one system.

## Oversold / undersold

**Undersold — `"1,245 test functions in the engine"` and `"119 on-chain program tests · 46 unit + 73 mainnet-fork"`.**
These are buried as tertiary metrics. "73 mainnet-fork tests" is the single most credible engineering artefact on
either page — it says he tests against real chain state, not mocks. Promote it into the `engine` visible layer.

**Undersold — the memory loop.** *"Whatever breaks once becomes a rule the next time"* with `G-127a` traced from found
→ recorded → designed → proven → retired is the most transferable thing here for a team, and it sits ninth on the page.

**Oversold — `"Six stages. I own scope, release and verification."` set against 62 steps and 34 gates.**
Not false, but the visible layer sells simplicity and the dropdown reveals a 11,009-line runbook. A reader who opens
it feels the mismatch. Fix: say the real thing on the surface — *"Six stages a person can hold in their head. Eleven
phases and 62 steps a script executes."*

**Oversold — `"Two Hetzner servers"` in an H1.** The headline spends its most valuable words on a hosting vendor. The
sentence that follows (*"Analysis is heavy and chatty; execution has to be fast and quiet"*) is the actual insight.
Fix: `"Two servers, one encrypted tunnel, and the Solana blockchain"` — and see the leak-check note below.

---

# Persona 3 — Design and readability

## Visible-element count per section, before any click

Counted in the live DOM: kicker, headline, lead, visual, each card / stat / key block, each note, each `<summary>`.
Threshold flagged at >12.

**the-system.html — no section exceeds 12.**

| Section | Count | Composition |
|---|---|---|
| cover | 3 | kicker, h1, lead |
| cover body | 5 | 3 stats, summary, screenshot |
| journey | 5 | kicker, h1, lead, chart+caption, summary |
| what | 9 | + banner, 4 cards |
| infra | 5 | + banner |
| engine | 8 | + stage chart, 3 stats |
| data | 7 | + 3 stats (**no illustration** — see below) |
| controls | 8 | + 2 key cards, 3 stats |
| intelligence | 8 | + cube, 3 stats |
| failures | 7 | + 3 cards |
| **measured** | **10** | + 6 tiles |
| close | 8 | + banner, 2 cards, note, next-card |

**how-i-ship.html — one section over 12.**

| Section | Count | |
|---|---|---|
| cover | 3 | |
| cover body | 4 | ribbon is height-0 on phone (P1 finding 1) |
| grew | 5 | |
| scope | 8 | |
| **run** | **18** ⚠ | kicker, h1, lead, expand-all, **11 phase summaries**, 3 stats, summary |
| reviewers | 7 | **no illustration** — 7 lane chips + 3 stats only |
| skills | 8 | |
| machinery | 8 | |
| failures | 7 | |
| scorecards | 8 | |
| **gaps** | **4** | kicker, h1, lead, summary — **no illustration counted; the bar trio is the only visual** |
| gates | 10 | |
| economics | 8 | |
| measured | 10 | |
| close | 9 | |

**Flagged: `run` at 18.** It is an index, so the count is defensible, but it is also the section where a first-time
reader stalls. Fix: group the eleven rows under three visible bands — `Before the code (Phases 0–3)`, `The panel
(Phases 4–6)`, `Shipping it (Phases 7–Final)` — three headers, eleven rows, and the eye gets a hierarchy instead of a
list.

## Each custom illustration, judged

Consistent language across all nine: dotted field, radial glow, hairline rounded cards with a coloured top rule,
cyan/violet/green tokens, mono micro-labels. **They do read as one custom family, not stock.** That is the good news.
Every problem below is a fixable execution defect, not a direction problem.

**`mini_system` — landing card 01.** Custom ✓. Legible at desktop; at 64 px tall on a phone the 9.5 px mono sub-labels
(`Python · Rust`, `~1.3 s`, `capped`) are at the edge of readable. **3 connectors invisible** (root cause above), so
"signals → two servers → engine → Solana" renders as four unconnected boxes.

**`mini_loop` — landing card 02.** Custom ✓. **The entire spine `60,60 → 500,60` is invisible**, so six labelled dots
float with nothing joining them. This is the worse of the two cards, and it is the one selling the AI-delivery story.

**`pipeline` — "what it does".** The best composition on the site. Two defects:
- **Text escapes its card.** Measured `getBBox()` against the parent `<rect>`: `"8 workers · 17 strategies"` overflows
  its 150-wide card by **+6.5 px**; `"~1.3 s to a landed trade"` by **+0.8 px**.
- **3 connectors invisible**, so the fan-in renders (diagonal) but the three stage boxes do not connect.
Fix: widen the two boxes to 168 (`box(p,200,66,168,...)`, `box(p,392,66,168,...)`) or drop the sub-label to 9 px, plus
the gradient fix.

**`servers` — "infrastructure". The worst-looking element on the site.** Three overlapping defects in one 120 px band:
- **`"Python · TimescaleDB · dashboard"` overflows its 170-wide card by +26.4 px** — the word *dashboard* sits
  entirely **outside** the "Finland · the brain" card, floating in the gap.
- **`"Rust engine · signed signals"` overflows by +3.6 px** — the final `s` of *signals* is clipped by the Nuremberg
  card's right border.
- **The `WIREGUARD` label collides** with both: its final `D` is clipped by the Nuremberg card, and it sits directly
  against the escaped *dashboard*. Verified at 3× zoom in `s1_wg_zoom2.png`.
- **Both connectors invisible**, so the WireGuard tunnel — the point of the diagram — has no line.
Fix: shorten to `"Python · TimescaleDB"` and `"Rust · signed signals"`, widen both cards to 190, move the boxes to
`x=180` / `x=440`, raise the WireGuard label to `y=70`.

**`layers` — "keeping AI in scope".** Custom ✓, five boxes read cleanly. Defects:
- **`"same-change updates"` overflows the "Three contracts" card by +4.3 px.**
- **All four box-to-box wires invisible**, and **the `M60,150 L698,150` rule is invisible** — so the purple and green
  dots at either end read as **two orphan dots** with a caption stranded between them. This is the clearest "looks
  unfinished" moment on the site.
Fix: gradient fix restores the rule and the four wires at once; widen box 4 to 132.

**`chain` — "skills and harnesses".** Custom ✓, the bracket groups are a nice touch. Defects:
- **`"official vendor docs"` overflows the "A skill" card by +10 px.**
- **The 7-node spine is invisible**, so seven glowing dots float unconnected — the "chain" in the name is absent.
- The `1`–`7` numerals are 8 px, `font-weight:600`, `#05080f` on a blurred cyan dot. Smallest and least legible type
  on the site. Fix: 9 px and drop the blur behind the numeral.

**`gate` — "where it stops".** Custom ✓. Defects:
- **All three connectors invisible**, so both lanes are chips and bars with nothing between them; the "claim → gate →
  blocked / passes" story does not read.
- **The `34 gates / 146 hard blocks` card is 112 px tall with two lines of text at the top** — ~60 px of dead space
  inside an orphan card at the right edge. Fix: shrink to `h=56` and centre it on the lanes, or add a third line.

**`loop` — "one machinery".** ✅ **The best illustration on the site.** The circle renders (varying `y`), the five
command names are placed by angle, the centre carries the payload, and both side annotations earn their space.
No defects. This is the reference the others should match.

**`pulse` — both close sections.** ✅ Renders correctly (varying `y`). Clean, restrained, on-language.

## Overlapping text, clipped labels

- **Clipped:** `WIREGUARD`'s final `D`, and `signals`' final `s`, both against the Nuremberg card
  (`the-system.html`, infrastructure).
- **Escaped:** `dashboard` sits fully outside its card (same illustration). This is the one a designer will see first.
- **Six SVG sub-labels overflow their parent card**, measured: +26.4, +10.0, +6.5, +4.3, +3.6, +0.8 px.
- **No text–text pixel overlap** anywhere else; an exhaustive pairwise `getBBox()` intersection over every `<text>` in
  every SVG on all three pages returned zero collisions.
- **No page-level horizontal scroll** at 390 px on any of the three pages (`scrollWidth === innerWidth === 390`).

## Unused space — content narrower than its container

**Opened dropdowns waste up to half the width.** Measured as (rightmost text edge − container left) / container width,
at 1440 px, container = 1120 px:

*the-system.html — 7 of 10 dropdowns under 63 %:*
`Populations and dates` **51 %** · `Where the numbers come from` **51 %** · `How the transaction is built and hardened`
**55 %** · `How the replay works` **55 %** · `See it on the dashboard` **62 %** · `How the feed is sharded` **62 %** ·
`In their own words` **62 %**.
(Good: `How the program enforces it` 100 %, `The milestones` 99 %, `The full map, box by box` 98 %.)

*how-i-ship.html — 4 of 13 under 56 %:*
`Populations and dates` **51 %** · `Where the numbers come from` **51 %** · `About the numbering` **51 %** ·
`How the cost is controlled` **55 %**.

The design intent says opened content should use the full width. Fix: the `points`-style dropdowns already run
two-column at 98–100 %; route the prose-only ones (`.fn`, note lists) through the same grid instead of a single
`max-width` column.

**8 of the 62 opened steps leave the entire right rail empty** — roughly 40 % of the row. Named:
`1 Read the request` · `1.6 Is there a screen involved?` · `4.5 Pick the external bug-hunter's depth` ·
`5.1 Four mandatory preambles` · `6.2 Skills gates` · `7.1 Functional testing requirement` (+2).
These steps carry no `block` / `leaves` / `reads` value, so the rail renders empty.
Fix: when a step has none of the three, collapse the row to a single full-width column.

**Captions are pinned to a narrow column under full-width figures.** Three cases, all producing an orphaned last word
with 500+ px of empty space beside it:
- `journey` (case study 1): *"Commits per month, from git across the three repositories · Apr 2025 to Sep 2026"* —
  `2026` alone on line 2, chart is 630 px wide, caption ~310 px.
- `grew` (case study 2): *"Lines in the workflow file, from git · growth is rules added after failures, not features"*
  — `features` orphaned.
- `economics`: *"Token use per review as a share of the pre-routing control run, which consumed about 13.4 million
  tokens. From the routing A/B recorded in the repository."*
Fix: let `.cap` inherit the figure's width instead of the text measure.

**The boundary block, both close sections.** Current render: the `— THE BOUNDARY` label sits inline, the sentence
starts beside it, then wraps *under* the label, and the right ~40 % of the container is empty:
*"And I will tell you where the boundary is: the changes I would not make this way, / and who I would bring in
instead."* It reads as a layout accident. Fix: stack the label above the sentence and let the sentence run the full
measure.

## Orphan cards

- **`scorecards` (case study 2): three metrics in a 2 + 1 L-shape.** `121` and `5` sit on row 1, `30 · data-flow
  passes` sits alone on row 2 with the whole right half empty. Every other metric strip on both pages is a clean
  3-across. Fix: force 3-across, or move `30` into the scorecard panel.
- **`gates` (case study 2): a 2-column metric strip** (`34 catalogued gates`, `146 hard-block instructions`) where
  every other section uses 3. Reads as a missing third column. Fix: add `62 steps gated` or set an explicit 2-col grid
  with a shorter measure.
- **`34 gates / 146 hard blocks` card** inside the gate banner — see above, ~60 px of dead interior.
- **`Data-flow tracer` lane chip** (`reviewers`, case study 2) is the only one of seven whose title wraps to two lines,
  pushing its body down and breaking the row's baseline. Fix: `Data-flow` on one line, `tracer` as the sub-label.
- **`failures` cards (case study 1) do not share a baseline.** Card 1 renders its number stacked (`7,150` above
  `cells checked before a parser change`); cards 2 and 3 render inline (`3.02×  the error the gate now refuses`).
  Bottom edges land ~20 px apart. Fix: one layout for all three.
- **`controls` key cards (case study 1)**: the left card ends in white space where the right card ends in
  `CANNOT WITHDRAW · EVER`. Fix: add the matching red line `CAN MOVE FUNDS` / or pad both to equal height.

## Sections with no custom visual

Design intent is headline + description + **one** custom visual + dropdown. Three sections have no illustration —
only a number strip, which is the weakest of the four permitted visual types and is already used everywhere else:

- **`data` — "The price provider caps a connection at 100 addresses. I needed 552."** The best headline on the site
  has nothing next to it. It is asking for a shard-placement diagram: 552 dots, 8 rings, one dot moving on a restart
  and landing in the same ring.
- **`reviewers` (case study 2)** — 7 lane chips + 3 stats. The lane matrix behind the dropdown is the visual; nothing
  of it surfaces.
- **`gaps` (case study 2)** — three bars. Adequate, but visually the thinnest section on either page.

## Phone

- **No horizontal page scroll** on any page. ✓
- **The case study 2 cover ribbon renders at height 0** — the CSS-order bug in P1 finding 1. Highest-priority phone fix.
- **Wide illustrations are cut at the right edge.** `.banner` becomes `overflow-x:auto` under 640 px with
  `svg{min-width:560px}` and an 88 % mask fade; `.fig` (the two charts) becomes `overflow-x:auto` with
  `svg{min-width:600px}` and **no fade at all**. Result at 390 px:
  - `journey` commits chart: the entire 2026 half — including the peak month and the tail — is off-screen, with **no
    visual hint** that it scrolls.
  - `infra` illustration: `Nuremberg · the hands` is cut mid-word to `N`, and `EXECUTION, FAST AND QUIET` to `EXE`.
  Fix: apply the same mask fade to `.fig`, and add a one-line `swipe →` hint under both. Better: give `servers`,
  `layers` and `chain` a stacked ≤400 px viewBox variant for phones — they are the three that lose the most.
- **Type under 14 px — eight distinct tiers, smallest 10.56 px.** Measured on `how-i-ship.html` at 390 px:

| Size | Where | Instances |
|---|---|---|
| **10.56 px** | `my decision` on the cover ribbon | 3 |
| **11.2 px** | actor tags — `script`, `Claude Sonnet`, `Me`, `OpenAI Codex`, `xAI Grok` | 83 |
| 12 px | `3 steps` pills · `What broke` labels · `Run 31 · Apr 2026` | 41 |
| 12.8 px | reviewer lane descriptions · scorecard values `11 / 12` | 14 |
| 13 px | kickers, step IDs, milestone dates, summaries | ~140 |
| 13.12 px | code pane, skill chips, status chips | ~46 |

  Contrast is **not** a problem anywhere — the weakest token (`--ink-3` #7d8ba3) is 5.8:1 on the page background and
  5.4:1 on cards, all above AA. The problem is size alone. Fix: raise the 10.56 px and 11.2 px tiers to 12 px minimum
  under 640 px — that is 86 elements, all of them labels a reader actually needs (who acted, on which step).
- **Illustration micro-labels stay at 9.5 px and 8.5 px inside the SVGs on a phone** (they do not scale up, since the
  SVG keeps its 560/720 min-width). Effectively unreadable on the move.

## Dropdown affordance

- Descriptive, specific labels — the strongest thing about the pattern. ✓
- The `Expand every phase and step` bulk control on case study 2 works and relabels itself to `Collapse all`. ✓
- `beforeprint` opens every `<details>` — a genuinely thoughtful touch for a recruiter who prints to PDF. ✓
- **Too quiet visually** (see P2). 13 px mono uppercase in `--ink-3`, no border, no fill, hairline chevron.
- **`.rv` reveal risk:** `.js .rv{opacity:0}` with an `IntersectionObserver` at `threshold:0.12` and
  `rootMargin:'0px 0px -10% 0px'`. Any `.rv` element taller than ~6,300 px on a 390 px phone can never reach 12 %
  visibility and would stay invisible. Nothing hits that today, but it is one long section away. Fix: add
  `threshold:[0,0.12]` so the observer also fires on first intersection.

---

# Leak check

**Clean:** no IPv4 addresses, no hostnames, no domains, no SSH paths or `root@`, no `id_rsa`, no database name or user,
no password / API key / token / bearer strings, on any of the three pages. Verified by regex over the full rendered
text including all `<details>` content.

**Investor / fund / client wording — clean and correctly used.** The only hits are the disclaimers themselves:
*"It trades only my own funds: no client assets, no investment service, no advice."* and *"The system this workflow
ships trades only my own funds: no client assets, no investment service, no advice."* No "investor", no third-party
capital framing, no returns claim. `"Signal subscriber · verify, dedupe, fan out"` is a component name, not a person.
`"Fund-moving code must have run, on a mainnet fork, in this run"` is a code classification. Both fine.

**Findings:**

**L1 — `NELLAI` in the footer of all three pages, unexplained.**
Current: `[ADD LINKEDIN / EMAIL] · Poland · remote · NELLAI · 2026`, hardcoded at `build_site.py:560`.
It sits in the slot a company or brand occupies, is defined nowhere on the site, and is not the candidate's name. A
reader will read it as an employer or a client. Under the stated rule (no real third parties beyond the candidate and
named AI vendors) it is the one string that has no defence.
Fix: delete it, or define it once — if it is his own entity, `Lukasz Rodzen · Poland · remote · 2026` is cleaner.

**L2 — Infrastructure fingerprint: hosting vendor + both datacentre cities + VPN protocol.**
Current, in an **H1**: *"Two Hetzner servers, one encrypted tunnel, and the Solana blockchain"*, plus, behind the
`infra` dropdown, *"Finland · Hetzner · the brain"*, *"Nuremberg · Hetzner · the hands"*,
*"My servers · WireGuard tunnel between them"*, and a dashboard screenshot captioned *"Service status · Finland host
vitals"* showing a `WIREGUARD VPN` service row.
Individually harmless; together they name the provider, both regions and the tunnel protocol of a machine that holds a
trading key. Nothing here lets anyone reach the host, but it is more than the story needs.
Fix: drop `Hetzner` from the H1 (*"Two servers, one encrypted tunnel, and the Solana blockchain"*), keep
`Finland` / `Nuremberg` as the latency story, and drop `Hetzner` and `WireGuard` from the detail — *"an encrypted
tunnel"* carries the same meaning.

**L3 — Named non-AI third parties (informational, judged as acceptable).**
`the-system.html`: Birdeye, Helius, Jupiter, Nansen, DefiLlama, CoinGecko, CoinMarketCap, Telegram, Solana,
TimescaleDB, Anchor, pump.fun, Phantom, Hetzner.
`how-i-ship.html`: Solana Foundation, Helius, Jupiter, Raydium, Orca, Meteora, Squads, Phantom, PumpFun, Postgres,
Birdeye, Anchor, GitHub.
These are the technology stack of the thing being described, and an engineering case study that hid them would be
worthless. **Recommend keeping all of them except `Hetzner` (L2)** — the hosting vendor is the only one that is
infrastructure rather than architecture.
The one that reveals a commercial detail rather than a technical one:
*"The price provider caps a connection at 100 addresses"* immediately after *"Birdeye price WebSocket"* discloses a
specific paid vendor's plan limit. Low risk, and it is also the best headline on the site. Keep.

**L4 — AI vendors named: Claude / Anthropic, OpenAI Codex, xAI Grok, Google (retired lane).** All within the stated
allowance. The commercial detail — *"One Claude Max subscription, one ChatGPT plan for Codex, one thirty-dollar Grok
plan"* — is his own spend, not a third party's, and it is one of the most persuasive lines on the page. Keep.

---

# Top 10 changes

1. **Fix the SVG wire gradients** — `banners.py:defs()`, add `gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0"`. Restores **19 invisible connectors across 8 of 9 illustrations**. One line; the largest visual gain available.
2. **Fix the phone ribbon** — move `theme.py:130`'s media block below line 425 (or use `.ribbon > .ribbon-list`). Case study 2's cover currently has **no visual and a 130 px hole** on every phone.
3. **Fix the six SVG text overflows**, worst first: `"Python · TimescaleDB · dashboard"` (+26.4 px, the word *dashboard* floats outside its card), `"official vendor docs"` (+10), `"8 workers · 17 strategies"` (+6.5), `"same-change updates"` (+4.3), `"Rust engine · signed signals"` (+3.6), `"~1.3 s to a landed trade"` (+0.8). Shorten the label or widen the card; also raise the `WIREGUARD` label off the Nuremberg border.
4. **Delete or define `NELLAI`** in the footer (`build_site.py:560`) — the only unexplained third-party string on the site.
5. **Give the phone two numbers above the fold** — 2×2 stat grid under the landing H1, buttons below it. Today the first stat starts at 810 px against an 844 px fold.
6. **Make opened dropdowns use the full width** — 7 of 10 on case study 1 and 4 of 13 on case study 2 render at 51–62 %; collapse the empty right rail on the 8 steps that have no `block` / `leaves` / `reads`.
7. **Rewrite the landing card for case study 2** against `s2_v6.py` (it still sells the retired *"Five model reviews… 235 recorded gaps"* page), and delete the dead `content.py:S2`.
8. **Answer `78 / 92`** with one sentence, and **deliver the boundary on case study 1** instead of only promising it. These are the two claims a head of engineering will press on.
9. **Phone type floor of 12 px** — raise the 10.56 px `my decision` ribbon labels and the 11.2 px actor tags (86 elements). Contrast is fine; size is not.
10. **Reconcile the four number conflicts** — `149` vs `300+` sources, `12M` vs `12.3M` rows, `8 shards` vs `552/100`, `"Twenty-two skill packages"` vs 21 in `s2_v6.py:SKILLS`. On a site whose thesis is *"Measured, with the populations printed"*, these are the cheapest credibility points on the board.

---

# Verdict

**SHIP AFTER FIXES** — the writing, the structure and the evidence are interview-grade, but two rendering defects (19 dead connectors in the custom illustrations; the phone cover of case study 2 rendering empty) and one unexplained footer string mean it should not go out as it stands.
