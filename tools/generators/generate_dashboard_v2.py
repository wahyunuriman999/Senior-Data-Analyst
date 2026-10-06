import urllib.request

print("Downloading ECharts library...")
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
    <title>Executive Sales & Profitability V2</title>
    
    <!-- Q-VIS-FATAL: INLINE SCRIPT INJECTION (NO CDN) -->
    <script>
    ECHARTS_INLINE_PAYLOAD
    </script>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
        
        :root {
            --bg-base: #0B1120; /* Very Dark Slate */
            --bg-panel: #111827; /* Dark Slate */
            --border: #1F2937;
            --text-main: #F9FAFB;
            --text-muted: #9CA3AF;
            
            /* Restrained Executive Semantic Colors */
            --primary: #3B82F6; /* Corporate Blue */
            --positive: #10B981; /* Emerald */
            --negative: #EF4444; /* Rose */
            --warning: #F59E0B; /* Amber */
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: var(--bg-base); color: var(--text-main); font-family: 'Inter', sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }

        /* HEADER */
        .header { height: 68px; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; padding: 0 32px; background: rgba(17, 24, 39, 0.95); z-index: 40; }
        .title-block h1 { font-size: 16px; font-weight: 600; letter-spacing: 0.5px; }
        .title-block span { font-size: 11px; color: var(--text-muted); font-family: 'JetBrains Mono'; }
        
        .btn-filter { background: var(--primary); color: #fff; border: none; padding: 8px 16px; border-radius: 4px; font-size: 13px; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .btn-filter:hover { opacity: 0.9; }

        /* FILTER CHIPS */
        .filter-chips { padding: 10px 32px; border-bottom: 1px solid var(--border); display: flex; gap: 8px; align-items: center; background: rgba(31, 41, 55, 0.3); }
        .chip { background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2); color: var(--primary); padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 500; display: flex; align-items: center; gap: 6px; }
        .btn-clear { background: none; border: none; color: var(--text-muted); font-size: 11px; cursor: pointer; margin-left: auto; }

        /* GRID SYSTEM */
        .scroll-area { flex: 1; overflow-y: auto; padding: 24px 32px; }
        .dashboard-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; }
        
        .panel { background: var(--bg-panel); border: 1px solid var(--border); border-radius: 8px; padding: 20px; display: flex; flex-direction: column; }
        .span-2 { grid-column: span 2; } .span-4 { grid-column: span 4; } .span-6 { grid-column: span 6; } .span-8 { grid-column: span 8; } .span-12 { grid-column: span 12; }
        .row-span-2 { grid-row: span 2; }

        /* KPIs */
        .kpi-title { font-size: 12px; color: var(--text-muted); font-weight: 600; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;}
        .kpi-value { font-size: 26px; font-weight: 700; font-family: 'JetBrains Mono'; margin-bottom: 4px; }
        .kpi-delta { font-size: 12px; font-weight: 500; display: flex; align-items: center; gap: 4px; }
        .pos { color: var(--positive); } .neg { color: var(--negative); }
        
        /* CHARTS (Q-VIS-FATAL: Explicit Sizing) */
        .chart-header { font-size: 14px; font-weight: 600; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
        .chart-container { height: 320px; width: 100%; } /* EXPLICIT HEIGHT MANDATORY */

        /* AI EXCEPTION PANEL */
        .ai-panel { background: rgba(59, 130, 246, 0.03); border: 1px solid rgba(59, 130, 246, 0.15); }
        .ai-header { color: var(--primary); font-family: 'JetBrains Mono'; font-size: 12px; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;}
        .ai-header::before { content: ''; width: 8px; height: 8px; background: var(--primary); border-radius: 50%; box-shadow: 0 0 8px var(--primary); }
        .ai-bullet { font-size: 13px; line-height: 1.6; color: #D1D5DB; margin-bottom: 12px; padding-left: 12px; border-left: 2px solid var(--border); }
        .ai-bullet strong { color: #fff; }

        /* DATA TABLE */
        .data-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }
        .data-table th { padding: 12px; border-bottom: 1px solid var(--border); color: var(--text-muted); font-weight: 600; text-transform: uppercase; font-size: 11px; }
        .data-table td { padding: 12px; border-bottom: 1px solid rgba(31, 41, 55, 0.5); font-family: 'JetBrains Mono'; }
        .data-table tr:hover { background: rgba(255,255,255,0.02); }

    </style>
</head>
<body>
    <div class="header">
        <div class="title-block">
            <h1>EXECUTIVE SALES & PROFITABILITY</h1>
            <span>MULTI-REGION CONSOLIDATED | YTD 2026 | SECURE RENDER MODE</span>
        </div>
        <button class="btn-filter">Intelligent Filters [3]</button>
    </div>

    <div class="filter-chips">
        <span style="font-size:11px; color:var(--text-muted); font-weight:600;">ACTIVE FILTERS:</span>
        <div class="chip">Date: YTD 2026 <span>×</span></div>
        <div class="chip">Segment: B2B Enterprise <span>×</span></div>
        <div class="chip">Channel: Direct Sales <span>×</span></div>
        <button class="btn-clear">Clear All</button>
    </div>

    <div class="scroll-area">
        <div class="dashboard-grid">
            
            <!-- 1. EXECUTIVE KPIs -->
            <div class="panel span-2"><div class="kpi-title">Gross Revenue</div><div class="kpi-value">$84.2M</div><div class="kpi-delta pos">▲ 12.4% YoY</div></div>
            <div class="panel span-2"><div class="kpi-title">Net Profit</div><div class="kpi-value">$14.5M</div><div class="kpi-delta neg">▼ -1.2% YoY</div></div>
            <div class="panel span-2"><div class="kpi-title">Profit Margin</div><div class="kpi-value">17.2%</div><div class="kpi-delta neg">▼ -2.1% pts</div></div>
            <div class="panel span-2"><div class="kpi-title">Total Orders</div><div class="kpi-value">245k</div><div class="kpi-delta pos">▲ 15.8% YoY</div></div>
            <div class="panel span-2"><div class="kpi-title">Avg Order Val</div><div class="kpi-value">$343</div><div class="kpi-delta neg">▼ -3.1% YoY</div></div>
            <div class="panel span-2"><div class="kpi-title">Cust. CAC</div><div class="kpi-value">$120</div><div class="kpi-delta neg">▲ 18.5% YoY (Worse)</div></div>

            <!-- 2. TREND ANALYSIS -->
            <div class="panel span-8 row-span-2">
                <div class="chart-header">Revenue vs Profit Trend (Trailing 12M) <span style="font-size:11px; color:var(--text-muted); font-weight:400;">Grain: Monthly Aggregation</span></div>
                <div id="chartTrend" class="chart-container"></div>
            </div>

            <!-- 6. ANOMALY / STORYTELLING -->
            <div class="panel span-4 row-span-2 ai-panel">
                <div class="ai-header">EXECUTIVE EXCEPTIONS (AI DETECTED)</div>
                <div class="ai-bullet"><strong>⚠️ Margin Squeeze:</strong> Top-line revenue is growing (+12.4%), but net profit is shrinking (-1.2%). Growth is currently unprofitable due to soaring CAC.</div>
                <div class="ai-bullet"><strong>📍 APAC Anomaly:</strong> APAC region is driving massive volume but operating at a severe 4.2% margin trap due to heavy discounting and supply chain tariffs.</div>
                <div class="ai-bullet"><strong>📦 Product Driver:</strong> 'Electronics' subcategory drove the highest revenue growth, but 'Apparel' generated 60% of the net profit pool.</div>
            </div>

            <!-- 3. REGION CONTRIBUTION -->
            <div class="panel span-4 row-span-2">
                <div class="chart-header">Regional Contribution (Revenue & Margin)</div>
                <div id="chartRegion" class="chart-container"></div>
            </div>

            <!-- 4. PRODUCT DRIVERS (WATERFALL) -->
            <div class="panel span-8 row-span-2">
                <div class="chart-header">Subcategory Drivers (Net Profit Growth YoY) <span style="font-size:11px; color:var(--text-muted); font-weight:400;">Variance Analysis</span></div>
                <div id="chartWaterfall" class="chart-container"></div>
            </div>

            <!-- 5. REVENUE VS PROFITABILITY (SCATTER) -->
            <div class="panel span-12 row-span-2">
                <div class="chart-header">Revenue vs Profitability Paradox (Subcategories) <span style="font-size:11px; color:var(--text-muted); font-weight:400;">Quadrant Analysis (Bubble Size = Orders)</span></div>
                <div id="chartScatter" class="chart-container"></div>
            </div>

            <!-- 7. DETAIL TABLE -->
            <div class="panel span-12">
                <div class="chart-header">Detail View: High-Risk Subcategories (Negative Margin or Dropping YoY)</div>
                <table class="data-table">
                    <thead>
                        <tr><th>Subcategory</th><th>Primary Region</th><th>Revenue</th><th>Cost</th><th>Net Profit</th><th>Margin %</th><th>YoY Growth</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Enterprise Servers</td><td>APAC</td><td>$18,450,000</td><td>$18,850,000</td><td class="neg">-$400,000</td><td class="neg">-2.1%</td><td class="pos">+25.0%</td></tr>
                        <tr><td>Legacy Hardware</td><td>NA</td><td>$4,100,000</td><td>$4,800,000</td><td class="neg">-$700,000</td><td class="neg">-17.0%</td><td class="neg">-15.4%</td></tr>
                        <tr><td>Network Cables</td><td>EMEA</td><td>$2,200,000</td><td>$2,100,000</td><td class="pos">$100,000</td><td class="neg">4.5%</td><td class="neg">-8.2%</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // Q-VIS-FATAL: NO DOMContentLoaded. Execute via setTimeout to guarantee IDE injection completion.
        function renderDash() {
            try {
                if (typeof echarts === 'undefined') throw new Error("ECharts library missing");

                const cTrend = echarts.init(document.getElementById('chartTrend'));
                const cRegion = echarts.init(document.getElementById('chartRegion'));
                const cWaterfall = echarts.init(document.getElementById('chartWaterfall'));
                const cScatter = echarts.init(document.getElementById('chartScatter'));

                const txtColor = '#9CA3AF';
                const font = 'Inter';

                // 2. TREND (Dual Axis)
                cTrend.setOption({
                    tooltip: { trigger: 'axis' },
                    legend: { data: ['Revenue ($M)', 'Profit ($M)'], textStyle: {color: txtColor, fontFamily: font}, top: 0 },
                    grid: { left: '3%', right: '3%', bottom: '5%', top: '15%', containLabel: true },
                    xAxis: { type: 'category', data: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'], axisLabel: {color: txtColor} },
                    yAxis: [
                        { type: 'value', splitLine: {lineStyle: {color: '#1F2937'}}, axisLabel: {color: txtColor, fontFamily: 'JetBrains Mono'} },
                        { type: 'value', splitLine: {show: false}, axisLabel: {color: txtColor, fontFamily: 'JetBrains Mono'} }
                    ],
                    series: [
                        { name: 'Revenue ($M)', type: 'line', smooth: true, yAxisIndex: 0,
                          itemStyle: { color: '#3B82F6' }, areaStyle: { color: 'rgba(59, 130, 246, 0.2)' },
                          data: [5.1, 5.5, 5.8, 6.2, 7.5, 7.4, 7.8, 8.2, 8.5, 8.1, 8.8, 9.2]
                        },
                        { name: 'Profit ($M)', type: 'line', smooth: true, yAxisIndex: 1,
                          itemStyle: { color: '#10B981' }, areaStyle: { color: 'rgba(16, 185, 129, 0.2)' },
                          data: [1.5, 1.6, 1.7, 1.8, 1.8, 1.7, 1.7, 1.6, 1.5, 1.3, 1.2, 1.1] // Margin squeezing
                        }
                    ]
                });

                // 3. REGIONAL BAR
                cRegion.setOption({
                    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
                    grid: { left: '3%', right: '15%', bottom: '5%', top: '5%', containLabel: true },
                    xAxis: { type: 'value', show: false },
                    yAxis: { type: 'category', data: ['LATAM', 'EMEA', 'NA', 'APAC'], axisLabel: {color: txtColor}, axisLine: {show:false}, axisTick: {show:false} },
                    series: [{
                        type: 'bar',
                        data: [
                            { value: 12.5, itemStyle: {color: '#10B981'} }, // High margin
                            { value: 18.2, itemStyle: {color: '#3B82F6'} }, // Normal
                            { value: 25.5, itemStyle: {color: '#3B82F6'} },
                            { value: 28.0, itemStyle: {color: '#EF4444'} }  // High Rev, Negative/Low Margin (Trap)
                        ],
                        label: { show: true, position: 'right', color: txtColor, formatter: '${c}M', fontFamily: 'JetBrains Mono' },
                        itemStyle: { borderRadius: [0, 4, 4, 0] }
                    }]
                });

                // 4. PRODUCT DRIVERS (WATERFALL)
                const base = [0, 1.2, 2.7, 3.2, 3.8, 2.5, 0];
                cWaterfall.setOption({
                    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
                    grid: { left: '3%', right: '3%', bottom: '5%', top: '10%', containLabel: true },
                    xAxis: { type: 'category', data: ['Last Year', 'Apparel', 'Software', 'Services', 'Hardware', 'Servers', 'This Year'], axisLabel: {color: txtColor} },
                    yAxis: { type: 'value', axisLabel: {color: txtColor, fontFamily: 'JetBrains Mono'}, splitLine: {lineStyle: {color: '#1F2937'}} },
                    series: [
                        { name: 'Placeholder', type: 'bar', stack: 'Total', itemStyle: { borderColor: 'transparent', color: 'transparent' }, emphasis: { itemStyle: { borderColor: 'transparent', color: 'transparent' } }, data: [0, 14.7, 15.9, 17.4, 17.9, 14.5, 0] },
                        { name: 'Gain', type: 'bar', stack: 'Total', itemStyle: { color: '#10B981', borderRadius: 2 }, data: [0, 1.2, 1.5, 0.5, 0, 0, 0] },
                        { name: 'Loss', type: 'bar', stack: 'Total', itemStyle: { color: '#EF4444', borderRadius: 2 }, data: [0, 0, 0, 0, -3.4, 0, 0] },
                        { name: 'Total', type: 'bar', stack: 'Total', itemStyle: { color: '#3B82F6', borderRadius: 2 }, data: [14.7, 0, 0, 0, 0, 0, 14.5] }
                    ]
                });

                // 5. REVENUE VS MARGIN PARADOX (SCATTER)
                const scatterData = [
                    [18.4, -2.1, 1200, 'Enterprise Servers'], [14.2, 74.3, 800, 'Cloud Licenses'],
                    [12.4, 25.9, 1500, 'Apparel'], [8.1, 80.6, 400, 'Security Software'],
                    [4.1, -17.0, 300, 'Legacy Hardware'], [16.5, 12.4, 2000, 'Support Contracts'],
                    [9.2, 45.1, 600, 'Analytics API'], [5.8, 5.2, 900, 'Training Services']
                ];
                
                cScatter.setOption({
                    tooltip: { formatter: (p) => `${p.data[3]}<br/>Rev: $${p.data[0]}M<br/>Margin: ${p.data[1]}%` },
                    grid: { left: '5%', right: '5%', bottom: '10%', top: '10%', containLabel: true },
                    xAxis: { name: 'Revenue ($M)', nameLocation: 'middle', nameGap: 25, type: 'value', axisLabel: {color: txtColor, fontFamily: 'JetBrains Mono'}, splitLine: {lineStyle: {color: '#1F2937'}} },
                    yAxis: { name: 'Net Margin (%)', nameLocation: 'middle', nameGap: 30, type: 'value', axisLabel: {color: txtColor, fontFamily: 'JetBrains Mono'}, splitLine: {lineStyle: {color: '#1F2937', type:'dashed'}} },
                    series: [{
                        type: 'scatter',
                        data: scatterData,
                        symbolSize: (data) => Math.sqrt(data[2]) * 1.5,
                        itemStyle: { color: (params) => params.data[1] < 0 ? '#EF4444' : (params.data[1] > 40 ? '#10B981' : '#3B82F6'), opacity: 0.8, borderColor: '#0B1120', borderWidth: 1 },
                        markLine: { symbol: ['none', 'none'], label: { show: false }, lineStyle: { color: '#4B5563', type: 'dashed', width: 1 }, data: [ { xAxis: 10 }, { yAxis: 20 } ] }
                    }]
                });

                window.addEventListener('resize', () => { cTrend.resize(); cRegion.resize(); cWaterfall.resize(); cScatter.resize(); });
            } catch(e) {
                console.error("Dashboard render error:", e);
                document.body.innerHTML += `<div style="position:fixed; top:0; left:0; right:0; padding:20px; background:#EF4444; color:#fff; font-family:monospace; z-index:9999;">JS ERROR: ${e.message}</div>`;
            }
        }

        setTimeout(renderDash, 300);
    </script>
</body>
</html>"""

final_html = html_template.replace("ECHARTS_INLINE_PAYLOAD", echarts_js)

file_path = r"C:\Users\ROG G532 LV\.gemini\antigravity\brain\3ed9f1b4-c6cf-43cb-a6a5-3bdfd69ebeeb\apex_executive_sales_v2.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print("HTML Dashboard V2 successfully generated using strict Q-VIS-FATAL protocol.")
