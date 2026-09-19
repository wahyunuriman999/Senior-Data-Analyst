# Data Grain Engine
Before aggregation, determine the grain of the fact table.
- Is one row = one transaction? One user login? One daily snapshot?
- Never mix grains without explicit dimensional bridging.
- Beware of fan-out or Cartesian explosions when joining fact tables to multi-valued dimensions.
