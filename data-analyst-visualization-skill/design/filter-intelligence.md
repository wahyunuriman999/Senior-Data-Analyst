# ELITE DASHBOARD FILTER & SLICER SYSTEM

## 1. FILTER INTELLIGENCE (CARDINALITY MAPPING)
- **Low Cardinality (2-4)**: Use Segmented Controls or Radio Buttons (e.g., Gender, Segment). NEVER use dropdowns.
- **Medium Cardinality (5-20)**: Use Multi-select Checkbox Dropdowns.
- **High Cardinality (20+)**: Use Searchable Typeahead / Autocomplete.
- **Numeric**: Use Range Sliders or Min/Max inputs.
- **Dates**: Use Smart Presets (Last 30 Days, YTD) + Custom Range.

## 2. FILTER STATE & HEADER SLICER BAR (MANDATORY)
- **Header Placement**: The primary slicers (e.g., Kota/Region, Kategori, Rentang Tanggal) MUST be pinned directly in the sticky Header/Subheader bar.
- **Active Filter Chips**: Selected filters appear immediately as chips in the header: `[ 📍 Kota: Bandung ✕ ]`.
- **Instant Unfilter / Clear**: Clicking the `✕` on a chip or clicking `[ Reset / Clear All ]` restores the full dataset instantly.

## 3. DEPENDENCY & CONFLICTS
- Cascading logic is mandatory (Provinsi -> Kota -> Cabang).
- If filters conflict resulting in 0 rows, NEVER show an empty broken chart. Show an explicit "No data matches the current filters" state with recovery actions.

## 4. ANALYTICAL SAFETY
- Filtering must preserve metric semantics (e.g., recalculating Margin as SUM(Profit)/SUM(Revenue), NOT average of rows).
- Warn users if the filtered sample size is too small for statistical significance.

## 5. UNIVERSAL CROSS-FILTERING (CLICK-TO-FILTER PROTOCOL)
Every visual element representing a discrete categorical entity MUST support 2-way cross-filtering.

### Implementation Pattern (ECharts + Vanilla JS State Engine):
```javascript
// Global Analytical State
const state = {
  selectedCity: 'All', // e.g. 'Bandung', 'Jakarta', or 'All'
  selectedCategory: 'All',
  dateRange: 'YTD'
};

// 1. Bind Click Handler to ECharts instances
chartRegional.on('click', function(params) {
  const clickedCity = params.name; // e.g. 'Bandung'
  toggleCityFilter(clickedCity);
});

// 2. Toggle and Dispatch Filter State
function toggleCityFilter(city) {
  if (state.selectedCity === city) {
    state.selectedCity = 'All'; // Click again to unfilter
  } else {
    state.selectedCity = city; // Auto-filter to clicked city
  }
  syncHeaderSlicers();
  recalculateAndRenderAll();
}

// 3. Recalculate from Single Source of Truth
function recalculateAndRenderAll() {
  const filtered = rawTransactions.filter(d => 
    (state.selectedCity === 'All' || d.city === state.selectedCity) &&
    (state.selectedCategory === 'All' || d.category === state.selectedCategory)
  );

  updateKPIs(filtered);
  updateTrendChart(filtered);
  updateCategoryChart(filtered);
  updateRegionalChart(filtered, state.selectedCity); // Highlights Bandung, dims others
  updateDetailTable(filtered);
}
```

### Visual Focus Rule during Cross-Filtering:
- The selected entity (e.g. Bandung) remains brightly colored (e.g. `#3B82F6` or `#10B981`).
- All other non-selected entities are dimmed to `opacity: 0.35` so the user retains visual comparison without distraction.
- The header slicer dropdown automatically syncs to display "Bandung".