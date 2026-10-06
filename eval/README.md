# Adversarial eval

`run_adversarial.py` executes the behavioral cases from
`proof/test-suites.md` (T1, T2, T3, T7) and `proof/adversarial-cases.md`
(C1–C15) against an LLM served over an OpenAI-compatible API.

Each case uses a **structured-response prompt** (`CHART: …`, `DECISION: …`,
…) so the pass/fail assertions stay deterministic instead of relying on a
second LLM judge.

Static cases are not LLM-executed — they are covered elsewhere:

| Case | Coverage |
|---|---|
| T4, T5, T6 | `validator/apex_validate.py` (12/12 on the v2 set) |
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
