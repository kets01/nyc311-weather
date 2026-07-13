# Provenance & FAIR Self-Assessment

> Filled in during Phase 8, 2026-07-13. See CONTEXT.md §8–9 for the original plan this replaces —
> as elsewhere in this project, this document states what was *actually done and verified*, not
> what was intended.

## Provenance

| Stage | What was recorded | Where |
|---|---|---|
| Download | The exact API query URLs (Socrata SODA `$select`/`$where`/`$order`; NCEI Access `dataset=daily-summaries&units=metric`) — they *are* the filters, and they're versioned code, not a one-off manual step. Plus, per file: download date, file size, row count, SHA-256 checksum. | `notebooks/00_download.ipynb` (queries) + `data/DOWNLOAD_LOG.md` (dated snapshot record) |
| Processing | Every cleaning/join step with row counts printed before/after ("provenance by print statement" — nothing dropped silently). Assessment (Phase 3) is kept as a separate step from cleaning (Phase 4) on purpose, so "what's wrong with the data" and "what I did about it" don't get conflated. | `notebooks/03_quality.ipynb` (assessment only, no fixes) → `notebooks/04_integrate.ipynb` (cleaning + join, with validation cells) |
| Environment | Package versions pinned (`pip freeze`); Python version + pandas version self-printed in every notebook's first cell, so a notebook carries its own environment fingerprint even in isolation. | `requirements.txt` + first cell of all 6 notebooks |
| Figures | Which notebook produced which figure — figure filenames are matched to the notebook that generated them (see table below), not just numbered sequentially by coincidence. | `figures/fig_00…fig_07` ↔ notebooks, mapped explicitly below |

**Figure → notebook mapping** (the two-digit prefix is a global sequential count, not 1:1 with
notebook number — see `docs/DMP.md` §III Naming for why):

| Figure | Produced by |
|---|---|
| `fig_00_weather_overview.png` | `02_explore_weather.ipynb` |
| `fig_01_requests_vs_tmax.png` | `05_analysis.ipynb` |
| `fig_02_heat_vs_tmin.png` | `05_analysis.ipynb` |
| `fig_03_flooding_vs_prcp.png` | `05_analysis.ipynb` |
| `fig_04_correlation_heatmap.png` | `05_analysis.ipynb` |
| `fig_05_missingno_matrix.png` | `03_quality.ipynb` |
| `fig_06_case_duration_hist.png` | `03_quality.ipynb` |
| `fig_07_provenance_chain.png` | a one-off script (`_build_provenance_diagram.py`, deleted after use — same pattern as the notebooks were originally built), **not** a numbered analysis notebook. Honest distinction: this figure documents the *pipeline*, it isn't an output *of* the pipeline, so it doesn't get an entry in the six numbered notebooks. |

**How Git contributes:** the commit history shows who changed what, when, and why, for notebooks,
docs, and the mapping table — one feature branch per phase since Phase 3 (see `docs/DMP.md` §III),
`git log --oneline --graph` shows this honestly rather than being rewritten to look tidier than it
was.

**How Jupyter contributes:** each notebook is a lab journal — code, parameters, and results in
execution order. Discipline rule, and verified rather than just claimed (see Reproducibility test
below): **"Restart & Run All" before committing**, so outputs are never stale relative to the code
that (supposedly) produced them.

**W3C PROV framing** (concept only, not a formal implementation): data files are *entities*,
notebook/script steps are *activities*, and the single *agent* throughout is kemki. The diagram
below traces this chain for the project's central figure:

**Provenance chain diagram** for `figures/fig_01_requests_vs_tmax.png` (the H1 figure — daily
request counts vs. TMAX):

![Provenance chain: NYC Open Data / NOAA portals -> raw CSVs (00_download) -> clean CSVs (04_integrate) -> joined table analysis_daily.csv (04_integrate) -> fig_01_requests_vs_tmax.png (05_analysis)](../figures/fig_07_provenance_chain.png)

**Honest limit:** Git doesn't version the big raw CSVs or `data/processed/311_clean.csv` (~248 MB,
over GitHub's 100 MB per-file limit) — that gap is covered by the download log (dated, checksummed
snapshot) and the rule that `data/raw/` is never edited, not by Git history. See `docs/DMP.md` §III
Version control.

## Reproducibility test (Phase 8.2)

Performed 2026-07-13: **"Restart & Run All"** (`jupyter nbconvert --to notebook --execute
--inplace`) on notebooks `01`–`05`, in numeric order, using the project's own pinned venv
(Python 3.11.9, kernel `python3` registered to `.venv`).

- **`00_download.ipynb` was skipped deliberately**, not by oversight — re-running it would call the
  live APIs and fetch a *new* snapshot, silently invalidating every checksum in
  `data/DOWNLOAD_LOG.md` and contradicting the project's own "raw data is frozen and dated" rule
  (see `docs/DMP.md` §IV). This is one of the two options the roadmap explicitly sanctions for this
  step; re-running against a new filename was the other, not taken because it adds a second raw
  snapshot with no analytical purpose.
- **All five re-executed notebooks (`01`–`05`) ran clean top to bottom, zero errors.** `nbconvert
  --execute` raises and stops on the first cell exception — none did.
- **Verified outputs are deterministic, not just "ran without crashing":** after the re-run,
  `git diff --stat` on `data/processed/` (the two committed processed tables) and `figures/`
  (all PNGs) showed **zero byte differences** — the entire pipeline from frozen raw CSVs to final
  figures reproduces exactly given the same inputs. Only the notebooks' own execution-count/output
  cells and the `ydata-profiling` HTML report changed (expected — the profiling report embeds its
  own generation timestamp).
- **Conclusion:** "could you reproduce this?" now has a tested answer, not just an intended one —
  yes, deterministically, for everything downstream of the frozen raw snapshot; the raw snapshot
  itself is reproducible in *query* (the API URL is code) but not guaranteed identical in *content*,
  since both source portals revise their data retroactively (see `data/DOWNLOAD_LOG.md`'s
  Reproducibility note).

## Preservation export (Phase 8.2b)

All 6 notebooks exported to static HTML, 2026-07-13: `jupyter nbconvert --to html
notebooks/*.ipynb` → `docs/notebooks_html/` (2.6 MB total, well within GitHub's limits). This is the
rot-proof layer named in `docs/DMP.md` §VIII: pinned `requirements.txt` keeps the notebooks
*runnable* for the medium term, but no environment is guaranteed to still install cleanly in 10
years — the HTML export keeps the executed analysis (code + real outputs, not just code) readable
indefinitely, independent of whether Python 3.11 and this exact package set still exist.

## FAIR self-assessment

Key point to lead with: **FAIR ≠ open.** Both source datasets are already open (public, no
restriction), but "open" says nothing about whether data is findable via a persistent identifier,
retrievable by machines, described in a shared vocabulary, or reusable with clear provenance — that
gap is exactly what this table checks. Assessed honestly rather than all-green — an admitted gap is
more credible than a claimed clean sweep (the same principle already applied to the Phase 6 privacy
check in `docs/DMP.md` §VI).

🟢 good · 🟡 partial / planned fix · 🔴 real, currently-unaddressed gap

| Principle | What it demands | Status now | Publication plan |
|---|---|---|---|
| **Findable** | Persistent identifier + rich metadata + indexed in a searchable resource | 🟡 **Sources**: findable via their own portal/station identifiers (`erm2-nwe9`, `USW00094728`), rich metadata exists in `docs/METADATA.md`. **This project's own outputs** (derived table, notebooks): no persistent identifier — only a GitHub URL, findable by link, not indexed anywhere a stranger would search | Zenodo deposit (`docs/DMP.md` §VII) → real DOI, indexed by Zenodo's own search and DataCite; **ROADMAP.md Phase 9.2** currently only has *reserved, sandbox* (temporary, non-resolving) DOIs, explicitly not real ones yet |
| **Accessible** | Retrievable via a standard, open protocol; metadata survives even if the data is later removed | 🟢 **Sources**: HTTPS, no authentication, no login. 🟡 **This project's own output**: retrievable via HTTPS (GitHub) today, but if the repo were deleted, the metadata would vanish with it — no independent record | Zenodo = HTTPS access, and critically **A2**: if a Zenodo record is ever withdrawn, the metadata stays resolvable at the DOI — unlike a deleted GitHub repo, where everything disappears at once |
| **Interoperable** | Open, shared formal language for (meta)data; vocabularies that themselves follow FAIR; qualified references to other (meta)data | 🟢 CSV, ISO 8601 dates, standard lat/long — consistent throughout, verified in Phase 3. 🔴 **`data/complaint_category_map.csv` is a homemade vocabulary**, not an external/shared one — flagged here rather than hidden, since it's the clearest weak spot in this whole assessment | Publishing the mapping table + data dictionaries *alongside* the data narrows the gap (a reader can see exactly how the vocabulary was built) but doesn't close it — a homemade vocabulary stays homemade even once published; a real fix would mean mapping onto an existing municipal-311 taxonomy if one existed |
| **Reusable** | Clear, accessible usage license; detailed provenance; meets domain-relevant community standards | 🟢 Licenses precisely cited, not just named (`docs/DMP.md` §VII: Local Law 11 / CC0 inbound, MIT / CC BY 4.0 outbound). 🟢 Provenance now detailed (this document + `data/DOWNLOAD_LOG.md`). 🟡 "Community standards" is a weak fit — there's no single established cross-domain standard for a municipal-311 + climate combination; CSV + explicit data dictionaries are the closest practical equivalent, not a formal one | Same licenses carried into the Zenodo record; `docs/METADATA.md`'s DataCite-style records + the mapping table give a future reuser everything a formal standard would, just not badged as one |

**How this would be shown in the exam:** this table as a slide, traffic-light colors kept, gaps
named out loud (temporary DOI only, homemade vocabulary, no formal community standard) rather than
smoothed over — an honest partial-FAIR assessment is the credible version of this slide, not the
all-green one.
