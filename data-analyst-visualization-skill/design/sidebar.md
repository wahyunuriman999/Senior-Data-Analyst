# Sidebar v2 — Navigation Spec

The skill's dashboards ship a sidebar, not a link list. This file is the
source of truth for what "keren" means here: grouped, scannable, collapsible,
and usable on a narrow screen — in the same dark premium tokens as the rest
of the dashboard (`design/tokens.json`). The reference structure is the
classic SaaS sidebar: a brand block, **labelled groups** (like FEATURES /
EXAMPLES), icon + label items, a clear active state, and a footer — never a
flat stack of links.

## 1. Anatomy (top → bottom)

| Part | Spec |
|---|---|
| Brand | 36px blue tile with a 1–2 letter monogram (`AX` default) + name (13px, 800) + tagline (10.5px, muted). Collapse button at the right end. |
| Group label | 10px, 700, uppercase, letter-spacing 1.2px, muted (`#8E97AD`). One per group. |
| Nav item | 28px icon tile (`#182238`) + label (12.5px) + optional badge. `border-left: 3px solid transparent`. |
| Active item | `background: rgba(91,141,239,.14)`, left border `#5B8DEF`, label 600 + `#ECEFF6`, icon tile turns blue. Exactly one `.on` at load (the first section). |
| Badge | Monospace 10px pill. Only build-time counts that are true: period count on Tren, dim1 value count on Tabel. Never a vanity number. |
| Footer | Avatar circle (initials) + user name / role + version chip (`v2`). |

Default groups, in order — derived from the sections that actually exist
on the page:

- **Analisis**: Tren & Forecast · Dekomposisi Varians · Kohort & Alur (only when cohort data exists)
- **Data**: {dim1} & {dim2} · Tabel {dim1}
- **Verifikasi**: Fakta Terverifikasi

## 2. Nav model rule (anti-slop)

**Nav is derived from real sections, never invented.** Every `href` must
point at a section `id` present in the same file (`#sec-tren`, `#sec-var`,
`#sec-kohort`, `#sec-wilayah`, `#sec-tabel`, `#sec-insight`). A link to a
missing section is a defect, not decoration. The cohort item appears only
when cohort data exists; otherwise the group simply has two items.

`cfg.sidebar` overrides (all optional, all escaped):

```json
{"sidebar": {
  "brand": {"mark": "AX", "name": "APEX ANALYST", "tag": "Apex Standard v2"},
  "footer": {"user": "Analyst", "role": "Apex Standard v2"}
}}
```

## 3. States

| State | Behaviour |
|---|---|
| Hover | Item bg `#182238`, label `#ECEFF6`. |
| Active (`.on`) | Tinted bg + blue left bar + blue icon tile (see §1). Set on click immediately; scrollspy updates it while scrolling. |
| Scrollspy | `IntersectionObserver`-free rAF-throttled scroll handler: the last section whose top is ≤ 140px from the viewport top becomes `.on`. The `#sec-kohort` wrapper uses `display:contents`, so its first child is measured instead. |
| Rail (collapsed) | `#app.rail`: sidebar 248px → 68px, labels / group labels / badges / footer text hidden, icons centred, active shown by the blue icon tile only. Toggle is the `«` / `»` button in the brand row. |
| Persistence | Rail state survives reload via `localStorage` key `apex-sidebar-rail` (`"1"`/`"0"`). A failed read/write (private mode) must never break chart rendering — all access is `try/catch`. |
| Drawer (≤ 1100px) | Sidebar becomes a fixed off-canvas drawer (`translateX(-105%)` → `0`), opened by the `☰` button in the topbar, closed by backdrop click, `Esc`, or tapping a nav item. **The old behaviour — `display:none` below 1100px, deleting navigation on small screens — is forbidden.** |
| Reduced motion | `prefers-reduced-motion: reduce` disables the drawer transition. |

## 4. Tokens

From `design/tokens.json` (`layout.sidebar` + `color.sidebar`):

- bg `#0C1327`, width 248px, rail 68px, active bg `rgba(91,141,239,.14)`
- borders `#26314D`, muted text `#8E97AD`, primary text `#ECEFF6`
- icon tile `#182238`, active tile `#5B8DEF`

## 5. Accessibility

- `<aside class="sidebar" aria-label="Navigasi dashboard">`,
  `<nav aria-label="Bagian dashboard">`.
- Collapse + hamburger are real `<button>`s with `aria-expanded`,
  `aria-label`, and (hamburger) `aria-controls="sidebar"`.
- `:focus-visible` outline `2px solid #5B8DEF`.
- All items are native `<a href="#…">` links: keyboard navigation and
  anchor jumps work with JS disabled.

## 6. Do / Don't

- DO group items under short uppercase labels (Analisis / Data / Verifikasi).
- DO keep exactly one active item; it must match the section on screen.
- DO show a badge only when the number is computed at build time.
- DON'T add links to pages/sections that don't exist.
- DON'T hide the sidebar with `display:none` at any breakpoint.
- DON'T put the slicer/filters inside the sidebar — filters live in the
  sticky header slicer bar (SKILL.md click-to-filter protocol).
- DON'T use emoji as the *only* affordance: every item has a text label
  (icons are decoration; the rail hides labels but keeps `title` tooltips
  via the link text).

## 7. Verification

- `validator/apex_validate.py` check **V-SIDEBAR** (16th): `<aside
  class="sidebar">` + ≥ 2 group labels + one `.nav-item.on` + collapse
  button + hamburger + drawer markup + no `.sidebar{display:none}` +
  ≥ 1 `.nav-badge`.
- `data-analyst-visualization-skill/proof/runners/test_sidebar.py`:
  builds a dashboard from `tools/apex/build_page.py` and asserts the
  anatomy, the cohort conditional, the brand override, and the badge
  counts — no browser needed.
