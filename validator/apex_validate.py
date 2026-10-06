#!/usr/bin/env python3
"""apex_validate.py — machine-checkable compliance for the Apex dashboard standard.

Usage:  python3 apex_validate.py <dashboard.html> [--json]

Runs the static (Auto=✓) checks from quality/qa-matrices.md against a generated
HTML dashboard. Exit 0 = all PASS, 1 = any FAIL, 2 = usage error.
Stdlib only — no dependencies.
"""
import json
import re
import sys

# Tokens mirrored from data-analyst-visualization-skill/design/tokens.json
TOKENS = {
    "bg": "#0A0F1E", "card": "#111A30", "card2": "#182238", "border": "#26314D",
    "text": "#ECEFF6", "muted": "#8E97AD",
    "base": "#5B8DEF", "pos": "#34B98A", "neg": "#E0605F",
    "amber": "#E8A54B", "peri": "#8C9BDB", "teal": "#3EC6A5",
}
DEPRECATED_NEON = ["#00f0ff", "#00ff66", "#ff0055", "#3B82F6",
                   "#10B981", "#EF4444", "#8B5CF6", "#F59E0B"]
CAUSAL_WORDS = ["menyebabkan", "disebabkan oleh", "membuktikan",
                "causes", "proven to drive", "proves that"]


def check_v_dark(html):
    """V-DARK (Q-VIS-000): dark background token present."""
    ok = TOKENS["bg"].lower() in html.lower()
    return ok, f"bg token {TOKENS['bg']} {'found' if ok else 'MISSING'}"


def check_v_palette(html):
    """V-PALETTE (Q-VIS-007): v2 semantic tokens used; v1 neon absent."""
    low = html.lower()
    missing = [h for h in [TOKENS["base"], TOKENS["pos"], TOKENS["neg"]]
               if h.lower() not in low]
    neon = [h for h in DEPRECATED_NEON if h.lower() in low]
    ok = not missing and not neon
    detail = []
    if missing:
        detail.append("missing tokens: " + ",".join(missing))
    if neon:
        detail.append("deprecated neon tokens present: " + ",".join(neon))
    return ok, "; ".join(detail) if detail else "v2 palette clean"


def check_v_nocdn(html):
    """V-NOCDN (Q-VIS-FATAL): zero external network-loading patterns."""
    pats = [r'(src|href)\s*=\s*["\']https?://', r'fetch\(\s*["\']https?://',
            r'@import\s', r'url\(\s*["\']?https?://',
            r'<script[^>]+src\s*=', r'<link[^>]+href\s*=\s*["\']http']
    hits = [p for p in pats if re.search(p, html, re.I)]
    return not hits, "no external loads" if not hits else "external loads: " + ",".join(hits)


def check_v_nodcl(html):
    """V-NODCL (Q-VIS-FATAL): no DOMContentLoaded wrapper."""
    # allow the word in comments; fail only on actual listener registration
    hit = re.search(r'addEventListener\s*\(\s*["\']DOMContentLoaded["\']', html)
    return not hit, "no DOMContentLoaded trap" if not hit else "DOMContentLoaded listener found"


def check_v_heights(html):
    """V-HEIGHTS (Q-VIS-FATAL): chart containers use hardcoded pixel heights."""
    heights = re.findall(r'height\s*:\s*(\d+)px', html)
    ok = len(heights) >= 4
    return ok, f"{len(heights)} hardcoded px heights" + ("" if ok else " (< 4)")


def check_v_facts(html):
    """V-FACTS (FACTS-PANEL): fact panel with formula/rule per fact."""
    has_panel = bool(re.search(r'class="fact"|id="insights"|Fakta Terverifikasi', html))
    rules = len(re.findall(r'aturan:|rumus:|residu|formula:', html, re.I))
    ok = has_panel and rules >= 3
    return ok, f"panel={has_panel}, rule markers={rules}"


def check_v_no_ai_persona(html):
    """V-NO-AI-PERSONA (FACTS-PANEL): no narrative AI analysis."""
    pats = [r'AI Data Storyteller', r'sebagai AI\b', r'menurut saya,',
            r'\bI (think|believe|feel)\b']
    hits = [p for p in pats if re.search(p, html, re.I)]
    return not hits, "no AI persona" if not hits else "persona markers: " + ",".join(hits)


def check_v_nocausal(html):
    """V-NOCAUSAL (Q-STORY-003): no causal claims on observational data."""
    hits = [w for w in CAUSAL_WORDS if w.lower() in html.lower()]
    return not hits, "no causal language" if not hits else "causal words: " + ",".join(hits)


def check_v_click(html):
    """V-CLICK (Q-VIS-CROSS-FILTER): click handlers wired on dimension vizzes."""
    handlers = re.findall(r'''\.on\(\s*["']click["']''', html)
    ok = len(handlers) >= 4
    return ok, f"{len(handlers)} click handlers" + ("" if ok else " (< 4: need bar/donut/trend/sankey/table)")


def check_v_slicer(html):
    """V-SLICER (Q-VIS-HEADER-SLICER): sticky slicer, selects, chips, reset."""
    selects = len(re.findall(r'<select', html, re.I))
    chips = bool(re.search(r'id="chips"|class="chip"', html))
    reset = bool(re.search(r'[Rr]eset|Clear All', html))
    sticky = bool(re.search(r'position\s*:\s*sticky', html))
    ok = selects >= 3 and chips and reset and sticky
    return ok, f"selects={selects}, chips={chips}, reset={reset}, sticky={sticky}"


def check_v_mono(html):
    """V-MONO (design tokens): monospace numerals."""
    ok = bool(re.search(r'JetBrains Mono|ui-monospace', html))
    return ok, "mono numerals present" if ok else "no monospace stack found"


def check_v_ssot(html):
    """V-SSOT (Q-VIS-ANALYTICAL): single data array + filter() usage (heuristic)."""
    has_filter = '.filter(' in html
    has_ssot_marker = bool(re.search(r'SSOT|APEX_DATA|Single Source', html))
    ok = has_filter and has_ssot_marker
    return ok, f"filter() usage={has_filter}, SSOT marker={has_ssot_marker}"


CHECKS = [
    ("V-DARK", "Q-VIS-000", check_v_dark),
    ("V-PALETTE", "Q-VIS-007", check_v_palette),
    ("V-NOCDN", "Q-VIS-FATAL", check_v_nocdn),
    ("V-NODCL", "Q-VIS-FATAL", check_v_nodcl),
    ("V-HEIGHTS", "Q-VIS-FATAL", check_v_heights),
    ("V-FACTS", "FACTS-PANEL", check_v_facts),
    ("V-NO-AI-PERSONA", "FACTS-PANEL", check_v_no_ai_persona),
    ("V-NOCAUSAL", "Q-STORY-003", check_v_nocausal),
    ("V-CLICK", "Q-VIS-CROSS-FILTER", check_v_click),
    ("V-SLICER", "Q-VIS-HEADER-SLICER", check_v_slicer),
    ("V-MONO", "tokens.json", check_v_mono),
    ("V-SSOT", "Q-VIS-ANALYTICAL", check_v_ssot),
]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    as_json = "--json" in sys.argv[1:]
    if len(args) != 1:
        print("usage: apex_validate.py <dashboard.html> [--json]", file=sys.stderr)
        return 2
    try:
        with open(args[0], encoding="utf-8") as f:
            html = f.read()
    except OSError as e:
        print(f"cannot read file: {e}", file=sys.stderr)
        return 2

    results = []
    for cid, ref, fn in CHECKS:
        try:
            ok, detail = fn(html)
        except Exception as e:  # noqa: BLE001 — a crashing check is a FAIL
            ok, detail = False, f"check crashed: {e}"
        results.append({"id": cid, "ref": ref, "pass": bool(ok), "detail": detail})

    npass = sum(1 for r in results if r["pass"])
    if as_json:
        print(json.dumps({"file": args[0], "pass": npass,
                          "fail": len(results) - npass, "checks": results},
                         indent=2))
    else:
        for r in results:
            print(f"{'PASS' if r['pass'] else 'FAIL'}  {r['id']:16} [{r['ref']}] {r['detail']}")
        print(f"\n{npass}/{len(results)} checks passed")
    return 0 if npass == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
