# Data Quality Findings

> Filled in during Phase 3, from `notebooks/03_quality.ipynb`. Every finding must be a NUMBER.
> Assessing and cleaning are kept separate: this document only records findings, not fixes.

## Preliminary notes carried over from Phase 2 (exploration)

`01_explore_311.ipynb` and `02_explore_weather.ipynb` are descriptive-only, but surfaced a few
things Phase 3 needs to check formally:
- `descriptor` (2.60%), `closed_date` (1.49%), `latitude`/`longitude` (1.34% each), `incident_zip`
  (0.78%) have real NaNs; `borough` has 0% real NaNs but 811 rows (0.07%) hold the placeholder
  value `Unspecified` — a disguised-missing case for the completeness section, not consistency.
- Casing pattern: HPD-style complaint types are ALL CAPS (`HEAT/HOT WATER`, `UNSANITARY
  CONDITION`) while DSNY/DOT/Parks-style types are Title Case (`Dirty Condition`, `Street
  Condition`) — worth a mention under consistency, though it doesn't need fixing (the mapping
  table already handles both).
- `unique_key` had 0 duplicated values in the combined 1,223,457-row subset — exact-duplicate
  uniqueness looks clean; the semantic-duplicate heuristic (same day + type + ZIP) is still open
  for Phase 3.3.6.
- Weather: 243/243 expected calendar days present, 0% missing values, 0 out-of-range
  temperature/precipitation values — this dataset looks clean going into Phase 3.

## Summary table

| Dimension | Finding | Number | Decision |
|---|---|---|---|
| Completeness | | | |
| Consistency | | | |
| Validity | | | |
| Accuracy | | | |
| Timeliness | | | |
| Uniqueness | | | |
| Integrity | | | |
| Representativeness | | | |

## Completeness

## Consistency

## Validity

## Accuracy

## Timeliness

## Uniqueness

## Integrity

## Representativeness
