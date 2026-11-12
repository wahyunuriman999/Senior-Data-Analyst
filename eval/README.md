# Adversarial eval

`run_adversarial.py` executes the behavioral cases from
`proof/test-suites.md` (T1, T2, T3, T7), `proof/adversarial-cases.md`
(C1–C15), and the v3 formula-library cases (F01, F02, F03, F04, F05, F06,
F08, F12) from `analytical/formula-library.md` — 27 cases total.

Each case uses a **structured-response prompt** (`CHART: …`, `DECISION: …`,
…) so the pass/fail assertions stay deterministic instead of relying on a
second LLM judge. Responses are normalized (markdown emphasis +
zero-width chars stripped) before the assertions run, so a correct
structured answer never fails on formatting.

Static cases are not LLM-executed — they are covered elsewhere:

| Case | Coverage |
|---|---|
| T4, T5, T6 | `validator/apex_validate.py` (17/17 on the v2 set) |
| T8 | engine proof test — variance invariant `R0 + Σefek = R1` holds (residual ~0) |

## Run

```bash
APEX_EVAL_BASE_URL=http://127.0.0.1:20128/v1 \
APEX_EVAL_MODEL=wx/muse-agent \
APEX_EVAL_API_KEY=<key-if-needed> \
python3 eval/run_adversarial.py --out eval/results_<date>_<model>.md

# subset:
python3 eval/run_adversarial.py --only T3,C9 --out /tmp/quick.md
```

Exit code: 0 = all PASS, 1 = any FAIL, 2 = config/transport error.
Results are committed next to the harness so the evidence is reviewable.
