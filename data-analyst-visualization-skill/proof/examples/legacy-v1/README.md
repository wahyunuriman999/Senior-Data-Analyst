# Legacy v1 examples

Dashboards generated **before** the Apex v2 standard (2026-10-06) by the
template scripts in `tools/generators/`.

They do **not** comply with the current standard:

- v1 neon palette (deprecated by `design/tokens.json`)
- "AI Data Storyteller" persona panels (replaced by Fakta Terverifikasi)
- partial or missing click-to-filter
- possible external CDN references (violates Q-VIS-FATAL)

Reference scores: `apex_bento_dashboard.html` → **4/12** on
`validator/apex_validate.py`.

Kept for history, not as reference. The current reference set is
`../v2/` (engine-generated, 12/12) and `../llm-validation/`.
