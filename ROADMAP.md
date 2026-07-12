# ROADMAP.md — Step-by-Step Plan (Student Edition)

Work top to bottom, tick the boxes. Each task has: **Goal · What to do · Why · Deliverable · Time · Watch out**.
Total: roughly **30–35 hours over 2–3 weeks**. Keep the last 3–4 days for the presentation and rehearsing.

> ⚠️ **Golden rule from the exam sheet:** analysis is NOT the focus. If time gets tight, cut Phase 5 — never Phases 3, 6, or 8.

---

## Project folder (create once in Phase 0 — this is all you need)

```
nyc311-weather/
├── README.md                     # what, why, how to run
├── requirements.txt              # pinned packages (pip freeze)
├── .gitignore                    # ignores data/raw/ and checkpoints
├── data/
│   ├── raw/                      # downloaded files — NEVER edit these
│   ├── processed/                # cleaned/joined tables saved by notebooks
│   ├── DOWNLOAD_LOG.md           # per file: URL, filters, date, size, rows
│   └── complaint_category_map.csv
├── notebooks/
│   ├── 00_download.ipynb         # API acquisition: query URLs + save to data/raw
│   ├── 01_explore_311.ipynb
│   ├── 02_explore_weather.ipynb
│   ├── 03_quality.ipynb
│   ├── 04_integrate.ipynb
│   └── 05_analysis.ipynb
├── docs/
│   ├── DMP.md                    # full DMP text → distilled into slides
│   ├── QUALITY_FINDINGS.md       # findings with numbers
│   ├── data_dictionary_311.md
│   ├── data_dictionary_weather.md
│   └── FAIR_and_provenance.md
├── figures/                      # exported plots (fig_01_....png)
└── presentation/                 # slides source + final PDF
```

---

# PHASE 0 — Setup (½ day)

- [x] **0.1 Create the folder structure** exactly as above. *Why:* every file gets one obvious home. *Deliverable:* the tree. *Time:* 10 min.
- [x] **0.2 Git init.** `git init`, create `.gitignore` containing `data/raw/`, `.ipynb_checkpoints/`, `__pycache__/`; first commit. Optional: private GitHub repo as extra backup. *Why:* version history = provenance of your work; you can show `git log` in the exam. *Time:* 15 min. *Watch out:* never commit the big raw CSV.
- [x] **0.3 Python environment.** Create a venv (or conda env), then `pip install pandas jupyter matplotlib seaborn missingno ydata-profiling holidays` and `pip freeze > requirements.txt`; also note your **Python version** (`python --version`) in the README — requirements.txt doesn't capture it, and it matters just as much. Commit. *Why:* pinned versions + Python version = your environment spec; environments are the most fragile part of long-term reproducibility. *Time:* 20 min.
- [x] **0.4 Start README.** Title, research question, data sources with links + licenses, folder guide. *Why:* first thing anyone (including the examiner) reads. *Time:* 20 min.
- [ ] **0.5 Set up backup.** Decide your 3 copies: laptop + USB/external drive + cloud folder. Copy the project once now; open one file from the copy to prove restore works. Note this in `docs/DMP.md`. *Why:* the DMP backup section must describe something real. *Time:* 20 min. **Status: 2/3 done** — laptop + GitHub remote (`github.com/kets01/nyc311-weather`) are live; USB/external-drive copy still outstanding (see `docs/DMP.md`).
- [x] **0.6 Create doc stubs.** Empty `DMP.md`, `QUALITY_FINDINGS.md`, `FAIR_and_provenance.md` with headings copied from CONTEXT.md. *Why:* you'll fill them phase by phase instead of the night before. *Time:* 15 min.

---

# PHASE 1 — Download the data via the APIs (½ day)

- [x] **1.1 Choose your subset and write it down.** Recommended: **Jan–Feb 2025 + Jul–Aug 2025** (winter vs. summer = weather contrast, and small enough for a laptop). Write one sentence in the README: "I chose … because …". *Why:* subsets are allowed, but must be deliberate. *Time:* 10 min.
- [x] **1.2 Create `00_download.ipynb` and fetch the 311 data (Socrata SODA API).** No key needed. One cell per time window — the whole download is:
  ```python
  import pandas as pd, urllib.parse
  where = "created_date between '2025-01-01T00:00:00' and '2025-02-28T23:59:59'"
  url = ("https://data.cityofnewyork.us/resource/erm2-nwe9.csv?"
         f"$where={urllib.parse.quote(where)}&$limit=1000000&$order=created_date")
  df = pd.read_csv(url)
  print(len(df), df['created_date'].min(), df['created_date'].max())
  df.to_csv("../data/raw/311_2025-01_2025-02_downloaded_2026-07-15.csv", index=False)
  ```
  Repeat for the summer window. *Watch out:* **always print the row count and check it's below your `$limit`** — if it equals the limit, the download was truncated and you must raise the limit or split the window. Also verify min/max dates match your window. *Why:* the URL in code = reproducible acquisition; server-side filtering means you only download your subset. *Time:* 45 min.
- [x] **1.3 Fetch the weather data (NOAA NCEI Access API, same notebook).** No token needed:
  ```python
  url = ("https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries"
         "&stations=USW00094728&startDate=2025-01-01&endDate=2025-08-31"
         "&dataTypes=TMAX,TMIN,PRCP,SNOW&units=metric&format=csv")
  wx = pd.read_csv(url)
  print(len(wx), wx['DATE'].min(), wx['DATE'].max())
  wx.to_csv("../data/raw/weather_centralpark_2025_downloaded_2026-07-15.csv", index=False)
  ```
  *Watch out:* keep `units=metric` in the URL — that's your explicit, documented answer to the units trap. Expect ~1 row per day; sanity-check TMAX values look like °C. *Time:* 20 min.
- [x] **1.4 Fill in `data/DOWNLOAD_LOG.md`.** For each file: the full API URL, download date, file size, number of rows. *Why:* the notebook reproduces the *query*; the log pins down the *snapshot* — both sources revise data retroactively, so "data as of <date>" needs a record. *Time:* 10 min.
- [x] **1.5 Freeze the raw data.** SHA-256 checksums recorded in the log; USB backup still pending (see 0.5). Rule: nothing ever edits `data/raw/`. Optional but nice: run `shasum -a 256` (Mac/Linux) or `certutil -hashfile file SHA256` (Windows) on each file and paste the checksums into the download log. Back up now. *Time:* 10 min.

---

# PHASE 2 — Explore & describe (1–1.5 days)

- [x] **2.1 Notebook `01_explore_311.ipynb`.** Habit for THIS and every notebook: first cell prints `sys.version` and `pd.__version__` (self-documenting provenance). Then load the CSV (use `pd.read_csv(..., low_memory=False)`); print shape, date min/max, missing % per column, top 30 complaint types, borough counts, duplicated `Unique Key` count. Run `ydata_profiling.ProfileReport(df.sample(100000))` and save the HTML into `docs/`. *Why:* the profiling report is a show-piece for "what tools do you use?". *Watch out:* compute missing % on the FULL data, not just the sample. *Time:* 2–3 h.
- [x] **2.2 Notebook `02_explore_weather.ipynb`.** Load weather CSV; plot TMAX/TMIN/PRCP/SNOW over time; **sanity-check units** (NYC TMAX ≈ −15…40 °C — if you see 250, it's tenths!); list missing days by comparing against a full calendar (`pd.date_range`). *Time:* 1 h.
- [x] **2.3 Write the data dictionaries.** In `docs/data_dictionary_311.md` (only the ~10 columns you actually use, one line each: name, type, unit, meaning, example, missing-behavior) and same for weather. *Why:* this answers the exam's "How do you describe the dataset?" — it's structural metadata. *Time:* 1 h.
- [x] **2.4 Build the category mapping table.** Create `data/complaint_category_map.csv` with two columns (`raw_type`, `category`): map the top complaint types to ~8–10 groups (HEAT, NOISE, FLOODING, SNOW_ICE, STREET, SANITATION, PARKING, …) and everything else to OTHER. Commit it. *Why:* this is your self-made **controlled vocabulary** — one of the best things you can show. *Watch out:* always keep an OTHER bucket so no rows get lost. *Time:* 1 h.
- [x] **2.5 Commit + update docs** (README data section, first notes in QUALITY_FINDINGS). *Time:* 20 min.

---

# PHASE 3 — Data quality assessment (1.5–2 days) — *core exam content!*

All in **`03_quality.ipynb`**, one section per dimension, every finding as a NUMBER. Then summarize in `docs/QUALITY_FINDINGS.md` as a table: *dimension | finding | number | my decision*.

- [ ] **3.1 Completeness.** `df.isna().mean()`; ALSO count disguised missing values ("Unspecified" borough, ZIP "00000"/"N/A"); `missingno.matrix`; missing weather days count. *Decision:* report, don't invent data; missing `Closed Date` on open cases is legitimate.
- [ ] **3.2 Consistency.** `Agency` vs `Agency Name` cross-tab; borough value list (spelling variants?); whitespace/case in complaint types before vs after normalizing.
- [ ] **3.3 Validity.** ZIP regex `^\d{5}$` pass rate; coordinates inside NYC box (lat 40.4–41.0, lon −74.3…−73.6); dates inside your window; TMAX in −30…45 °C, PRCP ≥ 0.
- [ ] **3.4 Accuracy.** Pick 2–3 extreme weather days in your window, check them against a weather website/news → note agreement. Say why real accuracy is hard without ground truth.
- [ ] **3.5 Timeliness.** Your download date vs portal "last updated"; histogram of `Closed − Created`; note that NOAA corrects values retroactively → "data as of <date>".
- [ ] **3.6 Uniqueness.** Exact duplicate `Unique Key` count; small heuristic for semantic duplicates (same day + type + ZIP, count multi-report incidents). *Decision:* remove exact dupes; keep semantic ones deliberately (unit = reports) — write that decision down.
- [ ] **3.7 Integrity.** Count `Closed Date < Created Date` rows; check every complaint type maps into your table (0 unmapped).
- [ ] **3.8 Representativeness.** Complaints per borough vs borough population (5 numbers from Wikipedia/census, cite them); one sentence on the single-weather-station limitation.
- [ ] **3.9 Write `docs/QUALITY_FINDINGS.md`** with the summary table + 2 screenshots (missingno, profiling report). *Time for the phase:* ~6–8 h total. *Watch out:* don't fix anything in this notebook — assessing and cleaning are separate steps (that separation itself is a good exam point).

---

# PHASE 4 — Clean & integrate (1 day)

All in **`04_integrate.ipynb`**, with a printed row count after every step ("provenance by print statement").

- [ ] **4.1 Clean 311.** Parse dates (`errors='coerce'`, count failures) → drop exact duplicates (count) → normalize complaint type text → merge the mapping table (assert 0 unmapped) → extract `date` column. Save `data/processed/311_clean.csv`. *Watch out:* every dropped row must be counted — no silent deletions.
- [ ] **4.2 Clean weather.** Parse dates; fix/verify units (document the conversion if any); keep TMAX/TMIN/PRCP/SNOW; reindex on the full calendar so missing days are visible NaNs. Save `data/processed/weather_clean.csv`.
- [ ] **4.3 Aggregate + join.** `groupby(['date','category']).size()` → LEFT JOIN weather on `date` → add `weekday`/`is_weekend`. Save `data/processed/analysis_daily.csv`. *Watch out:* aggregate FIRST, then join (otherwise you blow up the table); LEFT (not inner) join so days without weather stay visible.
- [ ] **4.4 Validate the join (don't skip!).** Checks in the notebook: row count unchanged by the join; `n_requests` sum == cleaned event count; % days with complete weather; one spot check on an extreme-weather day. *Why:* "how did you validate the integration?" is a near-certain exam question — you'll have cells to show.
- [ ] **4.5 Data dictionary for the joined table** (add a short section to the docs) + commit + backup. *Time for the phase:* ~5 h.

---

# PHASE 5 — Small analysis (½ day, HARD LIMIT)

All in **`05_analysis.ipynb`**.

- [ ] **5.1 Basics.** Requests per day over time; category totals; weekday effect (one bar chart).
- [ ] **5.2 The 4 figures** (see CONTEXT §10): time series (requests + TMAX), heat-vs-TMIN scatter, flooding-vs-PRCP scatter, Spearman correlation heatmap. Titles, axis labels with units, readable font; save as `figures/fig_01_….png` (300 dpi). *Watch out:* 4 figures max — more analysis costs you exam points elsewhere.
- [ ] **5.3 Interpret in 5 sentences.** One verdict per hypothesis H1–H4, association-language only, seasonality caveat included. Bonus: heat-complaint correlation within winter months only.
- [ ] **5.4 STOP.** Commit, write further ideas into the README under "Future work", and move on. *Time for the phase:* 3–4 h.

---

# PHASE 6 — Finish the DMP (½ day)

- [ ] **6.1 Fill `docs/DMP.md`** using the table in CONTEXT §6 — but replace every plan with what you *actually did* (backup tested on <date>, download log exists, raw untouched, etc.). Publication section stays future tense: "I would deposit on Zenodo because …". *Why:* concrete beats generic; the examiner may ask "show me". *Time:* 2 h.
- [ ] **6.2 Privacy check.** Confirm no figure/table you'll show contains addresses or exact coordinates — everything aggregated to day/borough/category. Note the check in the DMP. *Time:* 15 min.

---

# PHASE 7 — Metadata (2 h)

- [ ] **7.1 Descriptive records.** In the docs (or README): for each dataset a short standard-style record — title, publisher, identifier, license, coverage, keywords, download date. Mention Dublin Core/DataCite as the standards you're following in spirit.
- [ ] **7.2 Consistency pass.** Same license names, dates, and titles everywhere (README, DMP, dictionaries). Contradictions between documents look sloppy.

---

# PHASE 8 — Provenance & FAIR write-up (½ day)

- [ ] **8.1 Fill `docs/FAIR_and_provenance.md` — provenance part.** Table: stage → what was recorded → where (download log / notebooks / requirements.txt / git log). Draw one small "portal → raw CSV → clean CSV → joined table → figure 2" chain diagram (any tool, export PNG) for your best figure. *Time:* 1.5 h.
- [ ] **8.2 Mini reproducibility test.** Restart & Run All on all six notebooks in order (for 00_download, re-running fetches a fresh snapshot — run it against a NEW filename or skip it and note that raw snapshots are frozen by design) — everything must run clean top to bottom. Fix anything that breaks. *Why:* "could you reproduce this?" — now the honest answer is "yes, and I tested it." *Time:* 1 h.
- [ ] **8.2b Export the executed notebooks to HTML.** `jupyter nbconvert --to html notebooks/*.ipynb` → save into `docs/`. *Why:* your rot-proof preservation layer — environments decay, but HTML stays readable in 10+ years; someone in 2040 can *read* your analysis even if they can't *run* it. One command, big exam point. *Time:* 10 min.
- [ ] **8.3 FAIR self-assessment.** Fill the F/A/I/R table from CONTEXT §9 with YOUR status (traffic lights: what's already good, what the Zenodo plan would fix, what stays a gap — e.g., homemade category vocabulary). *Watch out:* don't grade yourself all-green; honest gaps are more credible. *Time:* 1 h.

---

# PHASE 9 — Describe the publication plan (1–2 h, no real deposit)

- [ ] **9.1 Write the plan.** Half a page in the DMP: WHAT would be deposited (cleaned data, notebooks, docs, mapping table — no record-level location data), WHERE (Zenodo — free, DOI, metadata persistence, GitHub integration; alternative: institutional repository), UNDER WHICH licenses (CC BY 4.0 data/docs, MIT code), metadata (DataCite via the Zenodo form).
- [ ] **9.2 Optional 15-min bonus:** open zenodo.org, click "New upload", fill the form fields (don't submit), screenshot it for a backup slide. Shows you've actually seen the process.

---

# PHASE 10 — Presentation (1.5–2 days)

- [ ] **10.1 Outline first.** ~15–18 slides per CONTEXT §11; check that every exam-sheet requirement has a slide: question ▢ DMP ▢ quality+tools ▢ description ▢ analysis ▢ provenance ▢ preservation/publication ▢ FAIR ▢. *Time:* 45 min.
- [ ] **10.2 Build the slides** from your docs — never invent new numbers on slides; copy them from notebooks. Insert the 4 figures, one profiling screenshot, the FAIR table, the provenance chain diagram. Big fonts (≥24 pt). *Time:* 3–4 h.
- [ ] **10.3 Backup slides.** Data dictionary excerpt, mapping table sample, extra quality numbers, Zenodo form screenshot. *Time:* 45 min.
- [ ] **10.4 Prepare the screen-share demos (2–3, each ≤ 90 s).** (a) profiling HTML report, (b) `00_download.ipynb` — one URL = the whole reproducible acquisition (examiners like this), (c) `04_integrate.ipynb` validation cells or `git log`. Practice the exact clicks; put a fallback screenshot of each into the backup slides in case of tech trouble. *Time:* 45 min.
- [ ] **10.5 Export the PDF.** Check fonts/figures at 100% zoom; name it `MoSD_Exam_<LastName>.pdf`; put copies on laptop + USB + cloud; **email it to the examiners in advance** (the exam sheet offers this — do it, it kills the HDMI risk). If you present from your own laptop anyway: get/test the HDMI adapter. *Time:* 45 min.
- [ ] **10.6 Final commit + tag** (`v1.0-exam`) + full backup.

---

# PHASE 11 — Exam prep (2–3 evenings)

- [ ] **11.1 Timed solo rehearsal.** Aim for **18–20 min** talking (leaves room in the ~30-min slot). Adjust slides only where you stumbled.
- [ ] **11.2 Drill the Q&A.** Write 3-sentence answers to every question in CONTEXT §11 plus: "What's in a DMP?", "Difference metadata vs. data dictionary?", "What is FAIR's A2?", "Why Spearman?", "Why did you use the APIs?", "Would re-downloading give identical data?" (answers are in CONTEXT §11!). Practice out loud.
- [ ] **11.3 Rehearsal 2 with a friend** who asks 5 random questions. Freeze the slides afterwards.
- [ ] **11.4 One-page crib sheet.** Your key numbers: row counts, missing %, duplicate counts, top 3 correlations, missing weather days, download dates.
- [ ] **11.5 24 h before: stop changing things.** Run the checklists below, back up, sleep.

---

# Timeline at a glance (adjust to your exam date)

| When | Milestone |
|---|---|
| Day 1 | Phase 0–1 done: setup, data downloaded, log filled |
| Day 3–4 | Phase 2 done: explored, dictionaries, mapping table |
| Day 6–7 | Phase 3 done: quality findings with numbers |
| Day 8–9 | Phase 4 done: joined + validated table |
| Day 10 | Phase 5 done: figures + correlations (frozen) |
| Day 12 | Phases 6–9 done: DMP, metadata, provenance, FAIR, publication plan |
| Day 14 | Phase 10 done: PDF exported and emailed |
| Exam − 1…3 days | Phase 11: two rehearsals, crib sheet, freeze |

**Dependencies in one line:** Setup → Download → Explore → Quality → Integrate → (small) Analysis → then the writing phases (DMP/metadata/provenance/FAIR use facts from the earlier phases) → Presentation → Rehearse.

---

# Final checklists

### Before building slides
- [ ] All notebooks pass "Restart & Run All" (00_download exempt — see 8.2)
- [ ] Raw files untouched; DOWNLOAD_LOG complete (full API URL, date, size, rows); query URLs in 00_download.ipynb committed
- [ ] QUALITY_FINDINGS has a number for all 8 dimensions + a decision each
- [ ] Join validated (counts reconcile, coverage % known, 1 spot check)
- [ ] DMP complete and TRUE (everything in it actually exists)
- [ ] FAIR table filled honestly; provenance chain diagram exists
- [ ] requirements.txt current; git history clean; backup fresh

### Presentation
- [ ] Every exam requirement has a slide (question, DMP, quality+tools, description, analysis, provenance, preservation/FAIR)
- [ ] DMP is IN the deck (exam explicitly requires it — no separate document needed)
- [ ] 15–18 content slides, big fonts, every number matches the notebooks
- [ ] Limitations slide included; backup slides ready
- [ ] 18–20 min timing verified twice; demos rehearsed with screenshot fallbacks
- [ ] PDF on laptop + USB + cloud + emailed to examiners; HDMI adapter if using own laptop

### Things that cost points (final self-audit)
- [ ] Analysis grew too big? → cut it (exam says it's not the focus)
- [ ] Any "causes" instead of "is associated with"? → reword
- [ ] FAIR as buzzwords without your project's specifics? → point to your table
- [ ] Quality claims without numbers or tool names? → add both
- [ ] "Open = FAIR" anywhere? → fix
- [ ] Contradictions between slides / docs / notebooks? → reconcile
- [ ] Record-level addresses/coordinates visible anywhere you present? → remove
- [ ] Exam logistics: appointment confirmed, Room 2084 known, PDF sent, arrive 15 min early?

### Exam day
- [ ] Laptop charged + charger (+ HDMI adapter if needed)
- [ ] PDF: laptop, USB, cloud, examiner inbox ✓
- [ ] Demo tabs open and working offline (profiling HTML, notebook, git log)
- [ ] Crib sheet with key numbers
- [ ] Water, 15 min early, breathe — you've documented everything. 🍀

*All the "why" behind every step: CONTEXT.md.*
