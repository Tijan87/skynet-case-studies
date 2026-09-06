# Visual approval pass

Final QA and polish before the site goes public. Measured at **1440** and **390** on all three
pages, every dropdown opened at least once (86 disclosures on `how-i-ship`, 10 on `the-system`,
1 on `index`). Only `src/theme.py`, `src/banners.py` and `src/build_site.py` were edited; the
generated HTML was rebuilt with `./build.sh`. No copy and no number was changed.

---

## What I changed

### Bugs that were breaking the render

| # | File | Change | Why |
|---|------|--------|-----|
| 1 | `build_site.py` · `fig_stages` | `opacity=.55` → `opacity="0.55"` | The unquoted attribute swallowed the closing `/`, so the following `<text>` became a child of `<rect>` and **the "292 ms" label never rendered**. The bottom row of the latency chart was a bar with no value. |
| 2 | `theme.py` ×4, `build_site.py` ×2 | `clamp(2rem,1.5vw+1.5rem,…)` → `clamp(2rem,1.5vw + 1.5rem,…)` | CSS math requires whitespace around `+`. Six declarations were silently dropped: `.tile .n` fell back to 17px body sans (tile numbers were smaller than their own labels), `.metrics .stat .n` and the four-up card numbers inflated to 56px, `.quote` lost its display size, `.pick h2` rendered at 40px instead of 32px. Fixing them restores the intended number hierarchy across every section. |
| 3 | `theme.py` · `.glow` | added `transform:translate(-50%,0)` | The centring transform only existed inside the `drift` keyframes, so the hero glow sat 156px off-centre for the first 1.5s — and permanently under `prefers-reduced-motion`, pushing `documentElement.scrollWidth` to 546 at a 390 viewport. Now 390/390 in both motion modes. |
| 4 | `theme.py` + `build_site.py` · new `.figs-x` wrapper | the phone fade mask moved from `.fig` onto an inner scroll band | The 88% fade mask was applied to the whole figure, so on phones it **faded out the legend and the caption** as well as the chart ("Execution engine · Rus…", "…Sep 2026"). Now only the scrolling chart band fades. |

### Alignment and rhythm

| # | File | Change | Rule |
|---|------|--------|------|
| 5 | `theme.py` · `.acc .in` | left padding `3.2rem` → `4.2rem` | Step body text started 16px to the left of the step title it belonged to. Both now sit on the same edge (measured: title 227, body 227). |
| 6 | `theme.py` · `.acc .in dl` | `align-content:start` | Auto rows were stretching to the height of the prose column, so a single "STOPS THE RUN WHEN" label sat ~45px above its value. Now the natural 7px gap. Affects all 62 steps. |
| 7 | `theme.py` · `.gate` | `align-content:start` + `.gate .claim{min-block-size:2.8em}` | Gate card rows were distributed over the stretched card height and one-line claims pushed the labels out of line. All four rows now align across every card in a row (measured identical tops ×3). |
| 8 | `theme.py` · `.cards.c4 .stat .l` | `min-block-size:2.7em` | Four-up card paragraphs started at different heights because one sub-label wrapped to two lines. Baselines now share a row. |
| 9 | `theme.py` · `.flow .fx:nth-child(1):nth-last-child(5) h3` | `min-block-size:2.5em` | Quantity query, so the reserve applies only to the five-up flow where one title wraps. The three-up and six-up flows are untouched. |
| 10 | `theme.py` · `.tl` ≥900px | per-item rail replaces the single container rail | Both timelines have 8 milestones → two rows of four, and **the second row had no connecting line at all**. Each cell now draws its own rail through the gap; `:nth-child(4n)` stops at the row end. |
| 11 | `theme.py` · `.note` | `max-inline-size:none` + `padding-right:max(0px,100% - 68ch)` | The hairline above a note was as narrow as its 68ch text, so section rules came in two different widths within 300px of each other. The rule is now full width; the text is still 68ch. |
| 12 | `theme.py` · `.rules` | flex-wrap → `grid` (auto-fit, 17rem) | Six programme rules wrapped 5 + 1, leaving one orphan on a second row. Now a balanced 3×2. |
| 13 | `theme.py` · `.key .no` | `margin-top:auto` restored | A later duplicate rule had killed it, so "cannot withdraw · ever" floated mid-card and both key cards carried hollow bottoms. It is a card floor again. |
| 14 | `theme.py` · `.pick .card > p` | `flex:1 1 auto` | The two landing cards' number strips and arrows sat 28px apart because one description is a line longer. Now measured identical (nums 1822, arrow 1891 on both). |
| 15 | `banners.py` · `layers()` | row centred (`x = 37 + i*132`), baseline rule and caption re-centred, composition raised 10 units | The five boxes had a 93px left margin against a 21px right margin. |

### Illustrations (`banners.py`)

| # | Banner | Change |
|---|--------|--------|
| 16 | `pipeline()` | Removed the green terminus dot that sat exactly on the Solana box's right border and read as a blemish. No other banner ends in a loose dot. |
| 17 | `loop()` | The dashed "memory reset" wire stopped 22 units short of the ring — **a visibly disconnected wire**. It now lands on the circle. The two facing annotations (`memory reset` / `2-day runs`) were 10 units apart vertically; they now share a baseline, as do their sub-labels. |
| 18 | `gate()` | The whole left composition moved 20 units left. The red "diff shows zero changes · hard block" caption was ending 13 units from the "34 gates" panel and the green terminus dot 20 units from it; the gutter is now 44px and 62px respectively. |

### Charts (`build_site.py`)

| # | Change |
|---|--------|
| 19 | `fig_stages` bar width `W-lx-70` → `W-lx-20`; `fig_routing` `bw 320 → 380`. Both charts stopped ~110px short of the figure's right edge. |
| 20 | `fig_journey` `L 36 → 28`, `fig_growth` `L 44 → 30`. The y-axis labels sat 15–27px inside the heading's left edge. |
| 21 | `theme.py`: `.pane + .cap` joined `.fig .cap, .shot + .cap` — artefact-pane captions were capped at 60ch while every other figure caption spanned the figure. |

Flag labels on `fig_growth` were checked for collision at 1440 (six flags on three staggered rows,
no overlap); axis labels on every chart render ≥12.4px effective.

### Phones

| # | Change | Rule |
|---|--------|------|
| 22 | `details.phase-acc > summary` ≤640px rebuilt on an explicit grid | The chevron was landing on a third row next to the step-count pill. It is now top-right on row 1, owner on row 2, count on row 3. |
| 23 | `.banner.mini{display:none}` ≤640px | At 300px the landing thumbnails rendered their labels at **4.6px** — a smudge, not a diagram. See "left deliberately" below. |
| 24 | `.lanes-strip .ln:last-child{grid-column:1/-1}` ≤640px | Seven lanes in a two-up grid left "Me" alone on a fourth row. It now takes the full row. |
| 25 | `.matrix{min-width:46rem}` ≤900px | The four-column reviewer table squeezed to ~15ch columns. Now ~24ch and scrolls, like the other wide artefacts. |
| 26 | End-of-sheet `@media (max-width:480px)` type floor for `.acc .in dt`, `.matrix th`, `.ribbon-list li b` | These were 10.5–11.5px. Placed at the end of the sheet because an earlier block lost the cascade to later rules. HTML text is now ≥12px everywhere on a phone (verified programmatically). |
| 27 | `.hero` top padding `clamp(5rem,…)` → `clamp(3.25rem,…)` | Pulls the proof numbers into the first phone screen: headline ends 301, description 503, boundary line 587, first two numbers 619–711. |
| 28 | Touch targets → 44px: `.tabs a`, `.expand-all`, `details.more > summary`, `.brand` | Were 40px / 13px. `.brand` uses `inline-block` + `padding-block` so the " · case studies" space is preserved. |

### Disclosure bodies

| # | Change |
|---|--------|
| 29 | `details.more .inner .fn`: dropped `column-count:2`, set `max-inline-size:74ch`. Two columns were splitting footnotes mid-phrase — "…a sell circuit / breaker at three retries", "…enough to enable a route, not / to certify it" — with a one-line second column. |
| 30 | `details.more .inner.two > .points{grid-template-columns:minmax(0,1fr)}`. Inside a two-column disclosure the prose was being split again into ~30ch columns (the gaps section). Now one 62ch column beside the artefact pane. |

Verified: every disclosure body starts at the container's left edge (160) and uses the full
1120 except `.fn` (592 by design) and the deliberate two-column splits (544 + 544).

---

## What I verified

Rendered locally over HTTP with Playwright (Chromium), `.rv` reveals forced on and every
`<details>` opened. Screenshots taken per section rather than as one 14,000px page so type and
hairlines stay measurable.

**1440 — full page + every section**

- `index_1440_full`, `index_1440_00_s0`, `_01_s1`, `_02_s2`
- `the-system_1440_full`, plus `00_cover`, `01_s1`, `02_journey`, `03_what`, `04_infra`,
  `05_engine`, `06_data`, `07_controls`, `08_intelligence`, `09_failures`, `10_measured`, `11_close`
- `how-i-ship_1440_full`, plus `00_cover`, `01_s1`, `02_grew`, `03_scope`, `04_run`,
  `05_reviewers`, `06_skills`, `07_machinery`, `08_failures`, `09_scorecards`, `10_gaps`,
  `11_gates`, `12_economics`, `13_measured`, `14_close`

**390 — full page + every section (same section list for all three pages)**

**Element close-ups at 1440**: `gate`, `loop`, `chain`, `layers`, `pulse` banners; the gates card
row; phase 0 and phase 3 of the run section; the routing chart; the gaps disclosure.

**Element close-ups at 390**: the landing mini banners and card; the pipeline and shards banners;
the stages and journey figures; phase 0 open; the lanes strip; the reviewer matrix; the gates row.

**Programmatic checks**

- Every CSS declaration in `theme.py` re-validated with `CSS.supports()` — zero invalid
  declarations remain (six were being dropped before).
- Horizontal overflow at 390 on all three pages, in both `prefers-reduced-motion` states:
  `scrollWidth` 390 = `clientWidth` 390, no non-scrollable element past the viewport.
- Console and page errors after clicking every "Expand every phase and step" button and every
  "Read more" summary, at 1440 and 390, all three pages: clean.
- Interactive elements under 44px: none except the off-screen skip link.
- HTML text under 12px at 390: none.
- Effective SVG label size at 1440 across all banners and figures: minimum 12.4px.

---

## What I left deliberately

- **Landing mini illustrations are hidden below 640px.** At a 300px card width their labels
  render at 4.6px; scrolling them sideways instead would truncate a five-node diagram inside a
  preview card. Hiding them is the honest call — the cards lead with label, title and numbers,
  and the illustrations return in full at 641px and above.
- **Banners still scroll sideways with a right fade on phones** (`min-width:560px`). You accepted
  this; I confirmed nothing is cut mid-word at the *left* edge on any of them — every banner
  starts flush with its first chip or box.
- **The `.tiles` sub-notes do not share a baseline across a row.** The number and the label do;
  the tertiary note follows its own label, which is one, two or three lines depending on the tile.
  Reserving three lines everywhere would put ~44px of void into four of six tiles. Not worth it.
- **The funnel stays at `max-width:44rem`.** Stretching three 10px bars to 1120px would make them
  hairlines. The space to their right is intentional.
- **The on-chain node grid keeps equal card heights**, so the two-item "Solana mainnet" card has
  space at the bottom. It reads as a diagram cell; letting it collapse would leave the grid ragged.
- **`fig_cube` is inset from the left edge.** It is a drawing, not a plotted axis, and its caption
  and the section heading share the edge.
- **"In their own words"** is the disclosure label on the-system's failures section when there are
  no extra cards to show, so it opens onto a one-sentence note. That is a wording question, and
  wording is frozen — flagging it rather than changing it.
- **`src/content.py`** carries one uncommitted change from before this pass (`CONTACT_HTML`
  emptied). I did not touch it, `s2_v6.py` or `s2_run.py`.

No screenshots were written into the repository; `git status` shows only the four edited sources,
the three regenerated pages and the two tracked `__pycache__` files that `build.sh` rewrites.

VISUALLY APPROVED
