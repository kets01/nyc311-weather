# Data Management Plan

> Filled in phase by phase as work progressed; finalized in Phase 6, restructured on 2026-07-13 to
> follow the BiodivERsA/Belmont Forum proposed DMP template (Goudeseune et al., 2019, *Guidance
> document on data management, open data, and the production of Data Management Plans*, §4.2,
> DOI: 10.5281/zenodo.3448251) — sections I–VIII plus Costs. No content from the earlier version was
> removed in the restructure, only reorganized and, where the template asked a question this
> project hadn't answered yet in one place, completed. Every entry below is what was *actually
> done*, not the original plan — see CONTEXT.md §6 for the plan this replaces. Content current as
> of 2026-07-13, after Phases 0–5.

## I. Data manager(s)

One-person project, but the roles are named because they'd be separate people on a real team:
**researcher** (research question, hypotheses, analysis), **data steward** (quality assessment,
metadata, controlled vocabulary), **archivist** (backups, version control, preservation). All
three hats worn by the same person (kemki) throughout. No specialized/external data expert on the
team beyond this. This document is stored as a project file (`docs/DMP.md`) and updated as work
progresses rather than written once and frozen.

## II. Data identification & description

**Purpose of the research:** How do weather conditions (temperature, precipitation, snow) influence
the daily number and category mix of NYC 311 service requests? Full reasoning, hypotheses (H1–H4)
and limitations are in CONTEXT.md.

**Datasets used** — both are secondary data, produced by someone else and reused here, not
collected first-hand:

| | NYC 311 Service Requests | NOAA daily weather |
|---|---|---|
| Produced by | NYC Open Data (dataset `erm2-nwe9`) | NOAA NCEI, station `USW00094728` (Central Park) |
| What it is | Tabular records, one row per service request (complaint type, location, timestamps, agency, status) | Tabular records, one row per calendar day (TMAX, TMIN, PRCP, SNOW) |
| Format | CSV | CSV |
| How obtained | Socrata SODA API, `$select`/`$where`/`$order` query params (see `notebooks/00_download.ipynb`) | NCEI Access API, `daily-summaries` endpoint, `units=metric` requested explicitly |
| Time window covered | 2025-01-01–2025-02-28 + 2025-07-01–2025-08-31 (winter vs. summer subset, chosen for weather contrast and laptop-sized volume) | 2025-01-01–2025-08-31 (243 calendar days, no gaps) |
| Volume | 603,544 + 619,913 = 1,223,457 rows; raw files ~111.2 MB + ~113.0 MB (≈224 MB combined) | 243 rows; ~9.9 KB |
| How often it changes | Static once downloaded — but both source portals revise their *own* copies retroactively (311 records get status/close-date updates after creation; NOAA corrects observations), so this project's snapshot is explicitly dated rather than treated as a moving target | same |

**Derived data produced by this project** (not of independent long-term value the way the two
source datasets are, but listed for completeness): `data/processed/311_clean.csv` (cleaned,
row-level, ~248 MB, regenerable, not distributed — see Version control under §III),
`data/processed/weather_clean.csv` (cleaned, reindexed onto the full calendar), and
`data/processed/analysis_daily.csv` (the two joined at day/category grain, 1,143 rows — this is the
actual analysis-ready table and the one with the most long-term reuse value).

**Other material of long-term value:** none beyond the digital artifacts above — no physical
specimens, software beyond the notebooks themselves, or curriculum materials are produced by this
project.

## III. Data organisation & exchange (internally, during the project)

**Single-person project — no internal exchange partners.** The template's questions about sharing
data among colleagues, who else has access, and how files are exchanged don't apply in the way they
would for a consortium; the organisational discipline below exists so the project would still be
legible to a second person if one joined, and so it's legible to the examiner.

**Naming:** Lowercase, underscores, ISO dates throughout — confirmed in practice, not just planned:
`311_2025-01_2025-02_downloaded_2026-07-12.csv`, `weather_centralpark_2025_downloaded_2026-07-12.csv`,
notebooks numbered `00_download.ipynb` … `05_analysis.ipynb`, figures `fig_00_…png` … `fig_06_…png`
(the two-digit prefix is a global sequential figure count across the project, not tied 1:1 to
notebook number — kept consistent after a Phase 5 renumbering fixed a collision between two
notebooks that had both used `fig_02`/`fig_03`).

**Folder structure:** Matches the tree in ROADMAP.md exactly: `data/{raw,processed}`, `notebooks/`,
`docs/`, `figures/`, `presentation/` (not yet populated — Phase 10), plus `DOWNLOAD_LOG.md` and
`complaint_category_map.csv` under `data/`.

**Version control:** Git, GitHub remote (see Backup, §IV). **Workflow note:** Phases 0–2 were
committed directly to `main`; starting Phase 3, switched to one feature branch per phase
(`phase-N-name`, merged with `--no-ff` into `main` once the phase's notebooks run clean and docs
are updated) — a deliberate correction made partway through, not the original plan. `git log
--oneline --graph` shows both eras honestly rather than being rewritten to look consistent.

Two files are gitignored despite being generated by the notebooks: `data/raw/` (large, and the
point is that it's a frozen, checksummed snapshot rather than something Git needs to diff) and
`data/processed/311_clean.csv` specifically (~248 MB — discovered in practice to exceed GitHub's
100 MB hard per-file limit; it's fully regenerable from the raw files + `04_integrate.ipynb`, so
losing Git history for it costs nothing). The small, actually analysis-ready
`data/processed/weather_clean.csv` and `analysis_daily.csv` are committed normally.

**Consistency/quality during the project:** enforced by the phase structure itself — Phase 3
(`03_quality.ipynb`) checks completeness/consistency/validity/accuracy/timeliness/uniqueness/
integrity/representativeness *before* any cleaning happens (assessing and cleaning are kept as
separate steps on purpose), and Phase 4 (`04_integrate.ipynb`) prints a row count after every
transformation so nothing is silently dropped.

## IV. Data storage and back-up (during the project)

**Storage:** Project folder on laptop (`nyc311-weather/`, structure above). Rule: **files in
`data/raw/` are never edited** — verified concretely on 2026-07-13 by re-computing SHA-256
checksums for all 3 raw files and confirming they still match the values logged in
`DOWNLOAD_LOG.md` on the download date, after 5 phases of downstream work. All cleaning/joining
happens in notebooks and is saved to `data/processed/`. Total footprint is small (well under 1 GB
including the gitignored files) — no dedicated storage budget was needed beyond the laptop's own
disk.

**Backup:** 3-2-1 rule: 3 copies, 2 media, 1 off-site.
1. **Laptop** — this working copy.
2. **Cloud / off-site** — GitHub remote `https://github.com/kets01/nyc311-weather.git`, set up
   2026-07-12 and pushed after every phase since. Covers code, docs, and notebooks — not the raw
   311/weather data (`data/raw/`, gitignored) or the large intermediate `data/processed/311_clean.csv`
   (~248 MB, gitignored — see Version control, §III).
3. **External drive/USB** — still outstanding. Because `data/raw/` and the large processed file are
   excluded from Git, a manual copy of the whole project folder to a USB/external drive is the
   plan to cover them. **Residual risk**, tracked here and in Risks below; to close out before
   Phase 10's final checklist, restore-tested by opening one copied file.

Backup frequency in practice: after every phase (i.e., at least daily during active work), via
`git push`.

## V. Data sharing, standards & metadata (with externals)

**File formats:** CSV (raw and processed data — open, long-lived, no proprietary/versioned-binary
lock-in), Markdown (all docs), Jupyter notebooks (`.ipynb`, to be additionally exported to HTML in
Phase 8 as a rot-proof layer), PNG at 300 dpi (figures), PDF (final presentation — Phase 10, not
yet produced). No domain-specific binary standard (e.g., NetCDF) applies here — both source
datasets are already flat tabular data, so CSV is the natural fit rather than a compromise.

**Tools/software needed to read or use the data:** Python 3.11 + pandas is sufficient for every
file in this project (CSV/Markdown/PNG all also open in any text editor or image viewer without
special software) — see Environment (§VIII) for the pinned dependency list.

**Metadata & documentation produced:** `README.md` (overview, sources, folder guide, at-a-glance
numbers), `CONTEXT.md` (full reasoning: research question, hypotheses, limitations, quality plan,
FAIR), `ROADMAP.md` (execution checklist, kept ticked off phase by phase), three data dictionaries
(311, weather, the joined `analysis_daily` table — the structural/schema-level metadata: column
names, types, units, meanings, missingness behavior), `docs/QUALITY_FINDINGS.md` (all 8 quality
dimensions with numbers), `data/DOWNLOAD_LOG.md` (provenance/snapshot record: URL, date, size, row
count, checksum per file), `data/complaint_category_map.csv` (self-made controlled vocabulary, 180
raw complaint types → 10 categories, 0 unmapped).

**Standards:** No biodiversity-specific standard applies to this domain; the analogous role is
played by **Dublin Core**/**DataCite** fields (title, creator, identifier, license, coverage,
keywords, date) for describing each dataset, and this project's own data dictionaries in place of a
formal domain metadata language. **Not yet done** (Phase 7 of the roadmap): writing one short
DataCite-style descriptive record per dataset explicitly in these terms, and a consistency pass
confirming the same license names/dates/titles are used identically across README, this DMP, and
the dictionaries.

## VI. Data restrictions

**How open:** Fully open — both source datasets are already public with no restriction (see
Licenses, §VII), and every output this project produces or displays is aggregated to
day/borough/category grain, not record-level.

**Personal/sensitive data and GDPR:** No name, contact detail, or other directly-identifying field
appears anywhere in either source dataset. The one indirect risk is that 311's exact coordinates +
ZIP + timestamp, combined, could plausibly re-identify a complainant's home if ever *displayed*
together at that precision — this is not personal data under the GDPR in the form it's stored
(no identified or identifiable living individual is named), but the standing rule adopted here
anyway is: only ever *show* aggregates (day/borough/category), keep record-level location data
local. Because no personal data is processed or published, GDPR consent/anonymization mechanics
(§2.5 of the BiodivERsA guidance) don't apply beyond this precaution.

**Phase 6 privacy check performed on 2026-07-13** — reviewed every artifact this project actually
displays:
- All 7 figures (`figures/fig_00…fig_06`) are aggregate: time series/scatter/heatmap of daily
  counts and weather, a missingness pattern (no values shown), a duration histogram. None plot
  individual coordinates or addresses.
- `docs/311_profiling_report.html` was generated with `minimal=True`; confirmed by inspecting the
  HTML that it has only "Overview" and "Variables" sections — no "Sample"/"Duplicate rows" table
  of raw records, and no individual lat/long values (grepped for coordinate-like numbers; the only
  matches were CSS layout percentages and internal chart-rendering SVG path coordinates, not data).
- **Found and fixed one real issue:** `docs/data_dictionary_311.md`'s example row had reused one
  real complaint's exact ZIP + 4-decimal-precision latitude/longitude together — precise enough to
  plausibly identify a specific building. Replaced with illustrative rounded values decoupled from
  any single real record (see the dictionary's footnote). This was a documentation-only slip —
  no notebook, saved table, or figure ever displayed or exported record-level coordinates — but
  it's reported here rather than quietly fixed, since catching your own mistake and saying so is
  worth more than claiming a clean check on the first pass.

**Security:** Worth being precise here rather than reciting standard boilerplate: **disk encryption
doesn't actually protect much in this specific project.** Both source datasets are fully public
(see Licenses, §VII) — anyone can re-run the exact API calls in `00_download.ipynb` and get the
same data, no login required. If this laptop were stolen, someone reading `data/raw/` would learn
nothing they couldn't already pull from `data.cityofnewyork.us` or NCEI themselves. So disk
encryption (confirmed on, user-verified 2026-07-13) is general laptop hygiene, not a load-bearing
control for this project's actual privacy risk.

The control that *is* doing real work is the aggregation-before-display rule above: the risk was
never "someone reads my raw CSV" (already public, already legally available to them), it's "I
publish a derived product — a scatter plot, a table — that makes re-identifying a complainant's
home *practically easy* in a way a 1.2-million-row government CSV, technically public but
practically obscure, does not." That distinction is what the Phase 6 privacy check was actually
checking for, and it's the one place a real issue was found and fixed.

Separately, and unrelated to the data's own confidentiality: nothing sensitive (credentials, API
keys) is committed to Git, and `.gitignore` keeps the large raw files out of the repository — for
size and provenance-snapshot reasons (see Version control, §III), not because they needed hiding.

**IP/reuse restrictions:** none — see Licenses (§VII); no embargo is planned.

## VII. Data publishing & licensing

**Inbound, verified precisely rather than described loosely:**
- **NYC 311:** not a conventional license — a legal mandate under **Local Law 11 of 2012** (NYC
  Administrative Code § 23-502(d)), which requires the city to publish datasets "without
  restriction or licensing requirements": no registration, no license, no usage restriction.
  Practically equivalent to public domain — no attribution legally required.
- **NOAA weather:** US federal government works aren't copyrightable domestically
  (17 U.S.C. § 105) and are automatically public domain; NCEI's own stated policy formally applies
  **CC0 1.0 Universal Public Domain Dedication** to its federally-produced holdings.

Both sources are therefore **effectively CC0-equivalent** — no share-alike, no required
attribution, no restriction on relicensing derived work however I choose.

**Outbound:** made concrete in this repo, not just planned — a root-level `LICENSE` file (MIT) now
covers the code (notebooks, scripts); documentation and the derived tables in `data/processed/`
are declared CC BY 4.0 (noted in `LICENSE` and here, since GitHub has no clean second-license
mechanism for a mixed repo). Because the inbound sources impose no constraint, choosing
attribution-required CC BY 4.0 over CC0 for my own outputs is a scholarly-norm choice, not a legal
necessity — worth being explicit about, since it would be easy to (wrongly) imply the inbound
licenses required it. The original source data keeps its own inbound status regardless of how the
derived tables are licensed.

**Where and how (described, not yet executed):** would deposit on **Zenodo**: free, gives a DOI,
keeps metadata even if a record is retracted, integrates with GitHub. What would be deposited: the
cleaned/joined data (`data/processed/`, excluding nothing since it's already aggregated to
day/category — no record-level location data in scope), all notebooks, and the documentation set
(dictionaries, quality findings, provenance). Licensed CC BY 4.0 (data/docs) / MIT (code), matching
the licenses already declared in this repo rather than invented fresh at deposit time. Metadata via
the Zenodo form (DataCite fields): title, authors, description, keywords, related identifiers
pointing back to the two source datasets (`erm2-nwe9`, station `USW00094728`). No embargo planned —
data would be made available as soon as the exam materials are finalized. No journal
data-availability requirement applies (this is a course exam, not a journal submission).

## VIII. Data archiving (after the project ends)

**Target:** keep everything ≥ 10 years (DFG good-scientific-practice guideline), in open formats
(CSV, Markdown, PNG) with fixity checksums. Currently have: SHA-256 checksums for the 3 raw files
in `DOWNLOAD_LOG.md`, re-verified unchanged as of this phase. Still to do (Phase 8): export all
notebooks to HTML — the plan is for the work to stay *interpretable* even once the pinned
environment eventually stops being *runnable*. DOI/long-term repository placement is the Zenodo
deposit described in §VII, not yet executed.

**Environment, so the data stays usable, not just stored:** `requirements.txt` pinned via `pip
freeze` (135 packages); Python 3.11.9 noted in `README.md`; every notebook's first cell prints
`sys.version` and `pd.__version__` (self-documenting provenance, confirmed present in all 6
notebooks). **Fresh-install tested on 2026-07-13:** created a new venv from scratch, ran `pip
install -r requirements.txt` with no errors, and confirmed every project dependency (pandas,
matplotlib, seaborn, missingno, ydata-profiling, holidays, jupyter_core, requests, scipy) imports
cleanly. Honest limit, stated up front rather than discovered later: no environment is guaranteed
to keep working over a 10-year horizon — pinned versions cover the medium term, Docker would extend
it further (not done here), and the HTML export planned for Phase 8 is what actually carries the
10-year requirement, independent of whether the code still runs.

**Software/tools needed for reuse and whether they'll be archived:** just Python + the packages in
`requirements.txt` (already versioned in Git, so archived alongside the data by construction) — no
bespoke or unarchived tooling is required to open or rerun this project.

## IX. Costs

Effectively zero marginal cost, stated explicitly rather than left implicit:
- **Data acquisition:** both APIs (Socrata SODA, NOAA NCEI Access) are free, no key/token, no rate
  payment required at this project's volume.
- **Storage during the project:** laptop disk already owned; no cloud storage budget needed (total
  footprint well under 1 GB including gitignored files).
- **Version control / backup:** GitHub free tier (public repo, no per-seat or storage charge at
  this scale).
- **Long-term archiving:** Zenodo is free for deposits under its size limit (50 GB/dataset), which
  this project is nowhere near; a DOI is issued at no cost.
- **Software:** entirely open-source (Python, pandas, Jupyter, etc.) — no licensing fees.

No budget line was needed or requested for this project; if it were extended into a funded project,
the main future cost to plan for would be Zenodo storage beyond the free tier if raw (not just
aggregated) data were ever deposited, and possibly paid long-term institutional repository storage
if requirements grew beyond what Zenodo's free tier and this project's DFG-10-year target need.

## Risks

Not one of the template's numbered sections, but kept as this project has always tracked it and the
content doesn't fit cleanly under Costs or Archiving alone:

- **Laptop dies:** mitigated by the GitHub remote (code/docs/notebooks); **not yet mitigated** for
  the raw data snapshot, which only exists on this laptop until the USB backup (see §IV) is
  actually done — the single clearest open risk in this plan.
- **Source portal changes data:** mitigated — raw snapshot is frozen, checksummed, and dated;
  "data as of 2026-07-12" is stated wherever the data is used.
- **Time runs out:** the exam sheet's own escape valve — analysis (Phase 5) was kept to a hard
  time limit and 4 figures by design, specifically so that Phases 3/6/8 (quality, DMP, FAIR/
  provenance) would not be the ones cut if time got tight.
