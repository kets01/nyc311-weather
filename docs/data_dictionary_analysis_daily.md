# Data Dictionary — `data/processed/analysis_daily.csv`

Produced by `notebooks/04_integrate.ipynb`: 311 requests aggregated to (date, category), then
LEFT JOINed with cleaned daily weather on `date`. One row = one complaint category on one day.
1,143 rows (121 distinct dates × up to 10 categories — not all 10 categories have a nonzero count
every single day, so the table is sparse rather than a full 121×10 grid).

| Column | Type | Unit | Meaning | Example | Missing behavior |
|---|---|---|---|---|---|
| `date` | date | — | Calendar date (NYC local, from `created_date`) | `2025-02-08` | 0% missing |
| `category` | string (enum, 10 values) | — | Controlled-vocabulary complaint category from `data/complaint_category_map.csv` | `SNOW_ICE` | 0% missing |
| `n_requests` | integer | count | Number of 311 reports of this category on this date | `47` | 0% missing; always ≥ 1 (zero-count date/category combos are simply absent rows, not explicit 0s) |
| `TMAX` | float | °C | Daily maximum temperature (Central Park) | `1.7` | 0% missing in this window (100% weather coverage, see `docs/QUALITY_FINDINGS.md`) |
| `TMIN` | float | °C | Daily minimum temperature | `-3.2` | 0% missing in this window |
| `PRCP` | float | mm | Daily precipitation | `15.5` | 0% missing in this window |
| `SNOW` | float | mm | Daily snowfall | `76.0` | 0% missing in this window |
| `weekday` | string | — | Day-of-week name | `Saturday` | 0% missing |
| `is_weekend` | boolean | — | `True` for Saturday/Sunday | `True` | 0% missing |

## Provenance

- Source tables: `data/processed/311_clean.csv` (1,223,457 rows, cleaned from the two raw 311
  windows) and `data/processed/weather_clean.csv` (243 rows, reindexed onto the full
  2025-01-01..2025-08-31 calendar).
- Aggregation: `311_clean.csv.groupby(["date", "category"]).size()`.
- Join: LEFT JOIN of the aggregated 311 table onto `weather_clean.csv` by `date` (311 side kept
  whole even for any date that might lack weather — none do, in this window).
- Validated in `04_integrate.ipynb` §4.4: row count unchanged by the join (1,143 → 1,143),
  `n_requests` sum equals the cleaned 311 event count exactly (1,223,457), 100% of the 121 dates
  have complete weather, and a spot check against the known biggest in-window snow day
  (2025-02-08, SNOW = 76.0 mm) matches the raw weather file exactly.
