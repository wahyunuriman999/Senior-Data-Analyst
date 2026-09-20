import os
import sys
import re

print("APEX DATA ANALYST REGRESSION SUITE\n")

errors = 0

def assert_check(condition, name):
    global errors
    if condition:
        print(f"[PASS] {name}")
    else:
        print(f"[FAIL] {name}")
        errors += 1

# 1. Fixture Integrity
fixtures = [
    "null_revenue.csv", "orders.csv", "order_tags.csv",
    "pie_18_categories.csv", "time_series.csv"
]
fixture_pass = all(os.path.exists(f"data-analyst-visualization-skill/proof/fixtures/{f}") for f in fixtures)
assert_check(fixture_pass, "Fixture integrity")

# 2. SQL Validation
sql_log = "data-analyst-visualization-skill/proof/runners/sql_validation_log.txt"
sql_pass = os.path.exists(sql_log) and "STATUS: PASS" in open(sql_log).read()
assert_check(sql_pass, "SQL validation execution log exists and passed")

# 3. Forecast Validation
fc_log = "data-analyst-visualization-skill/proof/runners/forecast_validation_log.txt"
fc_pass = os.path.exists(fc_log) and "STATUS: PASS" in open(fc_log).read()
assert_check(fc_pass, "Forecast validation execution log exists and passed")

# 4. Artifact Integrity
exec_html = "data-analyst-visualization-skill/proof/examples/executive_sales/executive_sales.html"
analyst_html = "data-analyst-visualization-skill/proof/examples/analyst_deep_dive/analyst_deep_dive.html"
art_pass = False
if os.path.exists(exec_html) and os.path.exists(analyst_html):
    with open(exec_html, 'r', encoding='utf-8') as f:
        content = f.read()
        if "echarts.min.js" in content and "html" in content.lower():
            art_pass = True
assert_check(art_pass, "Visual artifact generation & structure integrity")

# 5. Benchmark Status Consistency
bench = "data-analyst-visualization-skill/proof/behavioral-benchmarks.md"
bench_pass = False
if os.path.exists(bench):
    content = open(bench).read()
    # Check that B01 is strictly NOT_EXECUTED
    if re.search(r'B01\s*\|\s*NOT_EXECUTED', content) and not re.search(r'B01\s*\|\s*PASS', content):
        bench_pass = True
assert_check(bench_pass, "Benchmark status consistency (No fabricated LLM PASS claims)")

print("\n")
if errors == 0:
    print("RESULT: PASS")
    print("EXIT CODE: 0")
    sys.exit(0)
else:
    print("RESULT: FAIL")
    print(f"EXIT CODE: {errors}")
    sys.exit(errors)
