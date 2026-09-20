import urllib.request
import re

print("Downloading ECharts library for V3...")
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
    <title>Executive Sales & Profitability V3 - Analytical Engine</title>
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
            --primary: #3B82F6; 
            --positive: #10B981; 
            --negative: #EF4444; 
            --warning: #F59E0B; 
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: var(--bg-base); color: var(--text-main); font-family: 'Inter', sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }

        .header { height: 68px; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; padding: 0 32px; background: var(--bg-panel); z-index: 40; }
        .title-block h1 { font-size: 16px; font-weight: 600; letter-spacing: 0.5px; }
        .title-block span { font-size: 11px; color: var(--text-muted); font-family: 'JetBrains Mono'; }
        
        /* FILTERS BAR */
        .filter-bar { padding: 12px 32px; border-bottom: 1px solid var(--border); display: flex; gap: 16px; align-items: center; background: rgba(17, 24, 39, 0.5); }
        .filter-group { display: flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 500; color: var(--text-muted); }
        .filter-select { background: var(--bg-base); color: var(--text-main); border: 1px solid var(--border); padding: 4px 8px; border-radius: 4px; font-family: 'Inter'; outline: none; cursor: pointer;}
        
        /* GRID SYSTEM */
        .scroll-area { flex: 1; overflow-y: auto; padding: 24px 32px; position: relative; }
        .dashboard-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; }
        
        .panel { background: var(--bg-panel); border: 1px solid var(--border); border-radius: 8px; padding: 20px; display: flex; flex-direction: column; }
        .span-2 { grid-column: span 2; } .span-4 { grid-column: span 4; } .span-6 { grid-column: span 6; } .span-8 { grid-column: span 8; } .span-12 { grid-column: span 12; }
        .row-span-2 { grid-row: span 2; }

        .kpi-title { font-size: 12px; color: var(--text-muted); font-weight: 600; margin-bottom: 6px; text-transform: uppercase; }
        .kpi-value { font-size: 26px; font-weight: 700; font-family: 'JetBrains Mono'; margin-bottom: 4px; }
        .pos { color: var(--positive); } .neg { color: var(--negative); }
        
        .chart-header { font-size: 14px; font-weight: 600; margin-bottom: 16px; display: flex; justify-content: space-between; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
        .chart-container { height: 320px; width: 100%; } 

        .ai-panel { background: rgba(59, 130, 246, 0.03); border: 1px solid rgba(59, 130, 246, 0.15); }
        .ai-header { color: var(--primary); font-family: 'JetBrains Mono'; font-size: 12px; font-weight: 700; margin-bottom: 12px; }
        .ai-bullet { font-size: 13px; line-height: 1.6; color: #D1D5DB; margin-bottom: 12px; padding-left: 12px; border-left: 2px solid var(--border); }
        .ai-bullet strong { color: #fff; }

        .empty-state { position: absolute; inset: 0; background: rgba(11, 17, 32, 0.9); z-index: 50; display: none; flex-direction: column; align-items: center; justify-content: center; }
        .empty-state h2 { font-size: 20px; margin-bottom: 10px; }
        .empty-state p { color: var(--text-muted); font-size: 14px; }
    </style>
</head>
<body>
    <div class="header">
        <div class="title-block">
            <h1>EXECUTIVE SALES & PROFITABILITY V3</h1>
            <span>ANALYTICAL ENGINE | REAL-TIME FILTERING</span>
        </div>
    </div>

    <div class="filter-bar">
        <div class="filter-group">
            Region: 
            <select class="filter-select" id="filterRegion">
                <option value="All">All Regions</option>
                <option value="APAC">APAC</option>
                <option value="NA">North America</option>
                <option value="EMEA">EMEA</option>
                <option value="LATAM">LATAM</option>
            </select>
        </div>
        <div class="filter-group">
            Category: 
            <select class="filter-select" id="filterCategory">
                <option value="All">All Categories</option>
                <option value="Hardware">Hardware</option>
                <option value="Software">Software</option>
                <option value="Services">Services</option>
            </select>
        </div>
        <button class="filter-select" style="background:var(--primary); color:#fff; border:none;" onclick="resetFilters()">Clear All</button>
    </div>

    <div class="scroll-area">
        <div class="empty-state" id="emptyState">
            <h2>Zero Results</h2>
            <p>No data matches the current filters. Please adjust Region or Category.</p>
            <button class="filter-select" style="margin-top:20px; background:var(--primary); color:#fff;" onclick="resetFilters()">Reset Filters</button>
        </div>

        <div class="dashboard-grid">
            <div class="panel span-2"><div class="kpi-title">Revenue</div><div class="kpi-value" id="kpiRev">--</div></div>
            <div class="panel span-2"><div class="kpi-title">Net Profit</div><div class="kpi-value" id="kpiProf">--</div></div>
            <div class="panel span-2"><div class="kpi-title">Profit Margin</div><div class="kpi-value" id="kpiMar">--</div></div>
            <div class="panel span-2"><div class="kpi-title">Total Orders</div><div class="kpi-value" id="kpiOrd">--</div></div>
            <div class="panel span-4 ai-panel" style="grid-row: span 2;">
                <div class="ai-header">DYNAMIC EXCEPTIONS</div>
                <div id="aiInsights">Initializing...</div>
            </div>

            <div class="panel span-8">
                <div class="chart-header">Revenue vs Profitability Paradox (Subcategories)</div>
                <div id="chartScatter" class="chart-container"></div>
            </div>
            
            <div class="panel span-12">
                <div class="chart-header">Regional Breakdown</div>
                <div id="chartRegion" class="chart-container" style="height: 250px;"></div>
            </div>
        </div>
    </div>

    <script>
        // ANALYTICAL ENGINE V3
        // Data Grain: Monthly, Regional, Subcategory Aggregates
        const rawData = [
            { region: 'APAC', cat: 'Hardware', sub: 'Servers', rev: 12.4, prof: -0.4, ord: 1200 },
            { region: 'APAC', cat: 'Software', sub: 'Licenses', rev: 3.2, prof: 2.1, ord: 400 },
            { region: 'NA', cat: 'Software', sub: 'Cloud', rev: 8.2, prof: 6.1, ord: 800 },
            { region: 'NA', cat: 'Hardware', sub: 'Legacy', rev: 4.1, prof: -0.7, ord: 300 },
            { region: 'EMEA', cat: 'Services', sub: 'Support', rev: 6.5, prof: 1.2, ord: 2000 },
            { region: 'EMEA', cat: 'Hardware', sub: 'Cables', rev: 2.2, prof: 0.1, ord: 1500 },
            { region: 'LATAM', cat: 'Software', sub: 'Security', rev: 3.1, prof: 2.5, ord: 400 },
            { region: 'LATAM', cat: 'Services', sub: 'Training', rev: 1.8, prof: 0.8, ord: 900 }
        ];

        let cScatter, cRegion;

        function init() {
            cScatter = echarts.init(document.getElementById('chartScatter'));
            cRegion = echarts.init(document.getElementById('chartRegion'));
            window.addEventListener('resize', () => { cScatter.resize(); cRegion.resize(); });
            
            document.getElementById('filterRegion').addEventListener('change', updateDash);
            document.getElementById('filterCategory').addEventListener('change', updateDash);
            
            updateDash();
        }

        function resetFilters() {
            document.getElementById('filterRegion').value = 'All';
            document.getElementById('filterCategory').value = 'All';
            updateDash();
        }

        function updateDash() {
            const reg = document.getElementById('filterRegion').value;
            const cat = document.getElementById('filterCategory').value;
            
            // Filter Logic
            const filtered = rawData.filter(d => (reg === 'All' || d.region === reg) && (cat === 'All' || d.cat === cat));
            
            // Empty State Handling
            if (filtered.length === 0) {
                document.getElementById('emptyState').style.display = 'flex';
                return;
            } else {
                document.getElementById('emptyState').style.display = 'none';
            }

            // Metric Calculation (SAFE AGGREGATION: SUM(Profit)/SUM(Revenue))
            const totalRev = filtered.reduce((sum, d) => sum + d.rev, 0);
            const totalProf = filtered.reduce((sum, d) => sum + d.prof, 0);
            const totalOrd = filtered.reduce((sum, d) => sum + d.ord, 0);
            const margin = totalRev > 0 ? (totalProf / totalRev) * 100 : 0;

            document.getElementById('kpiRev').innerText = `$${totalRev.toFixed(1)}M`;
            document.getElementById('kpiProf').innerText = `$${totalProf.toFixed(1)}M`;
            
            const marEl = document.getElementById('kpiMar');
            marEl.innerText = `${margin.toFixed(1)}%`;
            marEl.className = `kpi-value ${margin < 10 ? 'neg' : 'pos'}`;
            
            document.getElementById('kpiOrd').innerText = `${(totalOrd/1000).toFixed(1)}k`;

            // Exception Engine (AI Narrative Generator based on FACT)
            let insights = "";
            if (margin < 5) {
                insights += `<div class="ai-bullet"><strong>🚨 CRITICAL: Margin Collapse.</strong> Current selection operates at ${margin.toFixed(1)}% margin. Severe profitability risk.</div>`;
            }
            if (filtered.some(d => d.rev > 10 && d.prof < 0)) {
                insights += `<div class="ai-bullet"><strong>⚠️ The Growth Paradox.</strong> Found subcategories with >$10M revenue but NEGATIVE profit. Volume is destroying value.</div>`;
            }
            if (filtered.length === rawData.length) {
                insights += `<div class="ai-bullet"><strong>ℹ️ Global View Active.</strong> North America drives software profit, while APAC creates a hardware margin trap. Filter by region to isolate.</div>`;
            }
            if (!insights) insights = `<div class="ai-bullet"><strong>✓ Stable.</strong> Metrics are within nominal analytical bounds for this slice.</div>`;
            document.getElementById('aiInsights').innerHTML = insights;

            // Chart 1: Scatter Paradox
            const scatterData = filtered.map(d => [d.rev, (d.prof/d.rev)*100, d.ord, d.sub]);
            cScatter.setOption({
                tooltip: { formatter: (p) => `${p.data[3]}<br/>Rev: $${p.data[0].toFixed(1)}M<br/>Margin: ${p.data[1].toFixed(1)}%` },
                grid: { left: '5%', right: '5%', bottom: '10%', top: '10%', containLabel: true },
                xAxis: { name: 'Revenue ($M)', nameLocation: 'middle', nameGap: 25, type: 'value', splitLine: {lineStyle: {color: '#1F2937'}} },
                yAxis: { name: 'Margin (%)', nameLocation: 'middle', nameGap: 30, type: 'value', splitLine: {lineStyle: {color: '#1F2937', type:'dashed'}} },
                series: [{
                    type: 'scatter', data: scatterData,
                    symbolSize: (data) => Math.sqrt(data[2]) * 1.5,
                    itemStyle: { color: (p) => p.data[1] < 0 ? '#EF4444' : '#3B82F6', opacity: 0.8 }
                }]
            });

            // Chart 2: Regional Aggregation
            const regMap = {};
            filtered.forEach(d => { if(!regMap[d.region]) regMap[d.region]=0; regMap[d.region] += d.rev; });
            const regNames = Object.keys(regMap);
            const regVals = Object.values(regMap);
            
            cRegion.setOption({
                tooltip: { trigger: 'axis' },
                grid: { left: '3%', right: '5%', bottom: '5%', top: '5%', containLabel: true },
                xAxis: { type: 'value', splitLine: {show:false} },
                yAxis: { type: 'category', data: regNames, axisLabel: {color: '#9CA3AF'} },
                series: [{ type: 'bar', data: regVals, itemStyle: {color: '#10B981'}, label: {show:true, position:'right', formatter:'${c}M'} }]
            });
        }

        setTimeout(init, 300);
    </script>
</body>
</html>"""

final_html = html_template.replace("ECHARTS_INLINE_PAYLOAD", echarts_js)

file_path = r"C:\Users\ROG G532 LV\.gemini\antigravity\scratch\Senior-Data-Analyst\Final_Executive_Dashboard_V3.html"
with open(file_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print("V3 Generated successfully.")
