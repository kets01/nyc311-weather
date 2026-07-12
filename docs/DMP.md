# Data Management Plan

> Filled in phase by phase as work progresses (Phase 6 finalizes it). Replace every plan with what
> was *actually done*. See CONTEXT.md §6 for the full reasoning behind each answer.

## Roles

## Data collection

## Storage

## Backup

3-2-1 rule: 3 copies, 2 media, 1 off-site.
1. **Laptop** — this working copy (`C:\Users\kemki\Documents\master\MSD\Exam\nyc311-weather`).
2. **Cloud / off-site** — GitHub remote `https://github.com/kets01/nyc311-weather.git`, set up
   2026-07-12 and pushed after the Phase 0 commit. Covers code, docs, and notebooks (not the raw
   data — `data/raw/` is gitignored, see below).
3. **External drive/USB** — still TODO. Because `data/raw/` is excluded from Git (it's the one
   thing GitHub doesn't back up), a periodic manual copy of the whole project folder to a USB/
   external drive is the plan to cover the raw CSVs. To do before Phase 10's final checklist;
   restore-tested by opening one copied file.

## Naming

## Folder structure

## Version control

## File formats

## Documentation & metadata

## Licenses

## Ethics & privacy

## Security

## Preservation

## Environment (long-term)

## Publication (described, not executed)

## Risks
