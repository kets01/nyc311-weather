# Data Dictionary — NOAA Daily Weather (Central Park, USW00094728)

Source: NOAA NCEI Access API, `daily-summaries` dataset, station `USW00094728`
(see `notebooks/00_download.ipynb`, `data/DOWNLOAD_LOG.md`). `units=metric` was requested
explicitly. Numbers below are from the 2025-01-01..2025-08-31 download (243 rows), computed in
`notebooks/02_explore_weather.ipynb`.

| Column | Type | Unit | Meaning | Example | Missing behavior |
|---|---|---|---|---|---|
| `STATION` | string | — | GHCN station identifier | `USW00094728` | 0% missing |
| `DATE` | date string (ISO 8601) | — | Calendar date of the observation | `2025-01-01` | 0% missing; 243/243 calendar days present in this window (no gaps) |
| `PRCP` | float | mm | Total daily precipitation | `0.0` | 0% missing in this window; observed range 0.0–67.1 mm |
| `SNOW` | float | mm | Total daily snowfall | `0.0` | 0% missing in this window; observed range 0.0–76.0 mm |
| `TMAX` | float | °C | Daily maximum temperature | `10.6` | 0% missing in this window; observed range −7.1 .. 37.2 °C — plausible for NYC, confirms `units=metric` worked (tenths-of-degree GHCN raw values would show implausible magnitudes like ~250) |
| `TMIN` | float | °C | Daily minimum temperature | `3.9` | 0% missing in this window; observed range −12.1 .. 27.2 °C |

**Note:** NOAA can retroactively correct daily-summary values after initial publication — the
download date recorded in `data/DOWNLOAD_LOG.md` pins down which version of these values this
project analyzed ("data as of 2026-07-12").
