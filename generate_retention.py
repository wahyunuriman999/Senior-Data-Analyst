import urllib.request

print("Downloading ECharts library for Retention Dashboard...")
req = urllib.request.Request('https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        echarts_js = response.read().decode('utf-8')
except Exception as e:
    print("Download failed:", e)
    echarts_js = "console.error('Failed to download ECharts');"

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Retention & Revenue Quality - SaaS Analytics</title>
    
    <!-- Q-VIS-FATAL: INLINE ECHARTS PAYLOAD -->
    <script>
    ECHARTS_INLINE_PAYLOAD
    </script>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
        
        :root {
            --bg-base: #0B1120;
            --bg-panel: #111827; 
            --border: #1F2937;
            --text-main: #F9FAFB;
            --text-muted: #9CA3AF;
            
            /* Premium SaaS Semantic Colors */
            --primary: #6366F1; /* Indigo */
            --positive: #10B981; /* Emerald */
            --negative: #F43F5E; /* Rose */
            --warning: #F59E0B; /* Amber */
            --accent: #8B5CF6; /* Violet */
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: var(--bg-base); color: var(--text-main); font-family: 'Inter', sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }

        .header { height: 68px; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; padding: 0 32px; background: rgba(17, 24, 39, 0.95); z-index: 40; }
        .title-block h1 { font-size: 16px; font-weight: 600; letter-spacing: 0.5px; }
        .title-block span { font-size: 11px; color: var(--warning); font-family: 'JetBrains Mono'; font-weight: 600;}
        
        .filter-bar { padding: 12px 32px; border-bottom: 1px solid var(--border); display: flex; gap: 16px; align-items: center; background: rgba(31, 41, 55, 0.3); }
        .filter-group { display: flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 500; color: var(--text-muted); }
        .filter-select { background: var(--bg-base); color: var(--text-main); border: 1px solid var(--border); padding: 6px 12px; border-radius: 4px; font-family: 'Inter'; outline: none; cursor: pointer; font-size: 12px;}
        .filter-select:hover { border-color: var(--primary); }

        .scroll-area { flex: 1; overflow-y: auto; padding: 24px 32px; }
        .dashboard-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; }
        
        .panel { background: var(--bg-panel); border: 1px solid var(--border); border-radius: 8px; padding: 20px; display: flex; flex-direction: column; }
        .span-2 { grid-column: span 2; } .span-3 { grid-column: span 3; } .span-4 { grid-column: span 4; } .span-6 { grid-column: span 6; } .span-8 { grid-column: span 8; } .span-9 { grid-column: span 9; } .span-12 { grid-column: span 12; }
        .row-span-2 { grid-row: span 2; }

        .kpi-title { font-size: 11px; color: var(--text-muted); font-weight: 600; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;}
        .kpi-value { font-size: 26px; font-weight: 700; font-family: 'JetBrains Mono'; margin-bottom: 4px; }
        .kpi-desc { font-size: 11px; color: var(--text-muted); line-height: 1.4; border-top: 1px solid var(--border); padding-top: 8px; margin-top: 8px;}
        
        .pos { color: var(--positive); } .neg { color: var(--negative); }
        
        .chart-header { font-size: 14px; font-weight: 600; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
        .chart-container { height: 320px; width: 100%; } 

        .ai-panel { background: rgba(99, 102, 241, 0.05); border: 1px solid rgba(99, 102, 241, 0.2); }
        .ai-header { color: var(--primary); font-family: 'JetBrains Mono'; font-size: 12px; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;}
        .ai-bullet { font-size: 13px; line-height: 1.6; color: #D1D5DB; margin-bottom: 12px; padding-left: 12px; border-left: 2px solid var(--border); }
        .ai-bullet strong { color: #fff; }

        .data-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }
        .data-table th { padding: 12px; border-bottom: 1px solid var(--border); color: var(--text-muted); font-weight: 600; text-transform: uppercase; font-size: 11px; }
        .data-table td { padding: 12px; border-bottom: 1px solid rgba(31, 41, 55, 0.5); font-family: 'JetBrains Mono'; }
        
        .badge { padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 600; background: rgba(255,255,255,0.1); }
        .badge.critical { background: rgba(244, 63, 94, 0.2); color: var(--negative); }
        .badge.safe { background: rgba(16, 185, 129, 0.2); color: var(--positive); }
    </style>
</head>
<body>
    <div class="header">
        <div class="title-block">
            <h1>CUSTOMER RETENTION & REVENUE QUALITY</h1>
            <span>SYNTHETIC DATASET OVERLAY | Q3 2026</span>
        </div>
    </div>

    <div class="filter-bar">
        <div class="filter-group">
            Period: 
            <select class="filter-select" id="filterPeriod">
                <option value="Q3">Q3 2026 (Trailing)</option>
            </select>
        </div>
        <div class="filter-group">
            Segment: 
            <select class="filter-select" id="filterSegment">
                <option value="All">All Segments</option>
                <option value="Enterprise">Enterprise</option>
                <option value="Mid-Market">Mid-Market</option>
                <option value="SMB">SMB</option>
            </select>
        </div>
        <button class="filter-select" style="background:var(--primary); color:#fff; border:none;" onclick="renderDash()">Apply / Reset</button>
    </div>

    <div class="scroll-area">
        <div class="dashboard-grid">
            
            <!-- KPIs -->
            <div class="panel span-2">
                <div class="kpi-title">Net Revenue Retention (NRR)</div>
                <div class="kpi-value pos" id="kpiNRR">108.4%</div>
                <div class="kpi-desc">Beg MRR + Expand - Contract - Churn / Beg MRR. Target: >110%</div>
            </div>
            <div class="panel span-2">
                <div class="kpi-title">Gross Rev Retention (GRR)</div>
                <div class="kpi-value neg" id="kpiGRR">84.2%</div>
                <div class="kpi-desc">Excludes Expansion. Pure retention signal. Target: >90%</div>
            </div>
            <div class="panel span-2">
                <div class="kpi-title">Logo Churn Rate</div>
                <div class="kpi-value neg" id="kpiLogoChurn">12.5%</div>
                <div class="kpi-desc">Churned Customers / Active at Start. High due to SMB segment.</div>
            </div>
            <div class="panel span-2">
                <div class="kpi-title">Rev Churn Rate</div>
                <div class="kpi-value pos" id="kpiRevChurn">4.1%</div>
                <div class="kpi-desc">Lost MRR / Beg MRR. Lower than Logo Churn (SMB driven).</div>
            </div>
            <div class="panel span-4 ai-panel" style="grid-row: span 2;">
                <div class="ai-header">EXECUTIVE INSIGHT ENGINE (Q3 2026)</div>
                <div class="ai-bullet"><strong>🚨 The Churn Trap:</strong> Logo Churn is 12.5%, but Revenue Churn is only 4.1%. <i>Fact:</i> We lost 150 SMB customers (high logo churn), but only 1 Enterprise customer. SMB represents high noise, low MRR impact.</div>
                <div class="ai-bullet"><strong>⚠️ Revenue Concentration Risk:</strong> Top 5% of customers generate 42% of total MRR. <i>Evidence:</i> Pareto analysis shows heavy reliance on 3 massive Enterprise accounts. Losing one will tank NRR.</div>
                <div class="ai-bullet"><strong>✓ Growth Quality:</strong> Expansion Revenue ($145k) outpaced Contraction + Churn ($85k), keeping NRR > 100%.</div>
            </div>

            <!-- CHARTS -->
            <div class="panel span-8">
                <div class="chart-header">MRR Movement Bridge (Waterfall) <span style="font-size:11px; font-weight:400; color:var(--text-muted);">How revenue changed over Q3</span></div>
                <div id="chartWaterfall" class="chart-container"></div>
            </div>

            <div class="panel span-6">
                <div class="chart-header">Logo Churn vs Revenue Churn Paradox <span style="font-size:11px; font-weight:400; color:var(--text-muted);">Segment Vulnerability</span></div>
                <div id="chartTrap" class="chart-container"></div>
            </div>

            <div class="panel span-6">
                <div class="chart-header">MRR Concentration (Pareto Curve) <span style="font-size:11px; font-weight:400; color:var(--text-muted);">Top 10% Risk</span></div>
                <div id="chartPareto" class="chart-container"></div>
            </div>

            <div class="panel span-12">
                <div class="chart-header">Customer Logo Retention Cohort (Monthly) <span style="font-size:11px; font-weight:400; color:var(--text-muted);">Retention Decay Heatmap</span></div>
                <div id="chartCohort" class="chart-container" style="height: 400px;"></div>
            </div>

            <div class="panel span-12">
                <div class="chart-header">At-Risk Whale Customers (High MRR + Declining Usage)</div>
                <table class="data-table">
                    <thead>
                        <tr><th>Customer ID</th><th>Segment</th><th>Current MRR</th><th>Usage Drop (30d)</th><th>Support Tickets (Unresolved)</th><th>Risk State</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>#ENT-8902</td><td>Enterprise</td><td>$42,500</td><td class="neg">-45%</td><td>8 (Escalated)</td><td><span class="badge critical">CRITICAL CHURN RISK</span></td></tr>
                        <tr><td>#ENT-4122</td><td>Enterprise</td><td>$38,000</td><td class="neg">-12%</td><td>2</td><td><span class="badge safe">MONITORING</span></td></tr>
                        <tr><td>#MID-9921</td><td>Mid-Market</td><td>$8,400</td><td class="neg">-60%</td><td>1</td><td><span class="badge critical">HIGH RISK</span></td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        function renderDash() {
            try {
                if (typeof echarts === 'undefined') throw new Error("ECharts missing");

                const cWater = echarts.init(document.getElementById('chartWaterfall'));
                const cTrap = echarts.init(document.getElementById('chartTrap'));
                const cPareto = echarts.init(document.getElementById('chartPareto'));
                const cCohort = echarts.init(document.getElementById('chartCohort'));

                const txtColor = '#9CA3AF';
                const font = 'Inter';

                // 1. WATERFALL (MRR Bridge)
                // Data: Beg MRR (1.5M), New (200k), Expansion (145k), Contraction (-35k), Churn (-50k), End (1.76M)
                cWater.setOption({
                    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
                    grid: { left: '3%', right: '3%', bottom: '5%', top: '10%', containLabel: true },
                    xAxis: { type: 'category', data: ['Beg. MRR', 'New Logo', 'Expansion', 'Contraction', 'Churn', 'End MRR'], axisLabel: {color: txtColor} },
                    yAxis: { type: 'value', axisLabel: {color: txtColor, formatter: '${c}k', fontFamily: 'JetBrains Mono'}, splitLine: {lineStyle: {color: '#1F2937'}} },
                    series: [
                        { name: 'Transparent', type: 'bar', stack: 'Total', itemStyle: { borderColor: 'transparent', color: 'transparent' }, emphasis: { itemStyle: { borderColor: 'transparent', color: 'transparent' } }, data: [0, 1500, 1700, 1810, 1760, 0] },
                        { name: 'Increase', type: 'bar', stack: 'Total', itemStyle: { color: '#10B981', borderRadius: 2 }, data: [1500, 200, 145, 0, 0, 1760] },
                        { name: 'Decrease', type: 'bar', stack: 'Total', itemStyle: { color: '#F43F5E', borderRadius: 2 }, data: [0, 0, 0, 35, 50, 0] }
                    ]
                });

                // 2. THE CHURN TRAP (Logo vs Rev Churn)
                cTrap.setOption({
                    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
                    legend: { data: ['Logo Churn %', 'Revenue Churn %'], textStyle: {color: txtColor}, top: 0 },
                    grid: { left: '3%', right: '3%', bottom: '5%', top: '15%', containLabel: true },
                    xAxis: { type: 'category', data: ['SMB', 'Mid-Market', 'Enterprise'], axisLabel: {color: txtColor} },
                    yAxis: { type: 'value', axisLabel: {color: txtColor, formatter: '{value}%'}, splitLine: {lineStyle: {color: '#1F2937'}} },
                    series: [
                        { name: 'Logo Churn %', type: 'bar', barGap: '10%', itemStyle: { color: '#F59E0B' }, data: [22.5, 5.2, 1.1] },
                        { name: 'Revenue Churn %', type: 'bar', itemStyle: { color: '#F43F5E' }, data: [4.1, 8.5, 18.4] }
                    ]
                });

                // 3. PARETO CONCENTRATION
                cPareto.setOption({
                    tooltip: { trigger: 'axis' },
                    grid: { left: '3%', right: '5%', bottom: '5%', top: '10%', containLabel: true },
                    xAxis: { type: 'category', data: ['Top 1%', 'Top 5%', 'Top 10%', 'Top 20%', 'Bottom 80%'], axisLabel: {color: txtColor} },
                    yAxis: [
                        { type: 'value', name: 'MRR ($)', axisLabel: {color: txtColor, formatter: '${value}k', fontFamily: 'JetBrains Mono'}, splitLine: {lineStyle: {color: '#1F2937'}} },
                        { type: 'value', name: 'Cumulative %', axisLabel: {color: txtColor, formatter: '{value}%'}, splitLine: {show: false}, max: 100 }
                    ],
                    series: [
                        { name: 'MRR Segment', type: 'bar', itemStyle: { color: '#6366F1' }, data: [450, 350, 200, 150, 100] },
                        { name: 'Cumulative', type: 'line', yAxisIndex: 1, itemStyle: { color: '#10B981' }, data: [36, 64, 80, 92, 100] }
                    ]
                });

                // 4. COHORT HEATMAP
                const months = ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6'];
                const cohorts = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
                // Synthetic Retention Data [col, row, value]
                const heatmapData = [
                    [0,0,100], [1,0,94], [2,0,88], [3,0,85], [4,0,82], [5,0,80], [6,0,79],
                    [0,1,100], [1,1,92], [2,1,85], [3,1,81], [4,1,78], [5,1,75], [6,1,null],
                    [0,2,100], [1,2,95], [2,2,90], [3,2,88], [4,2,85], [5,2,null], [6,2,null],
                    [0,3,100], [1,3,91], [2,3,84], [3,3,80], [4,3,null], [5,3,null], [6,3,null],
                    [0,4,100], [1,4,88], [2,4,81], [3,4,null], [4,4,null], [5,4,null], [6,4,null],
                    [0,5,100], [1,5,92], [2,5,null], [3,5,null], [4,5,null], [5,5,null], [6,5,null]
                ];

                cCohort.setOption({
                    tooltip: { position: 'top', formatter: (p) => `${cohorts[p.data[1]]} at ${months[p.data[0]]}: ${p.data[2]}% retained` },
                    grid: { height: '80%', top: '5%', bottom: '15%' },
                    xAxis: { type: 'category', data: months, splitArea: { show: true } },
                    yAxis: { type: 'category', data: cohorts, splitArea: { show: true } },
                    visualMap: { min: 70, max: 100, calculable: true, orient: 'horizontal', left: 'center', bottom: '0%', 
                                 inRange: { color: ['#F43F5E', '#F59E0B', '#10B981', '#6366F1'] } },
                    series: [{
                        name: 'Retention %', type: 'heatmap', data: heatmapData,
                        label: { show: true, formatter: (p) => p.data[2] ? `${p.data[2]}%` : '' },
                        itemStyle: { borderColor: '#0B1120', borderWidth: 2 }
                    }]
                });

                window.addEventListener('resize', () => { cWater.resize(); cTrap.resize(); cPareto.resize(); cCohort.resize(); });
            } catch(e) {
                console.error(e);
                document.body.innerHTML += `<div style="position:fixed; top:0; left:0; right:0; padding:20px; background:#EF4444; color:#fff; z-index:9999;">JS ERROR: ${e.message}</div>`;
            }
        }
        setTimeout(renderDash, 300);
    </script>
</body>
</html>"""

final_html = html_template.replace("ECHARTS_INLINE_PAYLOAD", echarts_js)
file_path = r"C:\Users\ROG G532 LV\.gemini\antigravity\scratch\Senior-Data-Analyst\Final_Retention_Dashboard.html"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print("Retention Dashboard generated successfully at root.")
