import sys

def patch_driver():
    with open('data-analyst-visualization-skill/analytical/driver-analysis.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Target 1: Causal-vs-Associational Boundary
    old_f = '''REQUIRED: "Feature X is the strongest predictor of high LTV in the historical data."
REQUIRED: "Metric Y is highly associated with conversion. We recommend an A/B test to see
           if intervening on Metric Y causally improves conversion."

Only refer to variables as "Predictors", "Correlates", or "Leading Indicators", unless
the data comes from a randomized experiment.'''

    new_f = '''REQUIRED: "Feature X is the strongest predictor of high LTV in the historical data."
REQUIRED: "Metric Y is highly associated with conversion. It is a strong candidate lever. 
           We recommend an A/B test to validate if intervening on Metric Y causally improves conversion."

Observational associations may generate "Candidate Drivers," "Hypotheses," or "Candidate Levers."
However, explicitly label them as associational hypotheses. Do NOT present them as proven causal interventions unless the data comes from a randomized experiment.'''
    
    content = content.replace(old_f, new_f)

    # Target 2: Adversarial Example
    old_adv = '''**Request:** "Tell me exactly what features to change to increase conversion rate based on the driver analysis."

**Engine Response:**
`
BLOCKED — Causal interpretation of observational driver analysis.

ISSUE: Driver analysis identifies what correlates with conversion, not what causes it.
       Changing a highly ranked feature (e.g., 'Viewed Pricing Page') by forcing all users
       to view the pricing page may decrease conversion, despite the positive correlation.

ACTION:
    1. Driver analysis will output the top PREDICTORS of conversion.
    2. These predictors must be treated as HYPOTHESES for experimentation.
    3. Causal language ("features to change to increase conversion") is rejected.

OUTPUT PROCEEDING WITH OBSERVATIONAL REPORT ONLY...
`'''

    new_adv = '''**Request:** "Tell me exactly what features to change to increase conversion rate based on the driver analysis."

**Engine Response:**
`
CAUSAL CLAIM BLOCKED — Re-framing as Candidate Levers.

ISSUE: Driver analysis identifies what correlates with conversion (associational), not what causes it.
       You asked what to "change" (intervention). I cannot guarantee a causal outcome from observational data.

ACTION:
    I will identify the top PREDICTORS of conversion and present them as CANDIDATE LEVERS (Hypotheses).
    Changing a highly ranked feature (e.g., 'Viewed Pricing Page') by forcing users to view it 
    may decrease conversion despite the correlation. Causal validation requires an experiment.

OUTPUT PROCEEDING WITH CANDIDATE LEVERS (HYPOTHESES) REPORT...
`'''

    content = content.replace(old_adv, new_adv)
    
    # Target 3: Test cases
    old_tc = '''| DRV-002 | Request containing causal language ("levers to pull") | Causal blocking activated | Warning emitted, text rephrased |'''
    new_tc = '''| DRV-002 | Request causal levers from observational data | "Candidate lever" allowed with hypothesis label; proven causal claim blocked | Engine reframes request but does not fail |'''
    content = content.replace(old_tc, new_tc)

    with open('data-analyst-visualization-skill/analytical/driver-analysis.md', 'w', encoding='utf-8') as f:
        f.write(content)

def patch_comparative():
    with open('data-analyst-visualization-skill/analytical/comparative-analysis.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_adv = '''Causal evidence requires a randomized rollout."\n`'''
    new_adv = '''Causal evidence requires a randomized rollout."\n`\n\n**Counterexample C — Pre-profiled dataset blocking (Rule exception test):**\n`\nRequest: "I already ran profiling on this clean A/B test data. Normal distribution, n=5000 each. Compare means."\nWRONG (Over-constrained): "BLOCKED. Must run Engine B1.1 first."\nRIGHT: "Descriptive evidence provided (Normal, n=5000). Proceeding directly to Welch's t-test (Step 3)."\n`'''
    
    content = content.replace(old_adv, new_adv)
    
    with open('data-analyst-visualization-skill/analytical/comparative-analysis.md', 'w', encoding='utf-8') as f:
        f.write(content)

patch_driver()
patch_comparative()
print("Python script executed.")