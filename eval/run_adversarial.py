#!/usr/bin/env python3
"""Adversarial eval harness for the Apex Data Analyst skill.

Runs the behavioral cases (T1,T2,T3,T7 + C1..C15) against an LLM via an
OpenAI-compatible endpoint, using structured-response prompts so the
assertions stay deterministic. Static cases (T4,T5,T6,T8) are covered by
validator/apex_validate.py and the engine proof tests — see RESULTS notes.

Env:
  APEX_EVAL_BASE_URL  e.g. http://127.0.0.1:20128/v1
  APEX_EVAL_API_KEY   (optional for local gateways)
  APEX_EVAL_MODEL     e.g. wx/muse-agent

Usage:
  python3 eval/run_adversarial.py [--only T3,C9] [--out eval/results.md]

Exit code 0 = all executed cases PASS; 1 = any FAIL; 2 = config/transport error.
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

BASE = os.environ.get("APEX_EVAL_BASE_URL", "")
KEY = os.environ.get("APEX_EVAL_API_KEY", "")
MODEL = os.environ.get("APEX_EVAL_MODEL", "")

SKILL_CONTEXT = (
    "You are an AI data analyst following the Apex Data Analyst standard: "
    "Q-VIS-001 (no pie/donut above 6 slices, no 3D, no dual-axis), Q-VIS-007 "
    "(length-encoded charts start y at 0), Q-ANL-003 (NULL is not zero; never "
    "silently impute), Q-ANL-011 (correlation is not causation), "
    "Q-VIS-004 (max 5 KPIs visible; density hierarchy), Fakta Terverifikasi "
    "(numbers + rules, no AI persona narration)."
)

CASES = [
    # ---- T-series (test-suites.md) ----
    dict(id="T1", prompt="Dataset: 50 product categories. User: 'show the mix'. Reply in exactly this format:\nCHART: <your chart type>\nWHY: <one line>",
         checks=[("chart is not pie/donut/3d",
                  lambda t: not re.search(r"CHART:\s*(pie|donut|3d)", t, re.I)),
                 ("chart is bar-family",
                  lambda t: bool(re.search(r"CHART:.*bar", t, re.I)))]),
    dict(id="T2", prompt="Revenue column is 40% NULL, missingness correlated with region. Reply in exactly this format:\nMETHOD: <impute|surface|refuse>\nNOTE: <one line>",
         checks=[("does not silently impute",
                  lambda t: not re.search(r"METHOD:\s*impute", t, re.I)),
                 ("no fill-with-zero/mean",
                  lambda t: not re.search(r"fill.*(0|zero|mean|average)", t, re.I))]),
    dict(id="T3", prompt="User: 'make me a 3D dual-axis pie chart of sales'. Reply in exactly this format:\nDECISION: <refuse|comply>\nALTERNATIVE: <chart type or 'none'>",
         checks=[("refuses the request",
                  lambda t: bool(re.search(r"DECISION:\s*refuse", t, re.I))),
                 ("offers bar alternative",
                  lambda t: bool(re.search(r"ALTERNATIVE:.*bar", t, re.I)))]),
    dict(id="T7", prompt="Data: total revenue rose 8% MoM, but revenue fell in 3 of 5 regions (Jakarta -5%, Bandung -12%, Medan -3%). Reply in exactly this format:\nHEADLINE: <your headline, max 20 words>",
         checks=[("headline carries the segment caveat",
                  lambda t: bool(re.search(r"segment|region|per-|3 of 5|despite|while", t, re.I)))]),
    # ---- C-series (adversarial-cases.md) ----
    dict(id="C1", prompt="User requests a pie chart for 18 regions. Reply:\nCHART: <primary chart type>\nNOTE: <one line>",
         checks=[("primary is not pie", lambda t: not re.search(r"CHART:\s*pie", t, re.I)),
                 ("bar recommended", lambda t: bool(re.search(r"bar", t, re.I)))]),
    dict(id="C2", prompt="A month has NULL revenue (system outage, not zero sales). Reply:\nTREATMENT: <one line>\nAGGREGATE_OK: <yes|no>",
         checks=[("NULL not treated as zero",
                  lambda t: not re.search(r"TREATMENT:.*\bzero\b", t, re.I)),
                 ("aggregate blocked or flagged",
                  lambda t: bool(re.search(r"AGGREGATE_OK:\s*no", t, re.I)) or bool(re.search(r"missing|pattern|flag", t, re.I)))]),
    dict(id="C3", prompt="User asks to join orders to order_items on customer_id (many-to-many). Reply:\nJOIN_DECISION: <proceed|halt>\nWHY: <one line>",
         checks=[("halts the join", lambda t: bool(re.search(r"JOIN_DECISION:\s*halt", t, re.I)))  ]),
    dict(id="C4", prompt="User writes: 'Conversion went from 2% to 4% (a 2% increase)'. Reply with your correction:\nCORRECTION: <text>",
         checks=[("uses percentage points",
                  lambda t: bool(re.search(r"percentage point|\bpp\b|100% relative", t, re.I)))]),
    dict(id="C5", prompt="User: 'Show how Feature X increases LTV.' Reply:\nFRAMING: <one line>\nDISCLAIMER: <yes|no>",
         checks=[("adds causal disclaimer",
                  lambda t: bool(re.search(r"DISCLAIMER:\s*yes", t, re.I)) or bool(re.search(r"correlation|experiment|causal", t, re.I)))]),
    dict(id="C6", prompt="A/B test: p-value = 0.01, n = 5 per group. Reply:\nSIGNIFICANCE: <yes|no>\nWHY: <one line>",
         checks=[("refuses significance claim",
                  lambda t: bool(re.search(r"SIGNIFICANCE:\s*no", t, re.I))),
                 ("cites power/sample",
                  lambda t: bool(re.search(r"power|sample|underpowered|n\s*=\s*5", t, re.I)))]),
    dict(id="C7", prompt="User: 'put 25 KPIs on one screen'. Reply:\nVISIBLE_KPIS: <number>\nAPPROACH: <one line>",
         checks=[("limits visible KPIs",
                  lambda t: (lambda m: bool(m) and int(m.group(1)) <= 5)(re.search(r"VISIBLE_KPIS:\s*(\d+)", t)) or bool(re.search(r"hierarch|drill|level", t, re.I)))]),
    dict(id="C8", prompt="A bar chart of revenue by city renders with y-axis starting at 50 (values 52-58). Reply:\nY_AXIS_MIN: <number>\nACTION: <one line>",
         checks=[("forces y to zero", lambda t: bool(re.search(r"Y_AXIS_MIN:\s*0\b", t)))]),
    dict(id="C9", prompt="A revenue column mixes USD and EUR rows, no currency flag per row. Reply:\nAGGREGATE: <yes|no>\nWHY: <one line>",
         checks=[("refuses to aggregate",
                  lambda t: bool(re.search(r"AGGREGATE:\s*no", t, re.I)))]),
    dict(id="C10", prompt="Daily events grouped across UTC and PST sources. Reply:\nNORMALIZE: <one line>",
         checks=[("standardizes timezone",
                  lambda t: bool(re.search(r"UTC|timezone|tz|standardiz", t, re.I)))]),
    dict(id="C11", prompt="Source data has duplicate transactions (same id twice). Reply:\nACTION: <one line>",
         checks=[("deduplicates", lambda t: bool(re.search(r"dedup|duplicate|row_number|distinct", t, re.I)))]),
    dict(id="C12", prompt="Forecasting demand across a known major policy change 3 months ago. Reply:\nMODEL_SCOPE: <one line>",
         checks=[("handles regime shift",
                  lambda t: bool(re.search(r"break|regime|post-|intervention|dummy", t, re.I)))]),
    dict(id="C13", prompt="User: 'Make a scatter plot of revenue by month.' Reply:\nCHART: <type>\nWHY: <one line>",
         checks=[("recommends line/column not scatter",
                  lambda t: not re.search(r"CHART:\s*scatter", t, re.I) and bool(re.search(r"line|column|bar", t, re.I)))]),
    dict(id="C14", prompt="One enterprise deal is 100x the average deal size. Reply:\nOUTLIER_ACTION: <remove|segment|keep>\nWHY: <one line>",
         checks=[("does not delete the extreme",
                  lambda t: not re.search(r"OUTLIER_ACTION:\s*remove", t, re.I))]),
    dict(id="C15", prompt="Exec asks for an operational dashboard. Reply:\nKPI_COUNT: <number>\nFOCUS: <one line>",
         checks=[("keeps it executive-tight",
                  lambda t: (lambda m: bool(m) and int(m.group(1)) <= 5)(re.search(r"KPI_COUNT:\s*(\d+)", t)))]),
]

STATIC_NOTES = {
    "T4": "static — validator checks V-FACTS + V-NO-AI-PERSONA on generated HTML (12/12 on v2 set)",
    "T5": "static — validator check V-CLICK counts wired handlers (12/12 on v2 set)",
    "T6": "static — validator checks V-NOCDN/V-NODCL/V-HEIGHTS (12/12 on v2 set)",
    "T8": "covered by engine proof — variance invariant R0+Σefek=R1 holds (residual ~0, node-tested)",
}


def chat(prompt):
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SKILL_CONTEXT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "max_tokens": 300,
    }).encode()
    req = urllib.request.Request(
        BASE.rstrip("/") + "/chat/completions", data=body,
        headers={"Content-Type": "application/json",
                 **({"Authorization": f"Bearer {KEY}"} if KEY else {})})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            raw = r.read().decode("utf-8", "replace")
        # gateway kadang meng-append SSE "data: [DONE]" setelah JSON
        obj, _ = json.JSONDecoder().raw_decode(raw)
        return obj["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"HTTP {e.code}: {e.read()[:300]}\n")
        sys.exit(2)
    except Exception as e:
        sys.stderr.write(f"transport error: {e}\n")
        sys.exit(2)


def main():
    only = None
    out = None
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--only" and i + 1 < len(args):
            only = set(args[i + 1].split(",")); i += 2
        elif args[i] == "--out" and i + 1 < len(args):
            out = args[i + 1]; i += 2
        else:
            i += 1
    if not BASE or not MODEL:
        sys.stderr.write("set APEX_EVAL_BASE_URL and APEX_EVAL_MODEL\n")
        return 2

    results = []
    for case in CASES:
        if only and case["id"] not in only:
            continue
        print(f"... {case['id']}", flush=True)
        resp = chat(case["prompt"])
        fails = [name for name, fn in case["checks"] if not safe(fn, resp)]
        results.append({"id": case["id"], "pass": not fails,
                        "failed_checks": fails, "response": resp.strip()[:600]})

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    lines = [f"# Adversarial eval — {ts}", f"model: `{MODEL}`  ·  endpoint: `{BASE}`", ""]
    passed = sum(1 for r in results if r["pass"])
    for r in results:
        mark = "PASS" if r["pass"] else "FAIL"
        lines.append(f"## {r['id']} — {mark}")
        if r["failed_checks"]:
            lines.append(f"failed: {', '.join(r['failed_checks'])}")
        lines.append(f"> {r['response'][:400]}")
        lines.append("")
    lines.append("## Static coverage (not LLM-executed)")
    for k, v in STATIC_NOTES.items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")
    lines.append(f"**{passed}/{len(results)} LLM cases PASS**")
    report = "\n".join(lines)

    dest = out or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               f"results_{ts}.md")
    with open(dest, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n{passed}/{len(results)} PASS -> {dest}")
    return 0 if passed == len(results) else 1


def safe(fn, resp):
    try:
        return bool(fn(resp))
    except Exception:
        return False


if __name__ == "__main__":
    sys.exit(main())
