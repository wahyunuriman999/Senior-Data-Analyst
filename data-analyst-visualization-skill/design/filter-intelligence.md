# ELITE DASHBOARD FILTER & SLICER SYSTEM

## 1. FILTER INTELLIGENCE (CARDINALITY MAPPING)
- **Low Cardinality (2-4)**: Use Segmented Controls or Radio Buttons (e.g., Gender, Segment). NEVER use dropdowns.
- **Medium Cardinality (5-20)**: Use Multi-select Checkbox Dropdowns.
- **High Cardinality (20+)**: Use Searchable Typeahead / Autocomplete.
- **Numeric**: Use Range Sliders or Min/Max inputs.
- **Dates**: Use Smart Presets (Last 30 Days, YTD) + Custom Range.

## 2. FILTER STATE & CHIPS
- Active filters MUST be visible as removable chips (e.g., [ Indonesia x ]).
- Do not clutter the header. Use a dedicated [ Filters (3) ] button that opens a Filter Panel.

## 3. DEPENDENCY & CONFLICTS
- Cascading logic is mandatory (Category -> Product).
- If filters conflict resulting in 0 rows, NEVER show an empty broken chart. Show an explicit No data matches the current filters state with recovery actions.

## 4. ANALYTICAL SAFETY
- Filtering must preserve metric semantics (e.g., recalculating Margin as SUM(Profit)/SUM(Revenue), NOT average of rows).
- Warn users if the filtered sample size is too small for statistical significance.