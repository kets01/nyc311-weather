# Download Log

Every file in `data/raw/` is fetched by `notebooks/00_download.ipynb`, which contains the exact
query URLs (versioned in Git). This log pins down the *snapshot*: both sources revise data
retroactively, so "data as of &lt;download date&gt;" needs a dated record independent of the code.
`data/raw/` itself is gitignored (large files) — this log plus the notebook are what stand in for
it in version control.

---

## 311_2025-01_2025-02_downloaded_2026-07-12.csv

- **Source:** NYC Open Data, Socrata SODA API, dataset `erm2-nwe9`
- **URL:** `https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$select=unique_key,created_date,closed_date,agency,agency_name,complaint_type,descriptor,borough,incident_zip,latitude,longitude,status&$where=created_date between '2025-01-01T00:00:00' and '2025-02-28T23:59:59'&$limit=1000000&$order=created_date`
- **Download date:** 2026-07-12
- **Rows:** 603,544 (below the 1,000,000 `$limit` → not truncated)
- **Date range in file:** 2025-01-01T00:00:12 to 2025-02-28T23:59:48 (matches requested window)
- **File size:** 113,789.4 KB (~111.2 MB)
- **SHA-256:** `09c22339dc6936888ec8b984f300fdb23ff458b1867dc8c1cf997debf70b5b58`
- **Note:** first attempt requested all 43 source columns and failed with `IncompleteRead` after
  ~140 MB transferred. Re-run with `$select` restricted to the ~12 columns this project uses —
  smaller and reliable. See notebook §1 for the reasoning.

## 311_2025-07_2025-08_downloaded_2026-07-12.csv

- **Source:** NYC Open Data, Socrata SODA API, dataset `erm2-nwe9`
- **URL:** `https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$select=unique_key,created_date,closed_date,agency,agency_name,complaint_type,descriptor,borough,incident_zip,latitude,longitude,status&$where=created_date between '2025-07-01T00:00:00' and '2025-08-31T23:59:59'&$limit=1000000&$order=created_date`
- **Download date:** 2026-07-12
- **Rows:** 619,913 (below the 1,000,000 `$limit` → not truncated)
- **Date range in file:** 2025-07-01T00:00:23 to 2025-08-31T23:59:56 (matches requested window)
- **File size:** 115,755.0 KB (~113.0 MB)
- **SHA-256:** `242d24d25bd36d273b29bfb9a1965d9d0dbedf2d63dff285eea219f1baa1a1a5`

## weather_centralpark_2025_downloaded_2026-07-12.csv

- **Source:** NOAA NCEI Access API, `daily-summaries` dataset, station `USW00094728` (NY City
  Central Park)
- **URL:** `https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=USW00094728&startDate=2025-01-01&endDate=2025-08-31&dataTypes=TMAX,TMIN,PRCP,SNOW&units=metric&format=csv`
- **Download date:** 2026-07-12
- **Rows:** 243 (exactly one row per calendar day, 2025-01-01 to 2025-08-31 → no missing days in
  this window)
- **Date range in file:** 2025-01-01 to 2025-08-31 (matches requested window)
- **File size:** 9.9 KB
- **SHA-256:** `923c5108e6788d1f1e0a9f004a7ed36563cbb5353c4d067f70457e0d103bf15a`
- **Units check:** `units=metric` requested explicitly; TMAX observed range −7.1 °C .. 37.2 °C,
  plausible for NYC (would look like ~250 if tenths-of-degree units had been returned instead).

---

## Reproducibility note

Re-running `00_download.ipynb` today would **not** produce byte-identical files: 311 records are
updated after creation (status, closed date, etc.) and NOAA corrects observations retroactively.
That is exactly why this log exists — the notebook reproduces the *query*, this log fixes the
*snapshot* the analysis is actually based on.
