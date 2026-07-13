# Descriptive Metadata Records

Structural metadata (column-by-column: names, types, units, missingness) lives in the data
dictionaries (`data_dictionary_311.md`, `data_dictionary_weather.md`,
`data_dictionary_analysis_daily.md`). This file is the other kind: **descriptive metadata** — the
record-level facts (title, publisher, identifier, license, coverage, keywords, date) that let
someone find and cite the dataset *before* they open a single column.

Fields follow [Dublin Core](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
element names, with [DataCite](https://schema.datacite.org/) equivalents noted where they differ.
**This table itself is human-readable only** — the point of a Markdown table is to be easy to scan,
not to be parsed by a machine. Each record below now has a **machine-readable counterpart**: a
DataCite Metadata Schema 4.4 JSON file in [`metadata/`](metadata/), with an explicit `identifiers`
block (F3: metadata includes the identifier of the data it describes), a `rightsList` with a real
`rightsUri` rather than a license *name* (R1.1, and answers "is the license URL-encoded?" — yes,
for the three records where a canonical rights URI exists), and `relatedIdentifiers` with a
`relationType` (`IsDerivedFrom`, `IsSourceOf`, `IsSupplementTo`, …) — I3's "qualified references to
other (meta)data," machine-parseable rather than prose. Four records now, not three: the two
inbound source datasets, this project's own derived data output, and — added when this gap was
caught — the **software** itself, which previously had a reserved DOI (see Record 3/4 below) but no
descriptive record of its own.

| Record | Markdown (this file) | Machine-readable (DataCite JSON) |
|---|---|---|
| 1 — 311 source | below | [`metadata/record_311.json`](metadata/record_311.json) |
| 2 — weather source | below | [`metadata/record_weather.json`](metadata/record_weather.json) |
| 3 — derived data | below | [`metadata/record_analysis_daily.json`](metadata/record_analysis_daily.json) |
| 4 — software | below | [`metadata/record_software.json`](metadata/record_software.json) |

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
| Rights / License | Local Law 11 of 2012 (NYC Admin Code § 23-502(d)) — mandated publication without restriction, registration, or license; effectively public-domain-equivalent. `rightsUri`: `https://codelibrary.amlegal.com/codes/newyorkcity/latest/NYCadmin/0-0-0-204577` (the codified statute text itself — Local Law 11 has no Creative-Commons-style license URI since it's a legal mandate, not a CC license, so this is the closest real resolvable reference). Full reasoning: `docs/DMP.md` §VII |
| Relation | `IsSourceOf` → Record 3 (`10.5072/zenodo.562134`, machine-readable in `metadata/record_311.json`) |

**DataCite note:** DataCite's `Identifier` element expects a persistent, resolvable ID (typically a
DOI); the source dataset itself has no DOI — the Socrata dataset ID plus this project's own frozen
snapshot (SHA-256 checksum in `data/DOWNLOAD_LOG.md`) stand in for one, recorded as
`identifierType: "Local"` in `metadata/record_311.json` (DataCite's own vocabulary for exactly this
case — a stable local ID that isn't a global persistent identifier).

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
| Rights / License | US federal government work, not copyrightable domestically (17 U.S.C. § 105); NCEI additionally applies CC0 1.0 Universal Public Domain Dedication. `rightsUri`: `https://creativecommons.org/publicdomain/zero/1.0/` (NCEI's own stated CC0 policy page: `https://www.ncei.noaa.gov/archive`). Full reasoning: `docs/DMP.md` §VII |
| Relation | `IsSourceOf` → Record 3 (`10.5072/zenodo.562134`, machine-readable in `metadata/record_weather.json`) |

## Record 3 — Derived: NYC 311 & Weather, Daily Category Counts (this project's own output)

| Dublin Core term | Value |
|---|---|
| Title | NYC 311 & Weather (2025) — Daily Request Counts by Category, Joined with Weather |
| Creator | kemki (this project) |
| Identifier | `10.5072/zenodo.562134` — reserved (not published) via the Zenodo Sandbox, 2026-07-13 (ROADMAP.md Phase 9.2). **This is a Sandbox DOI: it does not resolve on the real `doi.org`**, it exists to demonstrate the reservation mechanic, distinct from the software's own DOI (Record 4) |
| Source | Derived from Record 1 + Record 2 via `notebooks/04_integrate.ipynb` |
| Date | Produced 2026-07-13 (Phase 4); "as of" tag inherited from both source snapshots (2026-07-12) |
| Type | Dataset (tabular, daily aggregate) |
| Format | CSV |
| Language | en |
| Coverage — temporal | 2025-01-01 to 2025-02-28 and 2025-07-01 to 2025-08-31 |
| Coverage — spatial | New York City, USA (citywide; single weather station, no borough-level weather — see Representativeness in `docs/QUALITY_FINDINGS.md`) |
| Subject / Keywords | 311, weather, NYC, service requests, data integration, association analysis |
| Description | 1,143 rows, one per (date, complaint category); `n_requests` sums to the full cleaned 311 event count (see `docs/data_dictionary_analysis_daily.md`) |
| Rights / License | CC BY 4.0 (data/docs) — a scholarly-norm choice made freely, not one the inbound sources required (both are CC0-equivalent). `rightsUri`: `https://creativecommons.org/licenses/by/4.0/`. Full reasoning: `docs/DMP.md` §VII |
| Relation | `IsDerivedFrom` → Record 1 + Record 2 (`erm2-nwe9`, `USW00094728`); `IsSupplementedBy` → Record 4 software DOI (`10.5072/zenodo.562104`). Also documented narratively in `docs/QUALITY_FINDINGS.md` (quality decisions applied before integration) and `docs/data_dictionary_analysis_daily.md` (schema) |

## Record 4 — Software: the code/notebooks (this project's own output)

Added alongside the other three — the software deposit had a reserved DOI (ROADMAP.md Phase 9.2)
but, until now, no descriptive record of its own, which was itself a gap in "does every object with
an identifier have metadata describing it?"

| Dublin Core term | Value |
|---|---|
| Title | nyc311-weather: notebooks and pipeline for the NYC 311 & Weather (2025) MoSD exam project |
| Creator | kemki (this project) |
| Identifier | `10.5072/zenodo.562104` — reserved (not published) via the Zenodo Sandbox, 2026-07-13. **Sandbox DOI, does not resolve on real `doi.org`** |
| Source | This GitHub repository: `https://github.com/kets01/nyc311-weather` |
| Date | Created 2026-07-12 to 2026-07-13 |
| Type | Software (Jupyter notebooks + supporting scripts) |
| Format | `.ipynb`, `.py` |
| Language | en (code + comments) |
| Coverage | N/A (software, not observational data) |
| Subject / Keywords | reproducible research, data pipeline, Python, pandas, Jupyter |
| Description | 6 numbered notebooks (`00_download` … `05_analysis`) plus documentation-generation scripts (`build_fig07_provenance_diagram.py`, `build_provenance_json.py`); pinned dependencies in `requirements.txt` |
| Rights / License | MIT License. `rightsUri`: `https://opensource.org/license/mit/` |
| Relation | `IsSupplementTo` → Record 3 data DOI (`10.5072/zenodo.562134`); `IsIdenticalTo` → the GitHub repository URL |

---

## Consistency note (Phase 7.2)

Checked license wording, dataset identifiers (`erm2-nwe9`, `USW00094728`), and the snapshot date
(2026-07-12) against README.md, docs/DMP.md, and all three data dictionaries — all match. One real
inconsistency found and fixed during this pass: `CONTEXT.md`'s DMP-topic table (§6, Naming row) had
a stale example filename left over from before Phase 1 — `311_raw_jan-feb_downloaded_2026-07-15.csv`,
using both a placeholder date and a naming pattern that isn't what Phase 1 actually settled on.
Corrected to the real filename, `311_2025-01_2025-02_downloaded_2026-07-12.csv`, matching
`data/DOWNLOAD_LOG.md` and the actual files in `data/raw/`.

**2026-07-13 addendum:** a follow-up audit (prompted by exam Q&A prep, not part of the original
roadmap) checked whether this file's claims actually held up to FAIR's machine-actionability
requirements rather than just looking complete to a human reader. Two real gaps found and fixed
here: Record 3's identifier was stale (said "not yet minted" after the DOI had already been
reserved in Phase 9), and there was no descriptive record at all for the software deposit despite
it having its own reserved DOI. See `docs/FAIR_and_provenance.md` for the rest of that audit
(machine-readable provenance, and the one figure that briefly had no committed generating code).
