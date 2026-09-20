# Phase E: Design & Theme Engine

## CORE MANDATE: THE README EXPECTATION BASELINE
The 10 example artifacts showcased in the repository's README.md are not just mockups; they are the **Minimum Accepted Standard**. Users expect the AI to generate outputs that *exactly* match or exceed the visual fidelity, color precision, and density of those examples.

### 1. The Apex Enterprise Dark Theme (Default)
To guarantee consistency with the README expectations, you MUST adhere to this exact color and styling matrix:

**Background & Surface (Deep Space Blue/Gray):**
- **App Background**: #0B1120 or #050505
- **Card/Panel Surface**: #111827 or #1E293B
- **Borders/Dividers**: #374151 (Thin, solid)

**Semantic Data Palette (High Contrast):**
- **Primary Data (Base)**: #3B82F6 (Electric Blue) or #00f0ff (Cyan)
- **Positive / Success / Growth**: #10B981 (Emerald Green) or #00ff66
- **Negative / Churn / Alerts**: #EF4444 (Crimson Red) or #ff0055
- **Secondary / Comparison**: #8B5CF6 (Purple) or #F59E0B (Amber)

**Typography & Text:**
- **Primary Text**: #F9FAFB (Crisp White)
- **Muted/Axis Text**: #9CA3AF (Cool Gray)
- **Numbers/KPIs**: Must use Monospace font (JetBrains Mono, Fira Code, or Courier) for perfect vertical alignment.
- **Labels/Headers**: Clean sans-serif (Inter, Roboto, Helvetica).

### 2. Layout Density & Structure
- **No Wasted Space**: Embrace high-density layouts. Use CSS Grid or Flexbox to pack information tightly like a Bloomberg Terminal or professional SaaS dashboard.
- **AI Insight Sidebar**: Every dashboard MUST include a dedicated panel where the AI Auto-Critique (Phase F) writes out its findings (e.g., anomalies, drop-off rates).

### 3. Glassmorphism & Cinematic Overrides (When Max Complexity is Needed)
If the data requires deep relational focus (e.g., Sankey, Market Basket):
- Apply ackdrop-filter: blur(12px) to panels.
- Add subtle radial gradient glows behind critical data points or structural break annotations.

### 4. Alternative Themes (Only if Explicitly Requested)
- **Corporate Light**: Background #F8FAFC, Cards #FFFFFF, Text #0F172A.