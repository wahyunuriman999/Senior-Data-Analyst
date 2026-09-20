# Phase E: Design & Theme Engine

## CORE MANDATE: THE APEX MAXIMALIST AESTHETIC
By default, all generated dashboards and UI mockups must utilize the **Cinematic Dark Maximalist** theme unless explicitly requested otherwise by the user.

### 1. The Cinematic Dark Glassmorphism Theme
- **Base Background**: Deep true black or cyber-dark (#050505, #09090b). Use subtle radial gradients to create depth.
- **Panels & Cards**: Use Glassmorphism. Semi-transparent dark backgrounds (gba(20,20,25,0.7)) with heavy background blur (ackdrop-filter: blur(12px)).
- **Borders**: Hairline translucent borders (gba(255,255,255,0.1)) to separate sections.
- **Accent Colors (Neon/Cyber)**: 
  - Cyan (#00f0ff) for primary data.
  - Pink/Crimson (#ff0055) for drop-offs/churn/alerts.
  - Purple (#b026ff) for secondary cohorts.
  - Emerald Green (#00ff66) for success targets.
- **Shadows**: Glowing box shadows using the accent colors on hover or for critical data points.

### 2. Typography Hierarchy
- **Data/Numbers**: Must use a monospace font (e.g., JetBrains Mono, Fira Code) for strict alignment and futuristic analytical feel.
- **UI/Labels**: Clean sans-serif (e.g., Inter, Roboto) for readability.
- **Titles**: Uppercase, heavy font weight (800), often with linear-gradient text clips.

### 3. Layout Density (High-Density Analytical)
- Reject sparse layouts. Utilize CSS Grid to pack dense information securely.
- Always include an **AI Insight Sidebar** (A dedicated panel where AI auto-generates text insights about anomalies, drop-offs, and stats).

### 4. Alternative Themes (Only if Requested)
- **Corporate High-Density**: Light mode, grid constraints, low whitespace, semantic red/green/black.
- **SaaS Clean**: Light mode, card-based, generous whitespace, teal/blue accents, soft shadows.