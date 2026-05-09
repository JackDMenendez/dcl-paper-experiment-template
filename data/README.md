# data/

Data files produced and consumed by experiments.

## What goes here

- `*.npy` -- NumPy arrays produced by experiment scripts.
- `*.log` -- stdout captures from long-running experiments.
- `*.csv` -- tabular results that downstream figures read.

## What does NOT go here

- Source code (lives in `src/`).
- Figures (live in `paper/figures/` or the repo-root `figures/`).
- Build artefacts (live in `build/`).

## Tracking in git

`.npy` files are tracked when small enough that the repo stays
manageable. For multi-gigabyte outputs, store them in Zenodo or a
data-archive service and refer to them by DOI from the experiment's
companion `.md` doc and from the audit-table evidence column.

`.log` files are tracked (the `.gitignore` has `!data/*.log`) so the
exact stdout of each PASS/FAIL run is part of the project history.

## Naming

`<exp_id>_<descriptor>.{npy,log}` -- e.g. `exp_00_example.npy`,
`exp_12c_grid_113.log`. The `<exp_id>` prefix lets you `ls data/exp_12*`
and see everything that experiment touched.
