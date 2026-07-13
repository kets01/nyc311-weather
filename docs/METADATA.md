# Descriptive Metadata Records

Structural metadata (column-by-column: names, types, units, missingness) lives in the data
dictionaries (`data_dictionary_311.md`, `data_dictionary_weather.md`,
`data_dictionary_analysis_daily.md`). This file is the other kind: **descriptive metadata** — the
record-level facts (title, publisher, identifier, license, coverage, keywords, date) that let
someone find and cite the dataset *before* they open a single column.

Fields follow [Dublin Core](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
element names, with [DataCite](https://schema.datacite.org/) equivalents noted where they differ —
**in spirit, not as a formal XML/JSON record.** This project doesn't deposit to a repository with
structured metadata support yet; Phase 9's planned Zenodo deposit is where these same facts would
become an actual machine-readable DataCite record, generated from the Zenodo upload form rather
than hand-written here. Three records: the two inbound source datasets, and this project's own
derived output (relevant groundwork for that Phase 9 deposit).

---

## Record 1 — NYC 311 Service Requests (2025 subset used in this project)

| Dublin Core term | Value |
|---|---|
| Title | NYC 311 Service Requests from 2010 to Present — 2025 subset (Jan–Feb, Jul–Aug) |
| Creator / Publisher | City of New York (NYC Open Data portal; dataset maintained under NYC's 311 program) |
| Identifier | Socrata dataset ID `erm2-nwe9`; accessed at `https://data.cityofnewyork.us/resource/erm2-nwe9.csv` |
| Source | Socrata SODA API, server-side `$select`/`$where`/`$order` query (full URL in `data/DOWNLOAD_LOG.md`) |
| Date | Continuously updated by the publisher; **snapshot used here: 2026-07-12** (see Timeliness note below) |
| Type | Dataset (tabular, event-level records) |
| Format | CSV |
| Language | en |
| Coverage — temporal | 2025-01-01 to 2025-02-28 and 2025-07-01 to 2025-08-31 (winter/summer subset of the full 2010–present dataset) |
| Coverage — spatial | New York City, USA (5 boroughs) |
| Subject / Keywords | 311, service requests, complaints, municipal government, urban services, New York City |
| Description | 1,223,457 rows (603,544 + 619,913); ~12 columns retained via `$select` out of 43 in the source (see `docs/data_dictionary_311.md`) |
| Rights / License | Local Law 11 of 2012 (NYC Admin Code § 23-502(d)) — mandated publication without restriction, registration, or license; effectively public-domain-equivalent. Full reasoning: `docs/DMP.md` §VII |
| Relation | Joined with Record 2 by date to produce Record 3 (`data/processed/analysis_daily.csv`) |

**DataCite note:** DataCite's `Identifier` element expects a persistent, resolvable ID (typically a
DOI); the source dataset itself has no DOI — the Socrata dataset ID plus this project's own frozen
snapshot (SHA-256 checksum in `data/DOWNLOAD_LOG.md`) stand in for one. A DOI only enters the
picture at Phase 9, for this project's own derived output (Record 3), not for the untouched inbound
source.

## Record 2 — NOAA Daily Weather Summaries (Central Park, 2025)

| Dublin Core term | Value |
|---|---|
| Title | Daily Summaries — Central Park, NY (Station USW00094728), Jan–Aug 2025 |
| Creator / Publisher | NOAA National Centers for Environmental Information (NCEI) |
| Identifier | GHCN Daily station ID `USW00094728`; NCEI Access API `dataset=daily-summaries` |
| Source | NOAA NCEI Access API, `https://www.ncei.noaa.gov/access/services/data/v1` (full URL in `data/DOWNLOAD_LOG.md`) |
| Date | Continuously corrected retroactively by the publisher; **snapshot used here: 2026-07-12** |
| Type | Dataset (tabular, daily observations) |
| Format | CSV |
| Language | en |
| Coverage — temporal | 2025-01-01 to 2025-08-31 (243 calendar days, no gaps) |
| Coverage — spatial | Central Park, Manhattan, New York City, USA (single station) |
| Subject / Keywords | weather, climate, daily summaries, temperature, precipitation, snowfall |
| Description | 243 rows, 4 variables retained (TMAX, TMIN, PRCP, SNOW), `units=metric` requested explicitly (see `docs/data_dictionary_weather.md`) |
| Rights / License | US federal government work, not copyrightable domestically (17 U.S.C. § 105); NCEI additionally applies CC0 1.0 Universal Public Domain Dedication. Full reasoning: `docs/DMP.md` §VII |
| Relation | Joined with Record 1 by date to produce Record 3 (`data/processed/analysis_daily.csv`) |

## Record 3 — Derived: NYC 311 & Weather, Daily Category Counts (this project's own output)

| Dublin Core term | Value |
|---|---|
| Title | NYC 311 & Weather (2025) — Daily Request Counts by Category, Joined with Weather |
| Creator | kemki (this project) |
| Identifier | Not yet minted — planned as a Zenodo-reserved temporary DOI, separate from the code's own DOI (ROADMAP.md Phase 9.2); not a real/published identifier yet |
| Source | Derived from Record 1 + Record 2 via `notebooks/04_integrate.ipynb` |
| Date | Produced 2026-07-13 (Phase 4); "as of" tag inherited from both source snapshots (2026-07-12) |
| Type | Dataset (tabular, daily aggregate) |
| Format | CSV |
| Language | en |
| Coverage — temporal | 2025-01-01 to 2025-02-28 and 2025-07-01 to 2025-08-31 |
| Coverage — spatial | New York City, USA (citywide; single weather station, no borough-level weather — see Representativeness in `docs/QUALITY_FINDINGS.md`) |
| Subject / Keywords | 311, weather, NYC, service requests, data integration, association analysis |
| Description | 1,143 rows, one per (date, complaint category); `n_requests` sums to the full cleaned 311 event count (see `docs/data_dictionary_analysis_daily.md`) |
| Rights / License | CC BY 4.0 (data/docs) — a scholarly-norm choice made freely, not one the inbound sources required (both are CC0-equivalent). Full reasoning: `docs/DMP.md` §VII |
| Relation | Derived from Record 1 + Record 2; documented in `docs/QUALITY_FINDINGS.md` (quality decisions applied before integration) and `docs/data_dictionary_analysis_daily.md` (schema) |

---

## Consistency note (Phase 7.2)

Checked license wording, dataset identifiers (`erm2-nwe9`, `USW00094728`), and the snapshot date
(2026-07-12) against README.md, docs/DMP.md, and all three data dictionaries — all match. One real
inconsistency found and fixed during this pass: `CONTEXT.md`'s DMP-topic table (§6, Naming row) had
a stale example filename left over from before Phase 1 — `311_raw_jan-feb_downloaded_2026-07-15.csv`,
using both a placeholder date and a naming pattern that isn't what Phase 1 actually settled on.
Corrected to the real filename, `311_2025-01_2025-02_downloaded_2026-07-12.csv`, matching
`data/DOWNLOAD_LOG.md` and the actual files in `data/raw/`.
