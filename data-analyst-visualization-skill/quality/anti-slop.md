# Anti-slop — mapping the Anti-Slop Rulebook onto this skill

Source: **miqdadbadjuber/anti-slop** (MIT License), vendored in full at
`assets/anti-slop/` — **v3.2.28** (upstream commit `4520786`, synced
2026-11-12). The vendored copy is the filter's source of truth; this file
is the *mapping*: which anti-slop rules already bind this skill, which ones
are new here, and where the two conflict and how the conflict is resolved.

Anti-slop is a **filter, not a style guide**. It prescribes no colors, fonts,
or layouts. Direction stays this skill's own: `design/tokens.json` +
`design/design-system-theme.md`. A sterile result means direction was
missing — it never means "add decoration".

## The mapping

Each `AS-*` rule names the upstream rule it implements. Status:
**enforced** = already covered by an existing validator check or engine
behavior; **new** = introduced by this mapping; **review** = checked by a
human/LLM read, not by the validator.

### Copy — what the dashboard says

- **AS-01 — No em dash in dashboard text (R-02). NEW, validator-checked.**
  Agent-written UI text (titles, KPI subtitles, fact labels/formulas, nav
  labels, tooltips) never contains `—`. Use a comma, colon, or parentheses.
  Machine-checked by **V-ANTISLOP**. Carve-outs, per R-02 itself: skill
  documentation is exempt (this repo's docs use em dashes freely); code
  comments are exempt (antislop-code governs whether a comment earns its
  place, not its punctuation); the en dash `–` for ranges and compounds
  (`diskon–omzet`) is allowed — R-02 bans only the em dash.
- **AS-02 — No hype vocabulary in dashboard or analysis text (R-16 +
  copywriting skill). NEW, validator-checked (stem list) + review (full list).**
  Banned stems, machine-checked by V-ANTISLOP: `unlock`, `elevate`,
  `empower`, `delve`, `showcase`, `testament`, `seamless`, `cutting-edge`,
  `revolutionary`, `next-gen`, `next generation`, `ai powered`,
  `game-changer`, `effortless`, `in today's`, `let's dive`,
  `read that again`, `let that sink in`, `i hope this helps`, `honestly?`.
  The full review list adds the copywriting patterns: significance
  inflation ("the future of X", "a testament to"), weasel attribution
  ("experts say" — name the source or cut it), persuasive authority tropes
  ("at its core", "what really matters"), chatbot closers, fake-candid
  openers ("Here's the thing"), signposting ("Let's dive in"), temporal
  runway clichés ("In today's fast-paced world"), all-caps emphasis,
  actorless passive (name the actor when known), inanimate subject + human
  verb ("the data tells us"), rule-of-three overuse, negative parallelism,
  aphorism formulas, staccato drama, theatrical takeaways ("The takeaway is
  simple:"), synonym cycling, false ranges, fabricated specifics,
  speculative gap-filling, generic positive conclusions. Deliberately NOT
  banned: `robust` (robust statistics is the field's name — MAD is a robust
  estimator, F-06), `journey` (customer journey is a real funnel concept),
  `powerful`/`intelligent`/`ultimate` (too broad; the review list governs
  them in context).
- **AS-03 — No invented numbers, claims, or vanity metrics (R-17, R-36,
  R-38). ENFORCED.** Already the skill's core: F-00 + Fakta Terverifikasi
  (every number carries its exact formula) + V-FACTS/V-FORMULA. Anti-slop
  adds the tie-breaker: an empty section beats a fabricated one. Missing
  data is shown as `[REAL DATA]` or "Coming soon", never filled with a
  plausible-looking number.
- **AS-04 — No fake testimonials, avatars, or names (R-18). NEW, review.**
  No invented user quotes, personas, or names in dashboards, case studies,
  or demo copy. Demo data uses clearly synthetic domain labels, never fake
  people.
- **AS-05 — Ask or use honest placeholders before creating assets (R-23).
  NEW, review.** A logo, brand mark, or nav structure the user did not
  supply is written as what it is (`[LOGO]`, `[REAL DATA]`), never invented.

### Design — what the dashboard looks like

- **AS-06 — Purpose-gated decoration (R-01, R-06, R-07, R-10, R-12, R-13,
  R-29). ENFORCED.** The tokens already decide these with written reasons:
  no gradients, no glassmorphism, no glow, no grid/dot backgrounds, shadow
  only as elevation. Palette is 2–3 core colors + 1 accent by `tokens.json`.
- **AS-07 — JetBrains Mono numerals are a deliberate choice, not a default
  (R-06, resolved). ENFORCED.** R-06 warns against picking JetBrains Mono
  *because it is a model default*. This skill picks it for a stated reason
  (tabular numerals that align in dense financial tables) — that is exactly
  the R-31 one-line-reason discipline. V-MONO keeps enforcing it.
- **AS-08 — The fixed enterprise layout is the direction, not a template
  (R-05, resolved). ENFORCED.** R-05 forbids default AI template layouts
  (Hero + 3 cards, bento-grid default, "Trusted By" bar). This skill's
  layout is a deliberate enterprise standard documented in
  `design/design-system-theme.md`; variation comes from content — the chart
  grammar follows the data shape — not from rearranging chrome.
- **AS-09 — Dark theme is the stated direction (R-21). ENFORCED.** Dark is
  legitimate here because the skill's direction says so (dev/analyst tool,
  dense tables, long sessions) — not "dark looks tech". V-DARK/V-PALETTE
  enforce it; there is no half-implemented light toggle (R-34: a shipped
  theme must fully work).
- **AS-10 — No dead controls (R-26). ENFORCED.** V-CLICK: every interactive
  element is wired, or it is removed. Never a decorative button.
- **AS-11 — Nav links only to sections that exist (R-24). ENFORCED.**
  V-SIDEBAR: nav is derived from real sections; no invented links.
- **AS-12 — Contrast, keyboard, semantics (R-25, R-32, R-39). REVIEW.**
  Native elements, accessible names, alt text, visible labels, one `h1`,
  `<html lang>`, landmarks, `prefers-reduced-motion` honored (the sidebar
  already honors it; the drawer closes on Esc). Contrast is checked with
  the vendored `skills/antislop-human/contrast-check.py` when a new text
  color is introduced — the validator does not measure contrast.
- **AS-13 — Empty, loading, and error states (R-27). REVIEW.** A dashboard
  built from empty or partial data shows an honest empty state, not a
  fabricated chart. In-progress records follow F-12 (never silently folded
  into an average). The validator does not yet cover this; it is a review
  rule for hand-built dashboards and engine extensions.
- **AS-14 — Mobile responsiveness is perfect (R-03). ENFORCED (sidebar) +
  REVIEW (rest).** V-SIDEBAR covers the drawer below 1100px; full
  reflow/overflow/tap-target checks follow the vendored
  `skills/antislop-layoutmobile/SKILL.md` at review time.
- **AS-15 — Animations need a written UX purpose (R-19). REVIEW.** ECharts
  transitions in this skill are minimal and functional; any new motion
  states its purpose and matches the declared MOTION dial.
- **AS-16 — No cloning popular products (R-30). REVIEW.** Do not rebuild
  Linear/Vercel/Stripe/Notion/Apple unless explicitly asked.

### Code and delivery — how the dashboard is built

- **AS-17 — One-line reason per major decision (R-31). ENFORCED.** The
  keystone. Every Fakta already carries its formula — that *is* the reason.
  Every chart choice follows the visualization grammar with a stated reason.
  If the reason cannot be written in one line, the decision is invalid.
- **AS-18 — Verify before you deliver (R-35). ENFORCED.** The repo's
  existing standard: validator **17/17** + engine math tests + no PASS
  claimed without the recorded run. Unmeasured = say "not measured".
- **AS-19 — Build in source, never by string-replacing output (R-33).
  ENFORCED.** The engine builds HTML in `tools/apex/build_page.py`; no
  post-hoc patching of generated files.
- **AS-20 — Pure signal code (R-33 + antislop-code). REVIEW.** No noisy
  ASCII section banners, no comments that merely repeat the code. Keep
  comments that carry a rule reference (F-*, Q-*) or a non-obvious reason.
- **AS-21 — No unmeasured performance claims (R-40). ENFORCED.** V-NOCDN:
  no render-blocking third-party scripts; never report a Lighthouse/Web
  Vitals number that was not measured.

## Machine-checkable subset: V-ANTISLOP

`validator/apex_validate.py` check **V-ANTISLOP** (17th check) enforces
AS-01 + the AS-02 stem list on a generated dashboard. It reads only text
that can reach the reader:

- strips HTML comments, `<style>` blocks, the vendored ECharts script
  block, and the `window.APEX_DATA` raw-rows payload (vendor code and user
  rows are not agent-written UI text);
- strips JS line/block comments from the remaining script (the app logic —
  fact strings and KPI subtitles are built there);
- FAILS on any em dash `—` or any banned stem in what remains.

What it does NOT cover (review rules above): the full copywriting pattern
list, contrast/keyboard/semantics, empty states, mobile reflow. A 17/17
pass means "no machine-detectable slop", not "the copy is good".

## Delivery Gate (adapted from the Rulebook)

Before a dashboard ships: validator 17/17, engine tests green, and a read
of any hand-written insight text against AS-02's full list. The gate report
is the 4-block PASS/FAIL the Rulebook requires: what was checked, what
failed (numbered), what was fixed, what remains open.

## Keeping the vendored copy current

`assets/anti-slop/` is a verbatim vendor of the upstream repo (MIT License
kept in place, attribution to Miqdad Badjuber kept in `SKILL.md` and here).
Sync procedure: replace the directory wholesale from the upstream release
matching `skills/antislop/VERSION`, then record the new version + upstream
commit at the top of this file. Never edit the vendored copy in place —
local adaptations live in this mapping file, not in `assets/anti-slop/`.
Current: **v3.2.28, upstream `4520786` (2026-11-12)**.
