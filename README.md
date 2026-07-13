# NYC 311 & Weather (2025) — MoSD Exam Project

**Research question:** How do weather conditions (temperature, precipitation, snow) influence the
daily number and category mix of NYC 311 service requests in 2025?

Full reasoning, hypotheses, limitations, DMP, metadata, provenance and FAIR discussion live in
[CONTEXT.md](CONTEXT.md). Execution plan and progress checklist: [ROADMAP.md](ROADMAP.md).

## Data sources

| Dataset | Source | License |
|---|---|---|
| NYC 311 Service Requests (subset, 2025) | [NYC Open Data — `erm2-nwe9`](https://data.cityofnewyork.us/resource/erm2-nwe9.csv) via the Socrata SODA API | Local Law 11 of 2012 (NYC Admin Code § 23-502(d)) — mandated publication without restriction/license/registration; effectively public-domain-equivalent |
| Daily weather, Central Park station `USW00094728` (2025) | [NOAA NCEI Access API](https://www.ncei.noaa.gov/access/services/data/v1) | Public domain (17 U.S.C. § 105, US government work); NCEI applies CC0 1.0 to its holdings |

Both inbound sources are effectively CC0-equivalent — no required attribution, no share-alike, no
restriction on how derived work is licensed. See [docs/DMP.md](docs/DMP.md) §VII Data publishing &
licensing for the full reasoning and citations.

**Subset chosen:** Jan–Feb 2025 + Jul–Aug 2025 (winter vs. summer contrast, small enough for a
laptop). Both datasets are downloaded directly from their APIs by `notebooks/00_download.ipynb` —
the query URL is code, so acquisition itself is reproducible. Each fetch is additionally logged in
`data/DOWNLOAD_LOG.md` (URL, date, size, row count), because both sources revise data retroactively.

**At a glance (from `01_explore_311.ipynb` / `02_explore_weather.ipynb`, both descriptive-only —
see `docs/QUALITY_FINDINGS.md` for the full quality assessment):**
- 311: 1,223,457 rows combined (603,544 winter + 619,913 summer), 0 exact duplicate `unique_key`s,
  180 distinct raw `complaint_type` values mapped onto a ~10-value controlled vocabulary
  (`data/complaint_category_map.csv`, 5.7% falls into `OTHER`).
- 311 missingness: `descriptor` 2.60%, `closed_date` 1.49% (expected for open cases), `latitude`/
  `longitude` 1.34%, `incident_zip` 0.78%; `borough` has 811 rows (0.07%) holding the placeholder
  `Unspecified` rather than a real NaN.
- Weather: 243/243 calendar days present (2025-01-01..2025-08-31), 0% missing values, TMAX range
  −7.1..37.2 °C confirms `units=metric` was honored.
- Full data dictionaries: [docs/data_dictionary_311.md](docs/data_dictionary_311.md),
  [docs/data_dictionary_weather.md](docs/data_dictionary_weather.md). Descriptive (title/publisher/
  identifier/license/coverage/keywords) records per dataset: [docs/METADATA.md](docs/METADATA.md).

**Cleaned & joined (`04_integrate.ipynb`, see `docs/QUALITY_FINDINGS.md` for the decisions this
acts on):** `data/processed/analysis_daily.csv` — one row per (date, category), 1,143 rows,
LEFT-JOINed with weather by date. Validated: row count unchanged by the join, `n_requests` sum
equals the cleaned 311 event count (1,223,457) exactly, 100% of the 121 dates have complete
weather, spot-checked against the known biggest in-window snow day. Dictionary:
[docs/data_dictionary_analysis_daily.md](docs/data_dictionary_analysis_daily.md).

Note: `data/processed/311_clean.csv` (the row-level cleaned 311 table, ~248 MB) is gitignored —
too large for GitHub's per-file limit, and fully regenerable by re-running `04_integrate.ipynb`
against the frozen raw files. `weather_clean.csv` and `analysis_daily.csv` are small (both well
under 100 KB) and are committed as-is.

## Folder structure

```
nyc311-weather/
├── README.md                     # this file
├── requirements.txt               # pinned packages (pip freeze)
├── .gitignore                     # ignores data/raw/, venv, checkpoints
├── LICENSE                        # MIT (code); docs/data are CC BY 4.0, see docs/DMP.md
├── CONTEXT.md                     # full project reference: RQ, DMP, quality plan, FAIR, glossary
├── ROADMAP.md                     # step-by-step execution plan / checklist
├── data/
│   ├── raw/                       # downloaded files — NEVER edited (gitignored)
│   ├── processed/                 # cleaned/joined tables saved by notebooks
│   ├── DOWNLOAD_LOG.md             # per file: URL, filters, date, size, rows
│   └── complaint_category_map.csv  # controlled vocabulary: raw complaint type -> category
├── notebooks/
│   ├── 00_download.ipynb
│   ├── 01_explore_311.ipynb
│   ├── 02_explore_weather.ipynb
│   ├── 03_quality.ipynb
│   ├── 04_integrate.ipynb
│   └── 05_analysis.ipynb
├── docs/
│   ├── DMP.md
│   ├── METADATA.md               # descriptive (Dublin Core/DataCite-style) records per dataset
│   ├── QUALITY_FINDINGS.md
│   ├── data_dictionary_311.md
│   ├── data_dictionary_weather.md
│   ├── data_dictionary_analysis_daily.md
│   ├── FAIR_and_provenance.md
│   └── notebooks_html/            # notebooks exported to static HTML (Phase 8 preservation layer)
├── figures/                        # exported plots (fig_00_....png … fig_07_provenance_chain.png)
└── presentation/                   # slides source + final PDF
```

## Environment

- Python 3.11.9 (see also the version print in each notebook's first cell)
- Dependencies pinned in [requirements.txt](requirements.txt) (`pip freeze`)

Setup:

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash; use .venv\Scripts\activate on cmd/PowerShell
pip install -r requirements.txt
```

## Backup

3-2-1 rule: laptop (this repo) + GitHub remote (cloud/off-site, covers code/docs/notebooks) +
external drive/USB (still to do, covers `data/raw/` which is gitignored). See `docs/DMP.md` for
the concrete, dated record of when copies were made and restore-tested.

Remote: https://github.com/kets01/nyc311-weather

## License

Code (notebooks, scripts) is MIT-licensed — see [LICENSE](LICENSE). Documentation and the derived
tables in `data/processed/` are CC BY 4.0 — an attribution-required choice made freely, not one
required by the inbound sources (both are effectively CC0-equivalent, see Data sources above). The
original source data keeps its own inbound status regardless. Full reasoning in
`docs/DMP.md` §VII Data publishing & licensing.

**Planned publication (not executed):** two separate Zenodo deposits — software (this repo) and
data (`data/processed/` + docs) — each with its own DOI, cross-linked via DataCite related
identifiers. Temporary DOIs reserved (not published) via the Zenodo Sandbox on 2026-07-13 — these
are sandbox-only, non-resolving identifiers, not a real deposit:
- Software DOI: `10.5072/zenodo.562104`
- Data DOI: `10.5072/zenodo.562134`

See `docs/DMP.md` §VII for the full plan.

## Future work

Ideas surfaced during `05_analysis.ipynb` but deliberately not pursued — analysis has a hard time
limit for this exam, so these are documented instead of chased:

- **Disaggregate `NOISE` into indoor vs. outdoor sub-types** before testing H4. The aggregated
  category (which bundles residential, street, commercial, vehicle, park, and helicopter noise)
  showed no significant correlation with TMAX (r = 0.086, p = 0.35) — but residential noise is
  ~58% of that category and is plausibly weather-independent, which could be diluting a real
  outdoor-specific signal. Re-running H4 on just `Noise - Street/Sidewalk` / `Noise - Park` /
  `Noise - Vehicle` would be a cleaner test.
- **Sub-daily / lagged join.** The biggest single FLOODING day (2025-07-31, 543 reports) had only
  modest same-day rain (8.1 mm), and the 2025-07-14 storm's complaint volume spilled into the next
  calendar day. A join on "rain in the last 24–36 hours" rather than same-calendar-day PRCP would
  likely sharpen the H1 relationship.
- **Fill the March–June gap.** This project deliberately used a winter+summer subset for contrast;
  a full-year download would allow spring/fall as a natural intermediate check on the seasonality
  confound, beyond the single winter-only re-check already done for H2.
- **Borough-level analysis**, joining the representativeness finding from `QUALITY_FINDINGS.md`
  (Bronx complaints/capita roughly double Staten Island's) with weather — out of scope here since
  the project uses a single citywide weather station.
