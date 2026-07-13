# CONTEXT.md — Project Reference (Student Edition)

**Project:** How do weather conditions influence NYC 311 service requests? (2025 subset)
**Exam:** Management of Scientific Data — oral, ~30 min, presentation as PDF, DMP included in the slides.

**How this project works (the simple version):**
- Data is downloaded **via the sources' APIs, directly from a notebook** (`00_download.ipynb`): the query URL is code, so the acquisition itself is reproducible. A small download log records what was fetched and when.
- Everything happens in **Jupyter notebooks** with pandas.
- Publication is **not done for real** — I describe *how I would* publish (Zenodo, DOI) and show that I understand it.
- During the exam I can **screen-share** my notebooks, my profiling report, and my Git history as evidence.

---

## 1. Project Overview

**The idea:** take the official exam dataset (NYC 311 Service Requests, scenario 2), add one extra dataset (daily weather for NYC from NOAA), join them by date, and walk through the whole data lifecycle: plan → download → check quality → describe → integrate → small analysis → provenance → preservation/FAIR → present.

**Why this research question works:**
- The exam says originality doesn't matter — it just has to be reasonable. "Does weather affect complaints?" is intuitive (heat complaints in winter, flooding after rain, noise in summer).
- It *requires* joining a second dataset, which the exam explicitly encourages.
- The 311 data is messy in interesting ways (missing values, duplicates, weird categories) — perfect for the quality-control part.
- The analysis can stay small (a few plots + correlations), which matches the exam instruction that **analysis is NOT the focus**.

**Why weather data strengthens the project:** it lets me talk about real integration problems — different schemas, different time resolutions (events vs. daily values), units, missing days, and "one weather station for a whole city". Also, NOAA is a curated scientific source while 311 is citizen-reported — a nice contrast for the quality discussion.

---

## 2. Research Question

**Primary question:** How do weather conditions (temperature, precipitation, snow) influence the daily number and category mix of NYC 311 service requests in 2025?

**Objectives:**
1. Get a manageable 2025 subset of 311 data + matching daily weather data.
2. Assess data quality of both and document the issues.
3. Join them by date and validate the join.
4. Show the relationship with a few plots and correlations.
5. Document everything (DMP, metadata, provenance, FAIR).

**Hypotheses (simple and defensible):**
- **H1:** More rain → more flooding/sewer complaints.
- **H2:** Colder days → more "Heat/Hot Water" complaints (NYC law: landlords must heat when it's below 55 °F outside — nice fact to mention).
- **H3:** Snowfall → more snow/ice complaints.
- **H4:** Warm days → more outdoor noise complaints.

**Limitations (say these proactively — it earns points):**
1. **Correlation ≠ causation.** Season is a confounder: heat complaints correlate with cold *and* with "it's January".
2. **One weather station** (Central Park) stands in for the whole city.
3. 311 measures *reports*, not actual incidents (reporting bias).
4. Daily aggregation hides what happens within a day.

**Assumptions:** 311 timestamps are NYC local time; Central Park weather is a reasonable citywide proxy; daily resolution is fine for this question.

---

## 3. Dataset Documentation

### Dataset A — NYC 311 Service Requests
| Aspect | Details |
|---|---|
| Source | NYC Open Data portal, dataset "311 Service Requests from 2010 to Present" (ID: `erm2-nwe9`) |
| Publisher | City of New York (NYC Open Data / NYC 311) |
| License | Local Law 11 of 2012 (NYC Admin Code § 23-502(d)) — mandates publication without restriction, registration, or license; effectively public-domain-equivalent, no attribution legally required |
| Format | CSV via the **Socrata SODA API** (the portal's programmatic interface; no key needed for this dataset) |
| How I get it | One URL per time window, called from `00_download.ipynb` with `pd.read_csv(url)`: `https://data.cityofnewyork.us/resource/erm2-nwe9.csv?$where=created_date between '2025-01-01T00:00:00' and '2025-02-28T23:59:59'&$limit=1000000&$order=created_date` — the filter runs on NYC's servers, so I only download my subset. I save the result to `data/raw/` and log URL + date + row count. |
| Size | Full dataset ~40M rows — that's why I only take a **subset** (e.g., a few 2025 months with contrasting weather, like Jan–Feb + Jul–Aug). The exam sheet explicitly allows subsets. |
| Update frequency | Daily |
| Key columns | `Unique Key` (ID), `Created Date`, `Closed Date`, `Complaint Type`, `Descriptor`, `Agency`, `Borough`, `Incident Zip`, `Latitude`/`Longitude`, `Status` |
| Known issues | Missing ZIPs/coordinates, "Unspecified" borough, `Closed Date` sometimes before `Created Date`, 200+ inconsistent complaint types, possible duplicates |
| Pros | Official exam dataset, authoritative, rich, free |
| Cons | Citizen-reported (bias), messy categories, big |

### Dataset B — NOAA daily weather (Central Park)
| Aspect | Details |
|---|---|
| Source | NOAA **NCEI Access API** (no token needed), station **NY City Central Park (USW00094728)** — one URL fetched from `00_download.ipynb`: `https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&stations=USW00094728&startDate=2025-01-01&endDate=2025-08-31&dataTypes=TMAX,TMIN,PRCP,SNOW&units=metric&format=csv` |
| Publisher | NOAA / NCEI (US government) |
| License | Public domain (17 U.S.C. § 105, US government work); NCEI applies CC0 1.0 Universal Public Domain Dedication to its holdings |
| Format | CSV |
| Variables | `TMAX`, `TMIN` (temperature), `PRCP` (precipitation), `SNOW` (snowfall), `DATE` |
| ⚠️ Units trap | GHCN raw data stores tenths of °C/mm; other downloads use Fahrenheit/inches. My API URL requests **`units=metric` explicitly** — a deliberate, documented choice — and I still sanity-check the values (NYC TMAX should be roughly −15…40 °C). Great exam talking point. |
| Known issues | Occasional missing days; values can be corrected retroactively (so I note my download date); one station ≠ whole city |
| Pros | Tiny (365 rows/year), scientific gold standard, public domain |
| Cons | Spatial coverage is a single point |

**Nice contrast for a slide:** 311 = crowdsourced, huge, messy vs. NOAA = instrument-measured, tiny, curated.

---

## 4. Data Integration

**Goal:** one table with one row per **day** (and complaint category):
`date | complaint_category | n_requests | tmax | tmin | prcp | snow | weekday`

**Steps (all in one notebook):**
1. **311:** parse `Created Date` → extract the calendar **date** → clean up `Complaint Type` (trim spaces, unify case) → map the ~200 raw types to ~10 simple categories using a small mapping table I make myself (`complaint_category_map.csv`, e.g. HEAT, NOISE, FLOODING, SNOW_ICE, STREET, SANITATION, PARKING, OTHER) → count requests per day per category.
2. **Weather:** parse `DATE` → check/convert **units** → keep TMAX, TMIN, PRCP, SNOW → make sure there is exactly one row per day; if days are missing, keep them as missing (NaN) and say so.
3. **Join:** LEFT JOIN — 311 daily counts on the left, weather on the right, key = `date`. Left join so a missing weather day doesn't silently delete complaint data.
4. Add `weekday`/`weekend` (complaint volume depends on it).

**Expected problems to mention:**
| Problem | What I do |
|---|---|
| Different column names/types (`Created Date` vs `DATE`) | Rename + convert both to real date types before joining |
| Different time resolution (event timestamps vs daily values) | Aggregate 311 up to days — and say that intra-day info is lost |
| Timezone/DST | 311 is local NYC time; at *daily* resolution the effect is tiny, but I mention it |
| Missing weather days | Stay visible as NaN; report how many |
| Units | Verified with plausibility checks (see §5 Validity) |
| 200+ complaint types | My mapping table = a self-made **controlled vocabulary** (good keyword!) |

**Validation after joining (never skip):**
- Row count after join == row count of the daily 311 table (left join must not add/lose rows).
- Sum of `n_requests` == number of cleaned 311 events.
- % of days with complete weather → report it.
- Spot check: pick 1–2 days with known extreme weather in my window and check both sides look right.

---

## 5. Data Quality

For each dimension: what it means → how I check it (pandas one-liners) → what I expect → what I do about it.

| Dimension | Meaning | How I check (tools) | Expected findings | Handling |
|---|---|---|---|---|
| **Completeness** | Are values present? | `df.isna().mean()`; count placeholders like "Unspecified", "N/A", ZIP "00000" (they count as missing!); `missingno.matrix(df)`; check weather for missing days | ~5–10% missing geo fields; missing `Closed Date` for open cases (that's legitimate!) | Report rates; don't invent values; distinguish "legitimately empty" from "defect" |
| **Consistency** | No contradictions | Compare `Agency` vs `Agency Name`; borough spellings; value formats | Casing/whitespace variants; borough "Unspecified" although coordinates exist | Normalize text; use my mapping table |
| **Validity** | Values follow format/range rules | ZIP matches 5 digits; lat/lon inside NYC box (lat 40.4–41.0, lon −74.3…−73.6); TMAX in −30…45 °C; PRCP ≥ 0; dates inside my window | Some malformed ZIPs, a few (0,0) coordinates | Flag or exclude with a counted reason — never silently |
| **Accuracy** | Values match reality | Hard without ground truth → plausibility: spot-check 2–3 extreme weather days against news/weather websites | Mostly fine; complaint categories may be misassigned by call-takers | Disclose; aggregate to daily level reduces impact |
| **Timeliness** | Recent/current enough | Note the portal's "last updated"; my download date; distribution of `Closed Date − Created Date` | Recent records may still change; NOAA corrects values later | State "data as of <download date>" everywhere |
| **Uniqueness** | No duplicates | `df['Unique Key'].duplicated().sum()`; heuristic for "same day + same type + same location" | Exact duplicates rare; *semantic* duplicates (10 neighbors report one outage) common | Remove exact dupes; keep semantic ones **on purpose** — my unit of analysis is *reports*, and I say so (strong answer!) |
| **Integrity** | Logical rules hold | Count rows with `Closed Date < Created Date`; check every complaint type is in my mapping table | A small % of negative durations (known 311 quirk) | Count, exclude from duration logic only, document |
| **Representativeness** | Data reflects the real world population | Complaints per borough vs borough population; "one station for the whole city" | Reporting differs by neighborhood; coastal weather differs from Central Park | Can't be fixed — must be *disclosed*; talk about "reports", never "incidents" |

**Tools (all screen-shareable in the exam):**
- **pandas** — all checks above
- **ydata-profiling** — one command → full HTML report (missing values, distributions, duplicates). Very impressive to show.
- **missingno** — one-picture missing-data overview
- *(Optional stretch goal, only if time permits: mention that frameworks like Great Expectations turn such checks into automated test suites — knowing it exists is enough.)*

---

## 6. Data Management Plan (goes INTO the presentation — no separate document needed)

| DMP topic | My concrete answer |
|---|---|
| **Roles** | I'm a one-person project, but I name the hats: researcher, data steward (quality/metadata), archivist (backups). In a team these would be separate people. |
| **Data collection** | **API download from a notebook** (`00_download.ipynb`): Socrata SODA API for 311 (server-side date filter), NCEI Access API for weather (`units=metric` explicit). The query URLs live in versioned code → the acquisition itself is reproducible. Each fetch is additionally recorded in `data/DOWNLOAD_LOG.md`: full URL, date, file size, row count (the log matters because both sources revise data — my snapshot is tied to a date). |
| **Storage** | Project folder on my laptop. **Rule: files in `data/raw/` are never edited** — all changes happen in notebooks and are saved to `data/processed/`. |
| **Backup** | 3-2-1 rule: laptop + external drive/USB + cloud (e.g., university cloud). I actually copy the folder at each milestone and test once that I can open a restored file. |
| **Naming** | lowercase, underscores, ISO dates: `311_raw_jan-feb_downloaded_2026-07-15.csv`; notebooks numbered `01_…` to `05_…`. |
| **Folder structure** | See ROADMAP.md — small and fixed: data/raw, data/processed, notebooks, docs, figures, presentation. |
| **Version control** | Git for notebooks, docs, small tables (not for the big raw CSV — listed in `.gitignore`). Commit after every work session with a meaningful message. |
| **File formats** | CSV (open, long-lived) for data; Markdown for docs; PNG for figures; PDF for the presentation. |
| **Documentation & metadata** | README + data dictionary + this file; see §7. |
| **Licenses** | Inbound: 311 under Local Law 11 of 2012, weather under 17 U.S.C. §105/CC0 — both effectively CC0-equivalent, no attribution required. Outbound (if I published): code MIT, data/docs CC BY 4.0 — my own choice, not one the inbound licenses force. |
| **Ethics & privacy** | No names in 311, but exact coordinates + time could identify a complainant's home → I only ever *show* daily/borough/category aggregates; record-level location data stays local. This is the control that actually matters (see Security). |
| **Security** | Laptop disk encryption; nothing sensitive in Git. Honest caveat: since both sources are already public data, encryption isn't protecting a secret here — it's general hygiene, not the thing standing between the data and misuse. The real control is the aggregation-before-display rule above. |
| **Preservation** | Keep everything ≥ 10 years (German good-scientific-practice rule — DFG) in open formats with checksums. |
| **Environment (long-term)** | Pinned `requirements.txt` (`pip freeze`) + Python version in the README + versions printed in each notebook's first cell; fresh-install tested. Honest limit: every environment eventually decays — so notebooks are additionally exported to HTML and data kept in CSV, keeping the work *interpretable* even when no longer *runnable*. (Stronger option to name: Docker containers.) |
| **Publication (described, not executed)** | I *would* deposit the cleaned data + notebooks + docs on **Zenodo**: free, gives a **DOI**, keeps metadata even if a record is retracted, integrates with GitHub. I show the plan (and maybe the filled-out form as a screenshot) instead of a real deposit. |
| **Risks** | Laptop dies → backups; portal changes data → I keep my raw snapshot + download date; time runs out → analysis is the part I cut (exam says it's not the focus). |

---

## 7. Metadata

Four kinds, and what each is **concretely** in my project:

| Type | Question | My artifact | Standard to name |
|---|---|---|---|
| **Descriptive** | What is it, who made it, what's it about? | A short record per dataset (title, publisher, license, time range, keywords) in the README/docs | **Dublin Core**; **DataCite** (what Zenodo uses for DOIs) |
| **Structural** | How is it built? | **Data dictionary**: one row per column — name, type, unit, meaning, allowed values, example | Just a well-made CSV/table (mention CSVW exists) |
| **Administrative** | How is it managed? | License, formats, file sizes, contact, download dates | (part of DataCite/Dublin Core fields) |
| **Provenance** | Where from, what happened to it? | Download log + processing steps in notebooks (see §8) | **W3C PROV** (concept level) |

Key sentence for the exam: *"Metadata is for humans AND machines — that's why standards and controlled vocabularies (ISO dates, fixed category lists) matter."*

---

## 8. Provenance

**What I record, and how — kept simple:**

| Stage | What I write down | Where |
|---|---|---|
| Download | The exact API query URLs (they ARE the filters) live in `00_download.ipynb` (versioned in Git); plus download date, file size, row count | `00_download.ipynb` + `data/DOWNLOAD_LOG.md` |
| Processing | Every cleaning/join step with row counts before/after — visible as notebook cells in order | The numbered notebooks themselves |
| Environment | Package versions (`pip freeze > requirements.txt`; print `pd.__version__` in notebooks) | `requirements.txt` |
| Figures | Which notebook produced which figure | Figure filenames match notebook numbers |

**How Git contributes:** the commit history shows who changed what, when, and why — for notebooks, docs, and my mapping table. I can show `git log` live in the exam.
**How Jupyter contributes:** a notebook is a lab journal — code, parameters, and results in execution order. My discipline rule: **"Restart & Run All" before committing**, so outputs are never stale.
**Concept to name:** W3C PROV — data files are *entities*, notebook steps are *activities*, I am the *agent*. One tiny diagram "from portal to plot" for a single figure makes a great slide.
**Honest limit to mention:** Git doesn't version my big raw CSV — that's covered by the download log + keeping the raw file untouched.

---

## 9. FAIR Principles

Key opening line: **FAIR ≠ open.** FAIR is about making data findable and reusable by humans *and machines*. Assessed for *my* project, with the honest status:

| Principle | What it demands | My status now | What I would do (publication plan) |
|---|---|---|---|
| **Findable** | Persistent identifier + rich metadata + indexed | Sources are findable (portal ID, station ID). *My* results only live on my laptop → not findable | Zenodo deposit → **DOI**, rich metadata, indexed in search engines |
| **Accessible** | Retrievable via a standard open protocol; metadata survives even if data is removed | Sources: yes (HTTPS). Mine: no | Zenodo = HTTPS access; even if withdrawn, the metadata record stays (**that's A2** — classic exam question!) |
| **Interoperable** | Open formats, shared vocabularies, links to related data | CSV, ISO dates, standard coordinates ✓; my complaint categories are a homemade vocabulary — weak spot | Publish the mapping table + data dictionary with the data; metadata links back to the two sources ("derived from erm2-nwe9 / station USW00094728") |
| **Reusable** | Clear license, provenance, community conventions | Inbound licenses fine; provenance exists (§8) | Explicit CC BY 4.0 / MIT; README + data dictionary = community convention |

**How to demonstrate in the exam:** show this table as a slide (traffic-light colors), openly name the gaps — an honest partial-FAIR assessment is far more credible than "everything is green".

---

## 10. Analysis Plan (deliberately small!)

> The exam sheet literally says analysis is **not** the focus of MoSD. Budget: an afternoon. If time gets tight, this is what gets cut.

1. **Explore:** requests per day over time; top complaint categories; weekday effect.
2. **Figures (4 max):**
   - Daily total requests + temperature over time (two lines)
   - Heat complaints vs. TMIN (scatter) — should show H2 nicely
   - Flooding complaints vs. precipitation (scatter)
   - Correlation heatmap: categories × weather variables
3. **Statistics:** **Spearman** correlation (robust, no linearity assumption — a one-sentence justification that sounds great).
4. **Interpretation rules:** only say "is associated with", never "causes"; mention the seasonality confounder; optional bonus: compute the heat-complaint correlation *within winter months only* to show I thought about it.

**Explicitly NOT doing (say it proudly):** machine learning, forecasting, causal analysis — out of scope by exam design.

---

## 11. Presentation Strategy

**Structure (~15–18 slides):** Title & question (1) → lifecycle overview = agenda (1) → datasets & why (2) → **DMP (3–4 slides — it must be in the deck!)** → quality: findings with NUMBERS + tool screenshots (3–4) → integration & validation (2) → analysis figures (2) → provenance (1–2) → preservation/publication plan + FAIR table (2) → limitations & lessons learned (1). Plus a few backup slides (data dictionary, mapping table, extra findings).

**Screen-share moments (prepare 2–3, each ≤ 90 s, with screenshot fallbacks in backup slides):**
1. The **ydata-profiling HTML report** — scroll through missing values/duplicates.
2. **`00_download.ipynb`** — "this one URL is my entire, reproducible acquisition."
3. The **join + validation cells** in the integration notebook, or **`git log`** — provenance in action.

**How to impress:** numbers, not adjectives ("2.1% missing coordinates", not "some missing data"); show artifacts, not claims; defend decisions with the pattern *decision → alternatives → why → limitation*; a candid limitations slide.

**Common mistakes to avoid:** too much analysis; FAIR as empty buzzwords; generic DMP; claiming causality; unreadable slides; no time check; untested tech.

**Likely questions & strong answers:**
| Question | Strong answer (short) |
|---|---|
| "Is your data FAIR?" | "FAIR ≠ open. Currently partially: interoperable formats and provenance yes, but no persistent identifier — that's exactly what my Zenodo plan would fix: DOI, DataCite metadata, and A2 metadata persistence." |
| "How did you handle duplicates?" | "Exact ID duplicates: removed and counted. Semantic duplicates (many reports, one incident) I kept deliberately — my unit is *reports* — and documented the decision." |
| "What if the portal changes the data?" | "My raw snapshot with download date is frozen and backed up; I state 'data as of …' everywhere." |
| "Rain causes complaints, then?" | "It's an association; for flooding a mechanism is plausible, but season confounds most pairs — I checked heat complaints within winter only." |
| "Why did you use the APIs?" | "Three reasons: the query is code, so acquisition is reproducible; filtering happens server-side, so I only download my subset; and the parameters are explicit — e.g., I request `units=metric` from NOAA instead of guessing units later. I still keep a dated download log, because both sources revise data retroactively — the code reproduces the *query*, the log pins down the *snapshot*." |
| "Would re-running your download give identical data?" | "Not necessarily — 311 records get updated and NOAA corrects values retroactively. That's exactly why I froze my raw files, logged the download date, and state 'data as of <date>' everywhere. Query-reproducibility and snapshot-fixity are two different guarantees, and I provide both." |
| "Will this still run in 10 years?" | "Honestly: no one can guarantee that. I pin exact package and Python versions and tested a fresh install — that covers the medium term; Docker would extend it. But since every environment eventually decays, my preservation doesn't depend on executability alone: open CSV data, notebooks exported to HTML, and full documentation keep the work *interpretable* even if no longer *runnable* — that's what the 10-year retention requirement actually needs." |
| "Why Zenodo?" | "Free, DOI, versioning, metadata persists even if data is withdrawn, GitHub integration — unlike GitHub alone, which has no PID and no preservation guarantee." |
| "Personal data in 311?" | "No names, but coordinates+time can re-identify homes — so everything I show or would publish is aggregated to day/borough/category." |

---

## 12. Glossary (learn these — they're free points)

| Term | One-liner |
|---|---|
| **Data lifecycle** | Plan → collect → assure quality → describe → analyze → preserve → share → reuse. |
| **DMP** | Document that says how data is handled during and after a project (storage, backup, docs, licenses, preservation, sharing). |
| **FAIR** | Findable, Accessible, Interoperable, Reusable (Wilkinson et al. 2016). Not the same as "open". |
| **Metadata** | Data about data: descriptive, structural, administrative, provenance. |
| **Data dictionary** | Table describing every column: name, type, unit, meaning, allowed values. |
| **Provenance** | Documented origin + processing history. Standard concept: W3C PROV (entity/activity/agent). |
| **DOI / PID** | Persistent identifier that keeps resolving long-term (DOIs for data/papers, ORCID for people). |
| **Repository** | Service for preserving and sharing research data (Zenodo, institutional repositories). |
| **Checksum** | Hash (e.g., SHA-256) proving a file hasn't changed (= "fixity"). |
| **Controlled vocabulary** | Fixed list of allowed values (my category mapping table is one!). |
| **Tidy data** | One row = one observation, one column = one variable. |
| **Quality dimensions** | Completeness, consistency, validity, accuracy, timeliness, uniqueness, integrity (+ representativeness). |
| **3-2-1 backup** | 3 copies, 2 media, 1 off-site. |
| **Reproducibility** | Same data + same code → same result (helped by requirements.txt, run-all notebooks, download log). |
| **License (CC BY 4.0 / MIT / public domain)** | Reuse terms for data / code / government works. |
| **Aggregation (privacy)** | Coarsening data (per day/borough) so individuals can't be identified. |
| **DFG 10-year rule** | German good-scientific-practice guideline: keep research data ≥ 10 years. |

---

*Execution steps: see ROADMAP.md.*
