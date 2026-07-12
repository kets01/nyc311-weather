# NYC 311 & Weather (2025) — MoSD Exam Project

**Research question:** How do weather conditions (temperature, precipitation, snow) influence the
daily number and category mix of NYC 311 service requests in 2025?

Full reasoning, hypotheses, limitations, DMP, metadata, provenance and FAIR discussion live in
[CONTEXT.md](CONTEXT.md). Execution plan and progress checklist: [ROADMAP.md](ROADMAP.md).

## Data sources

| Dataset | Source | License |
|---|---|---|
| NYC 311 Service Requests (subset, 2025) | [NYC Open Data — `erm2-nwe9`](https://data.cityofnewyork.us/resource/erm2-nwe9.csv) via the Socrata SODA API | NYC Open Data Terms of Use |
| Daily weather, Central Park station `USW00094728` (2025) | [NOAA NCEI Access API](https://www.ncei.noaa.gov/access/services/data/v1) | US public domain |

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
  [docs/data_dictionary_weather.md](docs/data_dictionary_weather.md).

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
│   ├── QUALITY_FINDINGS.md
│   ├── data_dictionary_311.md
│   ├── data_dictionary_weather.md
│   ├── data_dictionary_analysis_daily.md
│   └── FAIR_and_provenance.md
├── figures/                        # exported plots (fig_01_....png)
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

## Future work

(filled in during Phase 5 — analysis)
