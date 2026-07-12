# Data Quality Findings

> From `notebooks/03_quality.ipynb` (311: 1,223,457 rows combined winter+summer 2025; weather:
> 243 rows, 2025-01-01..2025-08-31). Assessing and cleaning are kept separate: this document only
> records findings, not fixes — cleaning happens in `04_integrate.ipynb`.

## Summary table

| Dimension | Finding | Number | Decision |
|---|---|---|---|
| Completeness | Real NaNs concentrated in `descriptor`, `closed_date`, lat/long, `incident_zip` | descriptor 2.60%, closed_date 1.49%, lat/long 1.34%, incident_zip 0.78% | Report, don't invent values |
| Completeness | Disguised missing: `borough == "Unspecified"` | 811 rows (0.07%) | Treat as missing, not a real borough category |
| Completeness | Missing `closed_date`, broken down by status | 89.7% still-active (legitimate); **10.3% (1,883 rows) are `status == "Closed"` with no `closed_date`** | Flag the 1,883 as a genuine anomaly, not a legitimate gap — not fixed here |
| Completeness | Weather: missing calendar days / missing values | 0 missing days (243/243), 0% missing values in any column | No action needed |
| Consistency | `agency` → `agency_name` mapping | 0 agency codes map to more than one name | Clean; no fix needed |
| Consistency | Borough spelling variants | 0 beyond the `Unspecified` placeholder (already counted under completeness) | No fix needed |
| Consistency | `complaint_type` case/whitespace variants | 0 whitespace issues; 2 case-variant pairs (`Elevator`/`ELEVATOR`, `PLUMBING`/`Plumbing`) | No fix needed — both variants already map to the same category (`BUILDING`) in the controlled vocabulary |
| Validity | ZIP format `^\d{5}$` pass rate | 100.00% (1,213,975/1,213,975 non-null) | No fix needed |
| Validity | Coordinates inside NYC bounding box (lat 40.4–41.0, lon −74.3..−73.6) | 100.00% (1,207,103/1,207,103 non-null) | No fix needed |
| Validity | `created_date` inside requested download windows | 100% (0 rows outside) | Confirms Phase 1 download wasn't truncated/misfiltered |
| Validity | Weather TMAX/TMIN in −30..45 °C, PRCP/SNOW ≥ 0 | 100% pass on all four | No fix needed |
| Accuracy | Weather spot-checks vs external sources (2 of 3 quantitatively confirmed) | see narrative below | Treat NOAA station data as accurate; 311 record-level accuracy disclosed as unverifiable |
| Timeliness | Data snapshot date | 2026-07-12 (both sources) | State "data as of 2026-07-12" throughout |
| Timeliness | Case duration (`closed_date - created_date`), closed cases only | median 8.4 h, mean 217.6 h, min −1,752 h, max 13,272.6 h (98.5% of cases closed) | Report distribution; negative durations cross-referenced under Integrity |
| Uniqueness | Exact duplicate `unique_key` | 0 | Nothing to drop |
| Uniqueness | Semantic-duplicate heuristic (same day + type + ZIP) | 183,200 groups, 993,543 rows (81.2% of all rows), largest group 4,989 reports | **Deliberately not acted on** — see narrative below |
| Integrity | `closed_date < created_date` | 340 rows (0.028% of closed cases) | Flag; excluded from duration-based analysis, not deleted |
| Integrity | Complaint types with no category mapping | 0 (180/180 mapped) | Controlled vocabulary has full coverage |
| Representativeness | Complaints per 1,000 residents by borough (2020 Census populations) | Bronx 202.7, Manhattan 137.8, Brooklyn 128.1, Queens 122.8, Staten Island 90.4 | Disclose: complaint volume is not proportional to population — a reporting-behavior signal, not necessarily an incident-rate signal |
| Representativeness | Single weather station for the whole city | Central Park (`USW00094728`) only | Disclose as a known limitation; not fixable with this data |

## Completeness

Real (`NaN`) missing rates on the full 311 data: `descriptor` 2.60%, `closed_date` 1.49%,
`latitude`/`longitude` 1.34% each, `incident_zip` 0.78%; all other used columns are 0% missing.

Disguised missing values: 811 rows (0.07%) hold `borough == "Unspecified"` rather than a real
NaN — a placeholder, not a genuine sixth borough. No `incident_zip == "00000"` placeholders were
found (0 rows).

`closed_date` is missing for 18,210 rows (1.49%). Breaking this down by `status` shows it isn't
one uniform story: 16,327 rows (89.7%) belong to cases that are still active (`In Progress`,
`Pending`, `Open`, `Assigned`, `Started`, `Unspecified`) — a legitimate, expected gap. But 1,883
rows (10.3%) are marked `status == "Closed"` while still missing a `closed_date` — that combination
shouldn't exist, and is flagged here as a genuine completeness/integrity anomaly rather than
folded into the "legitimate" bucket.

Weather is fully complete in this window: 243/243 expected calendar days present, 0% missing
values in any of the 6 columns.

**Screenshot:** `figures/fig_05_missingno_matrix.png` (missingno matrix, 50,000-row sample —
sampled purely for plot readability; all percentages above are computed on the full data).

## Consistency

`agency` → `agency_name` is a clean 1:1 mapping (0 codes map to more than one name). Borough
values show no spelling variants beyond the `Unspecified` placeholder already counted under
Completeness. `complaint_type` has 0 whitespace issues, but folding case shows 178 distinct values
instead of 180 — two pairs (`Elevator`/`ELEVATOR`, `PLUMBING`/`Plumbing`) are pure case variants of
each other. This didn't need a fix because the category mapping table already assigns both
variants of each pair to the same category (`BUILDING`), but it's a useful illustration of the
same casing pattern noted in Phase 2 (HPD-style ALL CAPS vs. DSNY/DOT/Parks-style Title Case) not
being fully consistent even within a single agency's own naming.

## Validity

ZIP format, NYC-bounding-box coordinates, in-window dates, and weather value ranges all passed at
100%. This is a genuinely clean result, not an oversight — it reflects the `$select`/`$where`
server-side filtering from Phase 1 (dates) and the fact that Socrata's own client-side entry
validation already screens out most malformed ZIPs/coordinates before they reach the public API.

## Accuracy

Hard to check without ground truth, especially for 311 (no independent record of what actually
happened at each address — this is disclosed as a limitation, not resolved). For weather, 3
extreme days within the actual subset window were spot-checked against independent sources:

| Date | Our value | External source | Agreement |
|---|---|---|---|
| 2025-01-22 (coldest `TMIN` in-window) | TMIN = −12.1 °C | NWS/press: 2025's lowest NYC temperature (10 °F) occurred Jan 22 (10 °F = −12.2 °C) | within 0.1 °C |
| 2025-02-08 (biggest `SNOW` in-window) | SNOW = 76.0 mm | NWS event page ["February 8–9, 2025 Snow, Sleet, and Ice Event"](https://www.weather.gov/okx/20250208_09): 3.1 in over Feb 8–9 (≈78.7 mm) | within ~3.5% (plausibly a day-boundary difference — the official figure spans two days, ours is a single calendar day) |
| 2025-07-29 (hottest `TMAX` in-window) | TMAX = 36.1 °C | Press coverage confirms an active NYC heat wave around this date (second heat wave of summer 2025) | qualitative confirmation only — no exact published high found for this specific date |

**Decision:** the two numerically-checked days are treated as good evidence the NOAA station data
is accurate; the third is noted as weaker corroboration rather than being overstated as "confirmed."

## Timeliness

Both raw files are snapshotted as of **2026-07-12** (`data/DOWNLOAD_LOG.md`). 98.5% of the 311
subset (1,205,247/1,223,457) has a `closed_date`; case duration for those runs from a median of
8.4 hours to a mean of 217.6 hours, with a long right tail (max 13,272.6 hours ≈ 553 days) and a
negative minimum (−1,752 hours) that is the same anomaly counted under Integrity. NOAA
daily-summary values can be corrected retroactively after initial publication, so "data as of
2026-07-12" applies to the weather file as much as to the 311 file — a re-download today would not
be expected to reproduce these exact numbers.

**Figure:** `figures/fig_06_case_duration_hist.png` (closed-case duration histogram, capped at 30
days for readability).

## Uniqueness

Zero exact duplicate `unique_key` values — nothing to drop on that front. The semantic-duplicate
heuristic from the roadmap (same calendar day + `complaint_type` + `incident_zip`) flags 183,200
groups covering 993,543 rows — 81.2% of the entire dataset — with the single largest group holding
4,989 reports.

**Decision — deliberately not acted on:** that 81% figure is a heuristic *upper bound*, not a
claim that 81% of rows are true duplicates. With ~180 complaint types and a few hundred ZIP codes
spread across 121 days and 1.2M rows, many genuinely independent reports collide on
(day, type, ZIP) by chance alone — e.g. dozens of different people filing separate `Illegal
Parking` complaints about different cars in the same ZIP on the same day are not one incident
reported many times. Collapsing on this heuristic would silently delete a large share of
genuinely distinct reports. The unit of analysis for this project is *reports*, not *incidents*,
so no deduplication beyond the (zero) exact-`unique_key` duplicates is applied — and this finding
is itself the argument for why a coarser heuristic like this needs much more signal (exact
address, descriptor-text similarity) before it could safely drive row removal.

## Integrity

340 rows (0.028% of closed cases) have `closed_date < created_date` — a small but nonzero
proportion, consistent with the negative-duration tail seen under Timeliness. These are flagged,
not deleted, and are excluded specifically from any duration-based analysis, not from the dataset
as a whole. Every one of the 180 distinct `complaint_type` values in the subset maps into
`data/complaint_category_map.csv` (0 unmapped) — the controlled vocabulary has full coverage.

## Representativeness

Complaints per 1,000 residents by borough (2020 Census populations — NYC Dept. of City Planning /
US Census Bureau figures: Brooklyn 2,736,074; Queens 2,405,464; Manhattan 1,694,251; Bronx
1,472,654; Staten Island 495,747):

| Borough | Complaints | Population (2020) | Complaints / 1,000 residents |
|---|---|---|---|
| Bronx | 298,456 | 1,472,654 | **202.7** |
| Manhattan | 233,481 | 1,694,251 | 137.8 |
| Brooklyn | 350,548 | 2,736,074 | 128.1 |
| Queens | 295,369 | 2,405,464 | 122.8 |
| Staten Island | 44,792 | 495,747 | 90.4 |

The Bronx files 311 reports at roughly double the per-capita rate of Staten Island. This is
disclosed as a reporting-behavior signal, not interpreted as "the Bronx has more actual problems"
— 311 measures *reports*, and reporting propensity plausibly varies by borough (renter vs. owner
mix, community-board engagement, awareness of the 311 system, etc.), which the data can't
disentangle on its own.

The weather side has its own representativeness limitation: a single station (Central Park)
stands in for the entire city. Coastal and outer-borough microclimates (e.g. the Rockaways,
Staten Island's shoreline) can differ meaningfully, especially for precipitation and wind-driven
events — a disclosed limitation, not something more data cleaning can fix.

## Tools used

pandas (`.isna()`, `.value_counts()`, `.groupby()`, regex matching), missingno (`msno.matrix`),
matplotlib (case-duration histogram), and the `ydata-profiling` HTML report from Phase 2
(`docs/311_profiling_report.html`) as a complementary, broader-but-shallower automated pass over
the same data.
