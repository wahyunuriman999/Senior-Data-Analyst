# Usage — installing and running the Apex Data Analyst skill

Two ways to use this repo:

1. **As an AI skill** — give the prose standard to an AI agent so it builds
   dashboards the Apex way.
2. **As an engine** — run `tools/apex/apex_generate.py` directly; no AI needed.

## 1. Install as a skill

The skill entry point is `data-analyst-visualization-skill/SKILL.md`.
Supporting files it references: `design/`, `quality/`, `proof/`, `validator/`,
`tools/apex/`.

### Claude Code

```bash
mkdir -p ~/.claude/skills
cp -r data-analyst-visualization-skill ~/.claude/skills/apex-data-analyst
```

Project-scoped instead: copy into `<project>/.claude/skills/apex-data-analyst/`.
Then prompt: *"Build an executive sales dashboard from this CSV, following
the apex-data-analyst skill."*

### Cline (VS Code)

Cline reads workspace instructions. Either:

- copy the skill into your project and add to **Custom Instructions**
  (Cline settings): *"Follow data-analyst-visualization-skill/SKILL.md in
  <path> for any dashboard work"*, or
- paste `SKILL.md` content into a `.clinerules` file at the project root.

### Cursor / Antigravity / other agents

Point the agent at the skill directory and instruct it to read `SKILL.md`
first for any visualization task. Example prompt:

> Read `data-analyst-visualization-skill/SKILL.md` and follow it end-to-end.
> Dataset: <describe or attach CSV>. Deliver one self-contained HTML file.
> Every number must be computed from the data; no AI-storyteller narration;
> every dimensional visual must be click-to-filter; validate with
> `validator/apex_validate.py` before you call it done.

## 2. Run the engine directly

```bash
# vendor ECharts once (the standard forbids external CDNs)
mkdir -p tools/apex/vendor
curl -sSL -o tools/apex/vendor/echarts.min.js \
  https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js

# from your own CSV (columns: period,dim1,dim2,units,revenue,cost[,discount])
python3 tools/apex/apex_generate.py --csv data.csv --config cfg.json --out dashboard.html

# or a synthetic demo domain
python3 tools/apex/apex_generate.py --demo marketing --out marketing.html

# validate (expect 12/12)
python3 validator/apex_validate.py dashboard.html
```

See `tools/apex/README.md` for the config schema. Demo domains are synthetic
and labeled as such in the output.

## 3. What "done" looks like

Per `SKILL.md` §QA, a dashboard is done only when:

- `validator/apex_validate.py` → 12/12
- every number traceable to the filtered row set (SSOT)
- every dimensional visual is click-to-filter (with the two documented
  exceptions: waterfall components, cohort cells)
- insights are Fakta Terverifikasi: value + rule/formula, no persona narration
- zero external network requests (open DevTools → Network → empty)
