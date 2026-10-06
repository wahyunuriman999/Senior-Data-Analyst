import urllib.request
import os

print("Preparing ECharts inline payload...")
req = urllib.request.Request('https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js', headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        echarts_js = response.read().decode('utf-8')
except Exception as e:
    print("Download failed, using existing fallback:", e)
    # Read from existing if available
    with open(r'Final_Executive_Dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()
        import re
        m = re.search(r'<script>\s*(\/\*! ECharts[\s\S]*?)\s*<\/script>', content)
        echarts_js = m.group(1) if m else "console.error('ECharts missing');"

html_template = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise Multi-City Sales Performance - Anti-Slop Cross-Filtering Engine</title>
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
            --primary: #3B82F6;
            --positive: #10B981;
            --negative: #EF4444;
            --warning: #F59E0B;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: var(--bg-base); color: var(--text-main); font-family: 'Inter', sans-serif; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }

        /* HEADER & SLICER BAR */
        .header { height: 64px; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; padding: 0 28px; background: rgba(17, 24, 39, 0.98); z-index: 50; }
        .title-block h1 { font-size: 15px; font-weight: 700; letter-spacing: 0.3px; }
        .title-block span { font-size: 11px; color: var(--text-muted); font-family: 'JetBrains Mono'; }

        .slicer-header-bar { height: 48px; border-bottom: 1px solid var(--border); display: flex; align-items: center; padding: 0 28px; gap: 14px; background: rgba(15, 23, 42, 0.7); }
        .slicer-label { font-size: 11px; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
        .slicer-select { background: var(--bg-panel); color: var(--text-main); border: 1px solid var(--border); padding: 5px 10px; border-radius: 4px; font-size: 12px; outline: none; cursor: pointer; }
        .slicer-select:focus { border-color: var(--primary); }

        .active-chips { display: flex; align-items: center; gap: 8px; margin-left: 8px; }
        .chip { background: rgba(59, 130, 246, 0.15); border: 1px solid rgba(59, 130, 246, 0.4); color: #93C5FD; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; display: inline-flex; align-items: center; gap: 6px; }
        .chip-remove { cursor: pointer; color: #BFDBFE; font-weight: bold; }
        .chip-remove:hover { color: #fff; }

        .btn-clear { background: transparent; border: 1px solid var(--border); color: var(--text-muted); padding: 4px 10px; border-radius: 4px; font-size: 11px; font-weight: 600; cursor: pointer; margin-left: auto; transition: 0.15s; }
        .btn-clear:hover { background: rgba(239, 68, 68, 0.15); color: var(--negative); border-color: var(--negative); }

        /* GRID CONTENT */
        .scroll-area { flex: 1; overflow-y: auto; padding: 20px 28px; }
        .dashboard-grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 16px; }

        .panel { background: var(--bg-panel); border: 1px solid var(--border); border-radius: 8px; padding: 18px; display: flex; flex-direction: column; }
        .span-3 { grid-column: span 3; }
        .span-4 { grid-column: span 4; }
        .span-6 { grid-column: span 6; }
        .span-8 { grid-column: span 8; }
        .span-12 { grid-column: span 12; }

        /* KPIS */
        .kpi-title { font-size: 11px; color: var(--text-muted); font-weight: 600; text-transform: uppercase; margin-bottom: 4px; }
        .kpi-value { font-size: 24px; font-weight: 700; font-family: 'JetBrains Mono'; margin-bottom: 4px; }
        .kpi-sub { font-size: 11px; color: var(--text-muted); display: flex; align-items: center; gap: 4px; }
        .pos { color: var(--positive); }
        .neg { color: var(--negative); }

        /* CHARTS */
        .chart-header { font-size: 13px; font-weight: 600; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
        .chart-hint { font-size: 11px; font-weight: 400; color: #60A5FA; font-family: 'JetBrains Mono'; }
        .chart-container { height: 280px; width: 100%; }

        /* DATA TABLE */
        .data-table { width: 100%; border-collapse: collapse; font-size: 12px; }
        .data-table th { padding: 10px 12px; border-bottom: 1px solid var(--border); color: var(--text-muted); font-weight: 600; text-align: left; text-transform: uppercase; font-size: 11px; }
        .data-table td { padding: 10px 12px; border-bottom: 1px solid rgba(31, 41, 55, 0.6); font-family: 'JetBrains Mono'; }
        .data-table tr { cursor: pointer; transition: 0.1s; }
        .data-table tr:hover { background: rgba(59, 130, 246, 0.08); }
        .data-table tr.active-row { background: rgba(59, 130, 246, 0.18); font-weight: 700; }
        .badge { padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: 700; }
        .badge.target-met { background: rgba(16, 185, 129, 0.2); color: var(--positive); }
        .badge.target-miss { background: rgba(239, 68, 68, 0.2); color: var(--negative); }
    </style>
</head>
<body>
    <header class="header">
        <div class="title-block">
            <h1>MONITORING PERFORMA PENJUALAN RETAIL NASIONAL</h1>
            <span>DATA PROVINSI & KOTA | CROSS-FILTERING ENGINE AKTIF</span>
        </div>
        <div style="font-size:11px; font-family:'JetBrains Mono'; color:var(--text-muted);">
            STANDAR: <b style="color:var(--positive);">ANTI-SLOP V1.2</b>
        </div>
    </header>

    <!-- MANDATORY HEADER SLICER BAR -->
    <div class="slicer-header-bar">
        <span class="slicer-label">Filter Kota:</span>
        <select class="slicer-select" id="slicerCity" onchange="onSlicerCityChange(this.value)">
            <option value="All">Semua Kota (Nasional)</option>
            <option value="Bandung">Bandung</option>
            <option value="Jakarta">Jakarta</option>
            <option value="Surabaya">Surabaya</option>
            <option value="Medan">Medan</option>
            <option value="Semarang">Semarang</option>
        </select>

        <span class="slicer-label" style="margin-left:10px;">Kategori:</span>
        <select class="slicer-select" id="slicerCat" onchange="onSlicerCatChange(this.value)">
            <option value="All">Semua Kategori</option>
            <option value="Elektronik">Elektronik</option>
            <option value="Fashion">Fashion</option>
            <option value="F&B">F&B</option>
            <option value="Kebutuhan Pokok">Kebutuhan Pokok</option>
        </select>

        <div class="active-chips" id="chipsContainer"></div>

        <button class="btn-clear" onclick="resetFilters()">✕ Reset Filter</button>
    </div>

    <main class="scroll-area">
        <div class="dashboard-grid">
            <!-- 4 SUMMARY KPIS -->
            <div class="panel span-3">
                <div class="kpi-title">Total Pendapatan</div>
                <div class="kpi-value" id="kpiRevenue">--</div>
                <div class="kpi-sub pos" id="kpiRevYoY">▲ YTD Aktual</div>
            </div>
            <div class="panel span-3">
                <div class="kpi-title">Laba Bersih</div>
                <div class="kpi-value" id="kpiProfit">--</div>
                <div class="kpi-sub" id="kpiProfitMargin">Margin: --</div>
            </div>
            <div class="panel span-3">
                <div class="kpi-title">Margin Bersih (%)</div>
                <div class="kpi-value" id="kpiMargin">--</div>
                <div class="kpi-sub" id="kpiMarginStatus">Evaluasi Target</div>
            </div>
            <div class="panel span-3">
                <div class="kpi-title">Volume Transaksi</div>
                <div class="kpi-value" id="kpiOrders">--</div>
                <div class="kpi-sub" id="kpiAOV">AOV: --</div>
            </div>

            <!-- REGIONAL BREAKDOWN (CLICK-TO-FILTER SOURCE) -->
            <div class="panel span-6">
                <div class="chart-header">
                    <span>Pendapatan Berdasarkan Kota</span>
                    <span class="chart-hint">💡 KLIK BATANG UNTUK FILTER OTOMATIS</span>
                </div>
                <div id="chartCity" class="chart-container"></div>
            </div>

            <!-- TREND BULANAN -->
            <div class="panel span-6">
                <div class="chart-header">
                    <span id="trendHeader">Tren Pendapatan Bulanan (2026)</span>
                    <span style="font-size:11px; color:var(--text-muted); font-family:'JetBrains Mono';">GRAIN: BULANAN</span>
                </div>
                <div id="chartTrend" class="chart-container"></div>
            </div>

            <!-- BREAKDOWN KATEGORI -->
            <div class="panel span-5">
                <div class="chart-header">
                    <span>Distribusi Pendapatan per Kategori</span>
                    <span class="chart-hint">💡 KLIK KATEGORI UNTUK FILTER</span>
                </div>
                <div id="chartCategory" class="chart-container"></div>
            </div>

            <!-- DETAIL TABEL KOTA DENGAN CLICK-TO-FILTER -->
            <div class="panel span-7">
                <div class="chart-header">
                    <span>Tabel Kinerja Regional & Margin</span>
                    <span class="chart-hint">💡 KLIK BARIS KOTA UNTUK FILTER</span>
                </div>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Kota</th>
                            <th>Pendapatan</th>
                            <th>Laba Bersih</th>
                            <th>Margin</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody"></tbody>
                </table>
            </div>
        </div>
    </main>

    <script>
        // SINGLE SOURCE OF TRUTH (SSOT) - DATASET TRANSAKSI AGREGAT
        const rawSales = [
            // Bandung
            { city: 'Bandung', cat: 'Elektronik', month: 'Jan', rev: 1200000000, prof: 180000000, orders: 450 },
            { city: 'Bandung', cat: 'Elektronik', month: 'Feb', rev: 1350000000, prof: 210000000, orders: 510 },
            { city: 'Bandung', cat: 'Fashion', month: 'Jan', rev: 850000000, prof: 280000000, orders: 1200 },
            { city: 'Bandung', cat: 'Fashion', month: 'Feb', rev: 920000000, prof: 310000000, orders: 1310 },
            { city: 'Bandung', cat: 'F&B', month: 'Jan', rev: 400000000, prof: 90000000, orders: 2100 },
            { city: 'Bandung', cat: 'F&B', month: 'Feb', rev: 450000000, prof: 110000000, orders: 2350 },
            { city: 'Bandung', cat: 'Kebutuhan Pokok', month: 'Jan', rev: 600000000, prof: 45000000, orders: 1800 },
            { city: 'Bandung', cat: 'Kebutuhan Pokok', month: 'Feb', rev: 680000000, prof: 52000000, orders: 2010 },

            // Jakarta
            { city: 'Jakarta', cat: 'Elektronik', month: 'Jan', rev: 2800000000, prof: 420000000, orders: 980 },
            { city: 'Jakarta', cat: 'Elektronik', month: 'Feb', rev: 3100000000, prof: 490000000, orders: 1120 },
            { city: 'Jakarta', cat: 'Fashion', month: 'Jan', rev: 1600000000, prof: 540000000, orders: 2300 },
            { city: 'Jakarta', cat: 'Fashion', month: 'Feb', rev: 1750000000, prof: 610000000, orders: 2450 },
            { city: 'Jakarta', cat: 'F&B', month: 'Jan', rev: 900000000, prof: 210000000, orders: 4500 },
            { city: 'Jakarta', cat: 'F&B', month: 'Feb', rev: 980000000, prof: 240000000, orders: 4800 },
            { city: 'Jakarta', cat: 'Kebutuhan Pokok', month: 'Jan', rev: 1100000000, prof: 85000000, orders: 3200 },
            { city: 'Jakarta', cat: 'Kebutuhan Pokok', month: 'Feb', rev: 1250000000, prof: 98000000, orders: 3500 },

            // Surabaya
            { city: 'Surabaya', cat: 'Elektronik', month: 'Jan', rev: 1600000000, prof: 240000000, orders: 620 },
            { city: 'Surabaya', cat: 'Elektronik', month: 'Feb', rev: 1750000000, prof: 270000000, orders: 680 },
            { city: 'Surabaya', cat: 'Fashion', month: 'Jan', rev: 950000000, prof: 320000000, orders: 1400 },
            { city: 'Surabaya', cat: 'Fashion', month: 'Feb', rev: 1020000000, prof: 350000000, orders: 1520 },
            { city: 'Surabaya', cat: 'F&B', month: 'Jan', rev: 550000000, prof: 130000000, orders: 2800 },
            { city: 'Surabaya', cat: 'F&B', month: 'Feb', rev: 610000000, prof: 150000000, orders: 3100 },
            { city: 'Surabaya', cat: 'Kebutuhan Pokok', month: 'Jan', rev: 720000000, prof: 56000000, orders: 2200 },
            { city: 'Surabaya', cat: 'Kebutuhan Pokok', month: 'Feb', rev: 780000000, prof: 62000000, orders: 2400 },

            // Medan
            { city: 'Medan', cat: 'Elektronik', month: 'Jan', rev: 900000000, prof: 130000000, orders: 350 },
            { city: 'Medan', cat: 'Elektronik', month: 'Feb', rev: 980000000, prof: 145000000, orders: 390 },
            { city: 'Medan', cat: 'Fashion', month: 'Jan', rev: 620000000, prof: 200000000, orders: 900 },
            { city: 'Medan', cat: 'Fashion', month: 'Feb', rev: 670000000, prof: 220000000, orders: 980 },
            { city: 'Medan', cat: 'F&B', month: 'Jan', rev: 320000000, prof: 75000000, orders: 1600 },
            { city: 'Medan', cat: 'F&B', month: 'Feb', rev: 350000000, prof: 82000000, orders: 1750 },
            { city: 'Medan', cat: 'Kebutuhan Pokok', month: 'Jan', rev: 450000000, prof: 35000000, orders: 1350 },
            { city: 'Medan', cat: 'Kebutuhan Pokok', month: 'Feb', rev: 490000000, prof: 39000000, orders: 1480 },

            // Semarang
            { city: 'Semarang', cat: 'Elektronik', month: 'Jan', rev: 750000000, prof: 110000000, orders: 290 },
            { city: 'Semarang', cat: 'Elektronik', month: 'Feb', rev: 810000000, prof: 122000000, orders: 320 },
            { city: 'Semarang', cat: 'Fashion', month: 'Jan', rev: 520000000, prof: 170000000, orders: 750 },
            { city: 'Semarang', cat: 'Fashion', month: 'Feb', rev: 560000000, prof: 185000000, orders: 810 },
            { city: 'Semarang', cat: 'F&B', month: 'Jan', rev: 270000000, prof: 62000000, orders: 1350 },
            { city: 'Semarang', cat: 'F&B', month: 'Feb', rev: 295000000, prof: 69000000, orders: 1480 },
            { city: 'Semarang', cat: 'Kebutuhan Pokok', month: 'Jan', rev: 380000000, prof: 29000000, orders: 1150 },
            { city: 'Semarang', cat: 'Kebutuhan Pokok', month: 'Feb', rev: 410000000, prof: 32000000, orders: 1240 }
        ];

        // GLOBAL FILTER STATE
        const state = {
            city: 'All',
            cat: 'All'
        };

        let chartCity, chartTrend, chartCat;

        // FORMATTER RUPIAH
        function fmtRp(val) {
            if (val >= 1000000000) return 'Rp ' + (val / 1000000000).toFixed(2) + ' M';
            if (val >= 1000000) return 'Rp ' + (val / 1000000).toFixed(1) + ' Jt';
            return 'Rp ' + val.toLocaleString('id-ID');
        }

        function init() {
            chartCity = echarts.init(document.getElementById('chartCity'));
            chartTrend = echarts.init(document.getElementById('chartTrend'));
            chartCat = echarts.init(document.getElementById('chartCategory'));

            // 1. EVENT CLICK-TO-FILTER PADA CHART KOTA (MISAL KLIK BANDUNG)
            chartCity.on('click', function(params) {
                const clickedCity = params.name;
                toggleCityFilter(clickedCity);
            });

            // 2. EVENT CLICK-TO-FILTER PADA CHART KATEGORI
            chartCat.on('click', function(params) {
                const clickedCat = params.name;
                toggleCatFilter(clickedCat);
            });

            window.addEventListener('resize', () => {
                chartCity.resize();
                chartTrend.resize();
                chartCat.resize();
            });

            recalculateAndRender();
        }

        // TOGGLE & AUTO FILTER KOTA
        function toggleCityFilter(cityName) {
            if (state.city === cityName) {
                state.city = 'All'; // Klik ulang untuk unfilter
            } else {
                state.city = cityName; // Auto filter ke kota terpilih (e.g. Bandung)
            }
            syncSlicersUI();
            recalculateAndRender();
        }

        function toggleCatFilter(catName) {
            if (state.cat === catName) {
                state.cat = 'All';
            } else {
                state.cat = catName;
            }
            syncSlicersUI();
            recalculateAndRender();
        }

        function onSlicerCityChange(val) {
            state.city = val;
            syncSlicersUI();
            recalculateAndRender();
        }

        function onSlicerCatChange(val) {
            state.cat = val;
            syncSlicersUI();
            recalculateAndRender();
        }

        function resetFilters() {
            state.city = 'All';
            state.cat = 'All';
            syncSlicersUI();
            recalculateAndRender();
        }

        function syncSlicersUI() {
            document.getElementById('slicerCity').value = state.city;
            document.getElementById('slicerCat').value = state.cat;

            // Render active filter chips
            const chipsBox = document.getElementById('chipsContainer');
            chipsBox.innerHTML = '';

            if (state.city !== 'All') {
                const chip = document.createElement('div');
                chip.className = 'chip';
                chip.innerHTML = `📍 Kota: <b>${state.city}</b> <span class="chip-remove" onclick="toggleCityFilter('${state.city}')">✕</span>`;
                chipsBox.appendChild(chip);
            }

            if (state.cat !== 'All') {
                const chip = document.createElement('div');
                chip.className = 'chip';
                chip.innerHTML = `🏷️ Kategori: <b>${state.cat}</b> <span class="chip-remove" onclick="toggleCatFilter('${state.cat}')">✕</span>`;
                chipsBox.appendChild(chip);
            }
        }

        // CORE SSOT RECALCULATION & RENDERING
        function recalculateAndRender() {
            // 1. Filter raw data
            const filtered = rawSales.filter(d => 
                (state.city === 'All' || d.city === state.city) &&
                (state.cat === 'All' || d.cat === state.cat)
            );

            // 2. Hitung KPI Agregat
            const totalRev = filtered.reduce((acc, d) => acc + d.rev, 0);
            const totalProf = filtered.reduce((acc, d) => acc + d.prof, 0);
            const totalOrders = filtered.reduce((acc, d) => acc + d.orders, 0);
            const margin = totalRev > 0 ? (totalProf / totalRev) * 100 : 0;
            const aov = totalOrders > 0 ? totalRev / totalOrders : 0;

            document.getElementById('kpiRevenue').innerText = fmtRp(totalRev);
            document.getElementById('kpiProfit').innerText = fmtRp(totalProf);
            document.getElementById('kpiProfitMargin').innerText = `Laba dari Total Omzet`;
            
            const marginEl = document.getElementById('kpiMargin');
            marginEl.innerText = margin.toFixed(1) + '%';
            marginEl.className = `kpi-value ${margin >= 20 ? 'pos' : (margin >= 12 ? 'pos' : 'neg')}`;
            document.getElementById('kpiMarginStatus').innerText = margin >= 15 ? '✓ Target Tercapai' : '⚠️ Perhatian Margin Rendah';

            document.getElementById('kpiOrders').innerText = totalOrders.toLocaleString('id-ID');
            document.getElementById('kpiAOV').innerText = `AOV: ${fmtRp(aov)}`;

            document.getElementById('trendHeader').innerText = state.city === 'All' 
                ? 'Tren Pendapatan Bulanan (Nasional)' 
                : `Tren Pendapatan Bulanan (Khusus: ${state.city})`;

            // 3. Render Chart Kota (Highlight Kota Terpilih, Dim yang lain)
            const cityAgg = {};
            const citiesList = ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Semarang'];
            citiesList.forEach(c => cityAgg[c] = 0);

            // Hitung total per kota (memperhatikan filter kategori jika ada)
            rawSales.filter(d => state.cat === 'All' || d.cat === state.cat)
                    .forEach(d => cityAgg[d.city] = (cityAgg[d.city] || 0) + d.rev);

            const cityData = citiesList.map(c => {
                const isSelected = (state.city === c);
                const isAll = (state.city === 'All');
                return {
                    name: c,
                    value: cityAgg[c],
                    itemStyle: {
                        color: isSelected ? '#3B82F6' : (isAll ? '#60A5FA' : 'rgba(96, 165, 250, 0.25)'),
                        borderRadius: [0, 4, 4, 0]
                    }
                };
            });

            chartCity.setOption({
                tooltip: { 
                    trigger: 'item',
                    formatter: (p) => `<b>${p.name}</b><br/>Omzet: ${fmtRp(p.value)}<br/><i>(Klik untuk filter ke ${p.name})</i>`
                },
                grid: { left: '3%', right: '8%', bottom: '5%', top: '5%', containLabel: true },
                xAxis: { type: 'value', axisLabel: { color: '#9CA3AF', formatter: v => (v/1000000000).toFixed(1) + 'M' }, splitLine: { lineStyle: { color: '#1F2937' } } },
                yAxis: { type: 'category', data: citiesList, axisLabel: { color: '#F3F4F6', fontWeight: 600 }, axisLine: { show: false } },
                series: [{
                    type: 'bar',
                    data: cityData,
                    barWidth: 24,
                    label: { show: true, position: 'right', color: '#9CA3AF', formatter: (p) => (p.value/1000000000).toFixed(2) + ' M' }
                }]
            });

            // 4. Render Tren Bulanan (Jan vs Feb)
            const months = ['Jan', 'Feb'];
            const trendData = months.map(m => {
                return filtered.filter(d => d.month === m).reduce((acc, d) => acc + d.rev, 0);
            });
            const trendProf = months.map(m => {
                return filtered.filter(d => d.month === m).reduce((acc, d) => acc + d.prof, 0);
            });

            chartTrend.setOption({
                tooltip: { trigger: 'axis', formatter: (p) => `<b>Bulan ${p[0].name}</b><br/>Omzet: ${fmtRp(p[0].value)}<br/>Laba: ${fmtRp(p[1].value)}` },
                legend: { data: ['Pendapatan', 'Laba Bersih'], textStyle: { color: '#9CA3AF' }, top: 0 },
                grid: { left: '3%', right: '4%', bottom: '5%', top: '15%', containLabel: true },
                xAxis: { type: 'category', data: ['Januari', 'Februari'], axisLabel: { color: '#9CA3AF' } },
                yAxis: { type: 'value', axisLabel: { color: '#9CA3AF', formatter: v => (v/1000000000).toFixed(1) + 'M' }, splitLine: { lineStyle: { color: '#1F2937' } } },
                series: [
                    { name: 'Pendapatan', type: 'line', smooth: true, itemStyle: { color: '#3B82F6' }, areaStyle: { color: 'rgba(59, 130, 246, 0.2)' }, data: trendData },
                    { name: 'Laba Bersih', type: 'line', smooth: true, itemStyle: { color: '#10B981' }, areaStyle: { color: 'rgba(16, 185, 129, 0.2)' }, data: trendProf }
                ]
            });

            // 5. Render Breakdown Kategori
            const catMap = {};
            ['Elektronik', 'Fashion', 'F&B', 'Kebutuhan Pokok'].forEach(cat => catMap[cat] = 0);
            filtered.forEach(d => catMap[d.cat] += d.rev);

            const catSeries = Object.keys(catMap).map(k => {
                const isSelected = (state.cat === k);
                const isAll = (state.cat === 'All');
                return {
                    name: k,
                    value: catMap[k],
                    itemStyle: {
                        color: isSelected ? '#10B981' : (isAll ? '#3B82F6' : 'rgba(59, 130, 246, 0.25)')
                    }
                };
            });

            chartCat.setOption({
                tooltip: { trigger: 'item', formatter: p => `<b>${p.name}</b>: ${fmtRp(p.value)} (${((p.value/totalRev)*100).toFixed(1)}%)` },
                grid: { left: '3%', right: '5%', bottom: '5%', top: '5%', containLabel: true },
                xAxis: { type: 'category', data: Object.keys(catMap), axisLabel: { color: '#9CA3AF', interval: 0, fontSize: 10 } },
                yAxis: { type: 'value', axisLabel: { color: '#9CA3AF', formatter: v => (v/1000000000).toFixed(1) + 'M' }, splitLine: { lineStyle: { color: '#1F2937' } } },
                series: [{
                    type: 'bar',
                    data: catSeries,
                    barWidth: 32,
                    label: { show: true, position: 'top', color: '#9CA3AF', formatter: p => (p.value/1000000000).toFixed(1) + 'M' }
                }]
            });

            // 6. Update Tabel Kota
            const tableBody = document.getElementById('tableBody');
            tableBody.innerHTML = '';
            citiesList.forEach(city => {
                const cRows = rawSales.filter(d => d.city === city && (state.cat === 'All' || d.cat === state.cat));
                const cRev = cRows.reduce((a, b) => a + b.rev, 0);
                const cProf = cRows.reduce((a, b) => a + b.prof, 0);
                const cMargin = cRev > 0 ? (cProf / cRev) * 100 : 0;
                const isRowActive = (state.city === city);

                const tr = document.createElement('tr');
                if (isRowActive) tr.className = 'active-row';
                tr.onclick = () => toggleCityFilter(city);

                tr.innerHTML = `
                    <td style="color:${isRowActive ? '#60A5FA' : '#F9FAFB'}; font-weight:600;">
                        ${isRowActive ? '📍 ' : ''}${city}
                    </td>
                    <td>${fmtRp(cRev)}</td>
                    <td>${fmtRp(cProf)}</td>
                    <td class="${cMargin >= 18 ? 'pos' : 'neg'}">${cMargin.toFixed(1)}%</td>
                    <td>
                        <span class="badge ${cMargin >= 18 ? 'target-met' : 'target-miss'}">
                            ${cMargin >= 18 ? 'OPTIMAL' : 'PERHATIAN'}
                        </span>
                    </td>
                `;
                tableBody.appendChild(tr);
            });
        }

        setTimeout(init, 300);
    </script>
</body>
</html>"""

final_html = html_template.replace("ECHARTS_INLINE_PAYLOAD", echarts_js)

# Save at root for instant double-click
root_path = r"Final_CrossFilter_Dashboard.html"
with open(root_path, "w", encoding="utf-8") as f:
    f.write(final_html)

# Save in proof/examples/ as permanent architectural evidence
proof_path = os.path.join(r"data-analyst-visualization-skill\proof\examples", "Final_CrossFilter_Dashboard.html")
with open(proof_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print("Final CrossFilter Dashboard generated successfully at root and proof/examples/.")
