import urllib.request

print("Downloading ECharts library for Forensic Retention Dashboard...")
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
    <title>Customer Retention - Forensic Analytical Engine</title>
    <script>ECHARTS_INLINE_PAYLOAD</script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
        :root {
            --bg-base: #0B1120; --bg-panel: #111827; --border: #1F2937;
            --text-main: #F9FAFB; --text-muted: #9CA3AF;
            --primary: #6366F1; --positive: #10B981; --negative: #F43F5E; --warning: #F59E0B;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: var(--bg-base); color: var(--text-main); font-family: 'Inter', sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        .header { height: 68px; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; padding: 0 32px; background: rgba(17, 24, 39, 0.95); z-index: 40; }
        .title-block h1 { font-size: 16px; font-weight: 600; }
        .title-block span { font-size: 11px; color: var(--positive); font-family: 'JetBrains Mono'; font-weight: 600;}
        .filter-bar { padding: 12px 32px; border-bottom: 1px solid var(--border); display: flex; gap: 16px; align-items: center; background: rgba(31, 41, 55, 0.3); }
        .filter-group { display: flex; align-items: center; gap: 8px; font-size: 12px; font-weight: 500; color: var(--text-muted); }
        .filter-select { background: var(--bg-base); color: var(--text-main); border: 1px solid var(--border); padding: 6px 12px; border-radius: 4px; font-family: 'Inter'; outline: none; cursor: pointer; font-size: 12px;}
        .scroll-area { flex: 1; overflow-y: auto; padding: 24px 32px; position: relative;}
        .dashboard-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 20px; }
        .panel { background: var(--bg-panel); border: 1px solid var(--border); border-radius: 8px; padding: 20px; display: flex; flex-direction: column; }
        .span-2 { grid-column: span 2; } .span-3 { grid-column: span 3; } .span-4 { grid-column: span 4; } .span-6 { grid-column: span 6; } .span-8 { grid-column: span 8; } .span-12 { grid-column: span 12; }
        .row-span-2 { grid-row: span 2; }
        .kpi-title { font-size: 11px; color: var(--text-muted); font-weight: 600; margin-bottom: 6px; text-transform: uppercase;}
        .kpi-value { font-size: 24px; font-weight: 700; font-family: 'JetBrains Mono'; margin-bottom: 4px; }
        .kpi-desc { font-size: 10px; color: var(--text-muted); line-height: 1.4; border-top: 1px solid var(--border); padding-top: 8px; margin-top: 8px;}
        .pos { color: var(--positive); } .neg { color: var(--negative); }
        .chart-header { font-size: 14px; font-weight: 600; margin-bottom: 16px; display: flex; justify-content: space-between; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
        .chart-container { height: 320px; width: 100%; }
        .ai-panel { background: rgba(99, 102, 241, 0.05); border: 1px solid rgba(99, 102, 241, 0.2); }
        .ai-header { color: var(--primary); font-family: 'JetBrains Mono'; font-size: 12px; font-weight: 700; margin-bottom: 12px;}
        .ai-bullet { font-size: 13px; line-height: 1.6; color: #D1D5DB; margin-bottom: 12px; padding-left: 12px; border-left: 2px solid var(--border); }
        .ai-bullet strong { color: #fff; }
        .data-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }
        .data-table th { padding: 12px; border-bottom: 1px solid var(--border); color: var(--text-muted); font-weight: 600; text-transform: uppercase; font-size: 11px; }
        .data-table td { padding: 12px; border-bottom: 1px solid rgba(31, 41, 55, 0.5); font-family: 'JetBrains Mono'; }
        .badge { padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: 600; background: rgba(255,255,255,0.1); }
        .badge.critical { background: rgba(244, 63, 94, 0.2); color: var(--negative); }
        .badge.warning { background: rgba(245, 158, 11, 0.2); color: var(--warning); }
        .empty-state { position: absolute; inset: 0; background: rgba(11, 17, 32, 0.9); z-index: 50; display: none; flex-direction: column; align-items: center; justify-content: center; }
    </style>
</head>
<body>
    <div class="header">
        <div class="title-block">
            <h1>CUSTOMER RETENTION & REVENUE QUALITY V2</h1>
            <span>FORENSIC RECONCILIATION ENGINE | TRUE SINGLE SOURCE OF TRUTH</span>
        </div>
    </div>

    <div class="filter-bar">
        <div class="filter-group">
            Segment: 
            <select class="filter-select" id="filterSegment">
                <option value="All">All Segments</option>
                <option value="Enterprise">Enterprise</option>
                <option value="Mid-Market">Mid-Market</option>
                <option value="SMB">SMB</option>
            </select>
        </div>
        <button class="filter-select" style="background:var(--primary); color:#fff; border:none;" onclick="applyFilters()">Recalculate Entire Engine</button>
    </div>

    <div class="scroll-area">
        <div class="empty-state" id="emptyState">
            <h2>Zero Results</h2>
            <p>No customers match the current filter.</p>
        </div>

        <div class="dashboard-grid" id="mainGrid">
            <!-- KPIs -->
            <div class="panel span-2"><div class="kpi-title">Net Rev Retention (NRR)</div><div class="kpi-value" id="kpiNRR">--</div><div class="kpi-desc">(Beg+Exp-Cont-Churn)/Beg</div></div>
            <div class="panel span-2"><div class="kpi-title">Gross Rev Retention</div><div class="kpi-value" id="kpiGRR">--</div><div class="kpi-desc">(Beg-Cont-Churn)/Beg</div></div>
            <div class="panel span-2"><div class="kpi-title">Logo Churn Rate</div><div class="kpi-value" id="kpiLogoChurn">--</div><div class="kpi-desc">Churned Logos / Beg Logos</div></div>
            <div class="panel span-2"><div class="kpi-title">Revenue Churn Rate</div><div class="kpi-value" id="kpiRevChurn">--</div><div class="kpi-desc">Churned MRR / Beg MRR</div></div>
            
            <!-- EXCEPTION ENGINE -->
            <div class="panel span-4 ai-panel" style="grid-row: span 2;">
                <div class="ai-header">OBSERVED INSIGHTS (EVIDENCE-BASED)</div>
                <div id="aiInsights">Calculating...</div>
            </div>

            <!-- WATERFALL -->
            <div class="panel span-8">
                <div class="chart-header">MRR Movement Bridge <span style="font-size:11px; font-weight:400; color:var(--text-muted);">Exact Reconciliation</span></div>
                <div id="chartWaterfall" class="chart-container"></div>
            </div>

            <!-- CHURN TRAP -->
            <div class="panel span-4">
                <div class="chart-header">Logo vs Rev Churn (%)</div>
                <div id="chartTrap" class="chart-container"></div>
            </div>

            <!-- PARETO -->
            <div class="panel span-8">
                <div class="chart-header">MRR Concentration (Pareto) <span style="font-size:11px; font-weight:400; color:var(--text-muted);">Cumulative Revenue by Customer Percentile</span></div>
                <div id="chartPareto" class="chart-container"></div>
            </div>

            <!-- RISK TABLE -->
            <div class="panel span-12">
                <div class="chart-header">At-Risk Active Customers <span style="font-size:11px; font-weight:400; color:var(--text-muted);">Rule: UsageDrop > 40% OR Tickets >= 5</span></div>
                <table class="data-table">
                    <thead><tr><th>Customer ID</th><th>Segment</th><th>Beg MRR</th><th>Usage Drop</th><th>Tickets</th><th>Risk State</th></tr></thead>
                    <tbody id="riskTableBody"></tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        // SINGLE SOURCE OF TRUTH: Customer-Level Raw Data Array
        // Cohort Index: 0=Jan, 1=Feb, 2=Mar. ActiveMonths: how many months they stayed before churning (or 6 if active).
        const rawCustomerData = [
            // Enterprise (Low Logo count, Massive MRR. Low Logo Churn, High Rev Churn if one drops)
            { id: 'ENT-01', seg: 'Enterprise', isNew: false, isChurn: false, begMrr: 50000, endMrr: 60000, tix: 2, drop: 0, cohort: 0, activeM: 6 },
            { id: 'ENT-02', seg: 'Enterprise', isNew: false, isChurn: true,  begMrr: 45000, endMrr: 0,     tix: 8, drop: 60, cohort: 0, activeM: 3 }, // Massive Churn
            { id: 'ENT-03', seg: 'Enterprise', isNew: false, isChurn: false, begMrr: 40000, endMrr: 35000, tix: 1, drop: 10, cohort: 1, activeM: 6 }, // Contraction
            { id: 'ENT-04', seg: 'Enterprise', isNew: true,  isChurn: false, begMrr: 0,     endMrr: 38000, tix: 0, drop: 0, cohort: 5, activeM: 1 }, // New
            { id: 'ENT-05', seg: 'Enterprise', isNew: false, isChurn: false, begMrr: 42000, endMrr: 42000, tix: 6, drop: 45, cohort: 0, activeM: 6 }, // AT RISK!
            // Mid-Market
            { id: 'MID-01', seg: 'Mid-Market', isNew: false, isChurn: false, begMrr: 8000, endMrr: 9500, tix: 0, drop: 0, cohort: 0, activeM: 6 },
            { id: 'MID-02', seg: 'Mid-Market', isNew: false, isChurn: true,  begMrr: 7500, endMrr: 0,    tix: 3, drop: 50, cohort: 2, activeM: 2 },
            { id: 'MID-03', seg: 'Mid-Market', isNew: false, isChurn: false, begMrr: 9000, endMrr: 9000, tix: 1, drop: 5, cohort: 1, activeM: 6 },
            { id: 'MID-04', seg: 'Mid-Market', isNew: true,  isChurn: false, begMrr: 0,    endMrr: 8500, tix: 0, drop: 0, cohort: 4, activeM: 2 },
            // SMB (High Logo count, tiny MRR. High Logo Churn, Low Rev Churn)
        ];
        // Generate 50 SMBs dynamically to populate the SSOT
        for(let i=1; i<=50; i++) {
            let isCh = i <= 10; // 20% logo churn
            let beg = 500;
            let end = isCh ? 0 : 500;
            rawCustomerData.push({
                id: `SMB-${i}`, seg: 'SMB', isNew: false, isChurn: isCh, begMrr: beg, endMrr: end, tix: isCh ? 2 : 0, drop: isCh ? 100 : 0, cohort: i%3, activeM: isCh ? 2 : 6
            });
        }

        let cWater, cTrap, cPareto;

        function init() {
            cWater = echarts.init(document.getElementById('chartWaterfall'));
            cTrap = echarts.init(document.getElementById('chartTrap'));
            cPareto = echarts.init(document.getElementById('chartPareto'));
            window.addEventListener('resize', () => { cWater.resize(); cTrap.resize(); cPareto.resize(); });
            applyFilters();
        }

        function applyFilters() {
            const segFilter = document.getElementById('filterSegment').value;
            const data = rawCustomerData.filter(d => segFilter === 'All' || d.seg === segFilter);
            
            if (data.length === 0) {
                document.getElementById('emptyState').style.display = 'flex';
                return;
            } else {
                document.getElementById('emptyState').style.display = 'none';
            }

            // --- INVARIANT ENGINE (CALCULATIONS) ---
            let metrics = {
                begLogos: 0, churnLogos: 0, newLogos: 0,
                begMrr: 0, newMrr: 0, expMrr: 0, contMrr: 0, churnMrr: 0, endMrr: 0
            };

            data.forEach(d => {
                if (!d.isNew) {
                    metrics.begLogos++;
                    metrics.begMrr += d.begMrr;
                    if (d.isChurn) {
                        metrics.churnLogos++;
                        metrics.churnMrr += d.begMrr; // Lost MRR is their begMrr
                    } else {
                        if (d.endMrr > d.begMrr) metrics.expMrr += (d.endMrr - d.begMrr);
                        if (d.endMrr < d.begMrr) metrics.contMrr += (d.begMrr - d.endMrr);
                    }
                } else {
                    metrics.newLogos++;
                    metrics.newMrr += d.endMrr;
                }
                metrics.endMrr += d.endMrr;
            });

            // Mathematical Invariant Check
            const calcEndMrr = metrics.begMrr + metrics.newMrr + metrics.expMrr - metrics.contMrr - metrics.churnMrr;
            if (Math.abs(calcEndMrr - metrics.endMrr) > 1) console.error(`INVARIANT FAILURE: ${calcEndMrr} != ${metrics.endMrr}`);

            // KPI Calculations
            const nrr = metrics.begMrr > 0 ? ((metrics.begMrr + metrics.expMrr - metrics.contMrr - metrics.churnMrr) / metrics.begMrr) * 100 : 0;
            const grr = metrics.begMrr > 0 ? ((metrics.begMrr - metrics.contMrr - metrics.churnMrr) / metrics.begMrr) * 100 : 0;
            const logoChurn = metrics.begLogos > 0 ? (metrics.churnLogos / metrics.begLogos) * 100 : 0;
            const revChurn = metrics.begMrr > 0 ? (metrics.churnMrr / metrics.begMrr) * 100 : 0;

            // Update UI KPIs
            document.getElementById('kpiNRR').innerText = nrr.toFixed(1) + '%';
            document.getElementById('kpiNRR').className = `kpi-value ${nrr >= 100 ? 'pos' : 'neg'}`;
            document.getElementById('kpiGRR').innerText = grr.toFixed(1) + '%';
            document.getElementById('kpiGRR').className = `kpi-value ${grr >= 90 ? 'pos' : 'neg'}`;
            document.getElementById('kpiLogoChurn').innerText = logoChurn.toFixed(1) + '%';
            document.getElementById('kpiRevChurn').innerText = revChurn.toFixed(1) + '%';

            // --- CHART 1: WATERFALL (Reconciled) ---
            const b = metrics.begMrr, n = metrics.newMrr, e = metrics.expMrr, c = metrics.contMrr, ch = metrics.churnMrr, end = metrics.endMrr;
            cWater.setOption({
                tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
                grid: { left: '3%', right: '3%', bottom: '5%', top: '10%', containLabel: true },
                xAxis: { type: 'category', data: ['Beg. MRR', 'New', 'Expansion', 'Contraction', 'Churn', 'End MRR'], axisLabel: {color: '#9CA3AF'} },
                yAxis: { type: 'value', axisLabel: {color: '#9CA3AF', formatter: '${c}', fontFamily: 'JetBrains Mono'}, splitLine: {lineStyle: {color: '#1F2937'}} },
                series: [
                    { type: 'bar', stack: 'Total', itemStyle: { color: 'transparent' }, data: [0, b, b+n, b+n+e-c, b+n+e-c-ch, 0] },
                    { type: 'bar', stack: 'Total', itemStyle: { color: '#10B981', borderRadius: 2 }, data: [b, n, e, 0, 0, end] },
                    { type: 'bar', stack: 'Total', itemStyle: { color: '#F43F5E', borderRadius: 2 }, data: [0, 0, 0, c, ch, 0] }
                ]
            });

            // --- CHART 2: CHURN TRAP (Dynamic Segmentation) ---
            const segStats = {};
            data.forEach(d => {
                if(d.isNew) return;
                if(!segStats[d.seg]) segStats[d.seg] = { bLogos:0, cLogos:0, bMrr:0, cMrr:0 };
                segStats[d.seg].bLogos++;
                segStats[d.seg].bMrr += d.begMrr;
                if(d.isChurn) { segStats[d.seg].cLogos++; segStats[d.seg].cMrr += d.begMrr; }
            });
            const trapNames = Object.keys(segStats);
            const trapLogo = trapNames.map(s => (segStats[s].cLogos / segStats[s].bLogos)*100);
            const trapRev = trapNames.map(s => (segStats[s].cMrr / segStats[s].bMrr)*100);

            cTrap.setOption({
                tooltip: { trigger: 'axis' },
                legend: { data: ['Logo Churn %', 'Rev Churn %'], textStyle: {color: '#9CA3AF'}, top: 0 },
                grid: { left: '3%', right: '3%', bottom: '5%', top: '15%', containLabel: true },
                xAxis: { type: 'category', data: trapNames, axisLabel: {color: '#9CA3AF'} },
                yAxis: { type: 'value', axisLabel: {formatter: '{value}%', color: '#9CA3AF'}, splitLine: {lineStyle: {color: '#1F2937'}} },
                series: [
                    { name: 'Logo Churn %', type: 'bar', itemStyle: { color: '#F59E0B' }, data: trapLogo },
                    { name: 'Rev Churn %', type: 'bar', itemStyle: { color: '#F43F5E' }, data: trapRev }
                ]
            });

            // --- CHART 3: PARETO CONCENTRATION (Dynamic) ---
            const activeCusts = data.filter(d => !d.isChurn).sort((a,b) => b.endMrr - a.endMrr);
            const totalActiveMrr = activeCusts.reduce((sum, d) => sum + d.endMrr, 0);
            
            // Calculate Top 5% and 10% thresholds
            const top5Idx = Math.max(1, Math.ceil(activeCusts.length * 0.05));
            const top10Idx = Math.max(1, Math.ceil(activeCusts.length * 0.10));
            
            let top5Mrr = 0, top10Mrr = 0;
            activeCusts.forEach((c, idx) => {
                if(idx < top5Idx) top5Mrr += c.endMrr;
                if(idx < top10Idx) top10Mrr += c.endMrr;
            });

            let cum = 0;
            const paretoCurve = activeCusts.map((c, i) => {
                cum += c.endMrr;
                return { percent: ((i+1)/activeCusts.length)*100, cumMrr: cum, cumPct: (cum/totalActiveMrr)*100 };
            });
            // Sample for chart (Deciles approx)
            const pX = [], pYBar = [], pYLine = [];
            [0.05, 0.1, 0.2, 0.5, 1.0].forEach(thresh => {
                const target = paretoCurve.find(p => p.percent >= thresh*100) || paretoCurve[paretoCurve.length-1];
                if(target) {
                    pX.push(`Top ${thresh*100}%`);
                    pYLine.push(target.cumPct);
                    pYBar.push(target.cumMrr);
                }
            });

            cPareto.setOption({
                tooltip: { trigger: 'axis' },
                grid: { left: '3%', right: '5%', bottom: '5%', top: '10%', containLabel: true },
                xAxis: { type: 'category', data: pX, axisLabel: {color: '#9CA3AF'} },
                yAxis: [
                    { type: 'value', axisLabel: {color: '#9CA3AF'}, splitLine: {lineStyle: {color: '#1F2937'}} },
                    { type: 'value', axisLabel: {formatter: '{value}%', color: '#9CA3AF'}, max: 100, splitLine: {show:false} }
                ],
                series: [
                    { type: 'bar', data: pYBar, itemStyle: {color: '#6366F1'} },
                    { type: 'line', yAxisIndex: 1, data: pYLine, itemStyle: {color: '#10B981'} }
                ]
            });

            // --- EXCEPTION ENGINE (NARRATIVE) ---
            const t5Pct = totalActiveMrr > 0 ? (top5Mrr/totalActiveMrr)*100 : 0;
            let insights = "";
            insights += `<div class="ai-bullet"><strong>Observed Retention:</strong> Base MRR was $${metrics.begMrr.toLocaleString()}. Churn reduced it by $${metrics.churnMrr.toLocaleString()}, while expansion added $${metrics.expMrr.toLocaleString()}. NRR is precisely ${nrr.toFixed(1)}%.</div>`;
            
            if(t5Pct > 40) {
                insights += `<div class="ai-bullet"><strong>Concentration Fact:</strong> Top 5% of active customers generate ${t5Pct.toFixed(1)}% of total MRR. <br/><strong>Scenario:</strong> Loss of the single largest account would immediately reduce MRR by $${activeCusts[0]?.endMrr.toLocaleString()}, tanking NRR by ${((activeCusts[0]?.endMrr / metrics.begMrr)*100).toFixed(1)} percentage points.</div>`;
            }
            if(logoChurn > revChurn * 2) {
                insights += `<div class="ai-bullet"><strong>The Churn Paradox:</strong> Logo churn (${logoChurn.toFixed(1)}%) is heavily disproportionate to Revenue churn (${revChurn.toFixed(1)}%). We are losing high volumes of low-value accounts.</div>`;
            }
            document.getElementById('aiInsights').innerHTML = insights;

            // --- RISK TABLE (Explicit Rule Definition) ---
            const riskBody = document.getElementById('riskTableBody');
            riskBody.innerHTML = '';
            const atRisk = activeCusts.filter(c => c.drop > 40 || c.tix >= 5);
            atRisk.forEach(c => {
                const tr = document.createElement('tr');
                let severity = (c.drop > 40 && c.tix >= 5) ? '<span class="badge critical">CRITICAL</span>' : '<span class="badge warning">HIGH</span>';
                tr.innerHTML = `<td>${c.id}</td><td>${c.seg}</td><td>$${c.begMrr.toLocaleString()}</td><td class="neg">-${c.drop}%</td><td>${c.tix}</td><td>${severity}</td>`;
                riskBody.appendChild(tr);
            });
            if(atRisk.length === 0) {
                riskBody.innerHTML = `<tr><td colspan="6" style="text-align:center; color:#10B981;">No customers match the risk criteria.</td></tr>`;
            }
        }
        setTimeout(init, 200);
    </script>
</body>
</html>"""

final_html = html_template.replace("ECHARTS_INLINE_PAYLOAD", echarts_js)
file_path = r"C:\Users\ROG G532 LV\.gemini\antigravity\scratch\Senior-Data-Analyst\Final_Retention_Dashboard_V2_Corrected.html"

with open(file_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print("Forensic Corrected Dashboard Generated.")
