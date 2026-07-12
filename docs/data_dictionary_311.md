# Data Dictionary — NYC 311 Service Requests

Source: NYC Open Data, dataset `erm2-nwe9`, fetched via the Socrata SODA API
(see `notebooks/00_download.ipynb`, `data/DOWNLOAD_LOG.md`). Only the columns below were
requested via `$select` — the source table has 43 columns in total; these ~10 are what this
project actually uses (see CONTEXT.md §3). Numbers below are from the combined winter+summer 2025
subset (1,223,457 rows), computed in `notebooks/01_explore_311.ipynb`.

| Column | Type | Unit | Meaning | Example | Missing behavior |
|---|---|---|---|---|---|
| `unique_key` | integer | — | Unique ID for the service request | `63577994` | 0% missing; 0 duplicated values in this subset |
| `created_date` | datetime string (ISO 8601) | NYC local time | When the request was filed | `2025-01-01T00:00:12.000` | 0% missing |
| `closed_date` | datetime string (ISO 8601) | NYC local time | When the request was closed | `2025-01-02T17:05:54.000` | 1.49% missing — legitimate for still-open cases, not a defect |
| `agency` | string (code) | — | Responsible agency, short code | `NYPD`, `HPD`, `DSNY` | 0% missing |
| `agency_name` | string | — | Responsible agency, full name | `New York City Police Department` | 0% missing; cross-checked against `agency` in Phase 3 for consistency |
| `complaint_type` | string (free-standing category) | — | Raw complaint category (180 distinct values in this subset) | `Noise - Residential` | 0% missing; mapped to a ~10-value controlled vocabulary via `data/complaint_category_map.csv` |
| `descriptor` | string | — | Sub-category detail for the complaint type | `Loud Music/Party` | 2.60% missing |
| `borough` | string | — | NYC borough | `BRONX` | 0% missing as NaN, but 811 rows (0.07%) hold the placeholder value `Unspecified` — a disguised missing value, flagged in Phase 3 |
| `incident_zip` | float (should be 5-digit code) | — | ZIP code of the incident | `10466.0` | 0.78% missing; validity (5-digit format, plausible NYC range) checked in Phase 3 |
| `latitude` | float | decimal degrees | Incident latitude | `40.8919` | 1.34% missing; range-checked against the NYC bounding box in Phase 3 |
| `longitude` | float | decimal degrees | Incident longitude | `-73.8602` | 1.34% missing; range-checked against the NYC bounding box in Phase 3 |
| `status` | string (enum) | — | Request status | `Closed`, `Open`, `In Progress`, `Pending`, `Assigned`, `Started`, `Unspecified` | 0% missing |

**Not requested from the source** (43 columns total; the 31 not listed above — e.g. `location_type`,
`community_board`, `bbl`, `vehicle_type` — were dropped at the API level via `$select` to reduce
download size and are out of scope for this project's research question).
