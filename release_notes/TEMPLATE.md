<!-- markdownlint-disable MD022 MD024 MD032 MD047 MD060 -->
# vX.Y Release Notes

**Released:** YYYY-MM-DD
**Prior version:** vX.Y-1 (released YYYY-MM-DD)
**Tag:** vX.Y
**DOI:** [10.5281/zenodo.XXXXXXXX](https://doi.org/10.5281/zenodo.XXXXXXXX)

## Why vX.Y

Two or three sentences on the *purpose* of this release. Not a list of
changes -- those come below. Examples:

- vX.Y closes a release-candidate cycle: open proof-sketch items moved
  from `notes/` into the paper at the sufficiency-with-pointers level.
- vX.Y is a maintenance release: corrections and clarifications, no
  new claims.
- vX.Y is a major revision: re-derived chapter N from a stronger
  starting point.

## Summary of changes since vX.Y-1

### New experimental work

1. **`exp_NN` (one-line title).** Result, audit-table status.
2. ...

### New theoretical work (proof sketches + paper-section patches)

3. **Tier N: <topic>** (\S of the paper). What changed and why.
   Source note: `notes/<file>.md`.
4. ...

### New audit-table rows

Additive rows in `paper/sections/audit_table.tex`:

- **"<Claim>"** (`exp_NN`, `STATUS`).
- ...

### Layout / polish

- ...

### Computational scaffolding

- Scripts added in `src/utilities/` and what each one establishes.

### Follow-on paper index updates

- `notes/follow_on_implications.md` (or equivalent index file)
  changes.

## What is not in vX.Y (explicit follow-on scope)

- Item, deferred to companion paper #N.
- ...

## Bibliography additions

- `key_year` -- description. Cited in \S<section> (or "parked, not
  yet cited").

## Reproducibility

One paragraph on how the headline result can be reproduced from a
fresh clone of the tag, including approximate wall-clock time on a
named hardware class.

---

For the detailed change list of all commits between vX.Y-1 and vX.Y,
see `git log vX.Y-1..vX.Y`.
