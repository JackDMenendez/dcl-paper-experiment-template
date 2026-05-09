# audit_universe -- companion doc

`audit_universe.py` is the master roll-up that reports the project's
status against the paper's audit table. Run it from the repo root:

```sh
python audit_universe.py
```

It exits non-zero only when a cached log contradicts a declared
non-FAIL row (a regression). In all other cases it prints a status
table and exits 0.

## Why it does not re-run experiments by default

Real research projects accumulate experiments that take 24+ hours to
run. The original "run every experiment in sequence" model is fine
for sub-minute checks but unusable as soon as the suite includes
multi-day experiments. Rerunning the whole suite on every commit is
not viable, and a master roll-up that nobody actually invokes is
worse than no roll-up at all.

The redesigned model treats `paper/sections/audit_table.tex` as the
**authority** and the cached `data/<exp_id>*.log` files as the
**evidence trail**. Re-derivation is a separate, opt-in concern.

## How a row is checked

For each row in `paper/sections/audit_table.tex`:

1. The script extracts the **declared status** (`PASS` / `PART` /
   `STUB` / `FAIL`) from the row's status cell.
2. The script extracts every **experiment ID** mentioned in the
   row's evidence cell (e.g. `exp_12c`, `exp_12d_tight`). Rows whose
   evidence is purely analytical ("Derived analytically (\S...)")
   have no experiment IDs and are reported as-is.
3. For each experiment ID, the script finds the **most recent
   `data/<exp_id>*.log`** by mtime and parses it for a PASS / PART /
   STUB / FAIL marker.
4. A **discrepancy** is flagged when:
   - the row is declared `PASS` or `PART` but the log says `FAIL`, or
   - the row is declared `PASS` and no log is present at all.

The script does NOT flag a row whose declared status is `STUB` --
those rows are admissions of pending work, not claims that need
backing.

## Modes

| Command | Effect |
|---|---|
| `python audit_universe.py` | Default. Parse table + parse logs, print report. |
| `python audit_universe.py --check-freshness` | Also flag any log whose mtime predates its experiment script's mtime. The script was edited after the log was generated -- the log is stale. |
| `python audit_universe.py --run-quick` | Re-run every experiment whose `RUNTIME_BUDGET_SECONDS` attribute is below 60 (the `QUICK_BUDGET_SECONDS` constant). Useful in CI. |
| `python audit_universe.py --run EXP_ID` | Re-run one experiment by ID, regardless of budget. Captures stdout to `data/<exp_id>*.log`. |
| `python audit_universe.py --list` | List the audit-table rows without running anything. |

## Conventions an experiment script must follow

For an experiment to be visible to this audit:

1. **Filename.** `src/experiments/exp_NN_<short_name>.py`. The
   `exp_NN` prefix is what the audit table's evidence column refers
   to and what the audit-script glob keys on.
2. **Status marker in stdout.** Print `<exp_id> PASS` (or `PART` /
   `FAIL`) on its own line near the end. The audit script picks the
   last marker in the log.
3. **Capture the log.** When run via `make -C src/experiments
   exp_NN` or via `audit_universe.py --run`, stdout is captured to
   `data/exp_NN_<short_name>.log` automatically. When run by hand,
   redirect stdout yourself:
   ```sh
   python -u src/experiments/exp_NN_short_name.py 2>&1 \
       | tee data/exp_NN_short_name.log
   ```
4. **Optional: a runtime budget.** A module-level constant tells
   `--run-quick` whether the experiment fits in CI:
   ```python
   RUNTIME_BUDGET_SECONDS = 30  # rough wall-clock estimate
   ```
   Experiments without this attribute are skipped by `--run-quick`.

## What this design does NOT solve

- **Determinism.** "PASS in the most recent log" only matches "PASSes
  now" if the experiment is deterministic for fixed parameters. Any
  experiment whose result depends on environment, RNG state, or
  external data should record those inputs in its companion `.md`
  doc and rerun cadence in its row's evidence cell.
- **Runtime invariants.** The audit script trusts the log marker. If
  an experiment prints `PASS` even when it shouldn't, this script
  will not catch it. Unit tests in `tests/` are the layer that
  catches those bugs; the audit is the layer above unit tests.
- **Long-horizon stability.** A short run that PASSes can hide a
  long-horizon failure (cf.\ `exp_12c` in the source DCL project).
  The audit table should carry a separate row for the long-horizon
  claim, not be silent about it.

## Adding a new experiment

Three files land together:

1. **Audit row** in `paper/sections/audit_table.tex` (declares the
   claim, names the experiment ID, sets initial status).
2. **Script + companion doc** in `src/experiments/`
   (`exp_NN_<name>.py` + `exp_NN_<name>.md`).
3. **Index entry** in `src/experiments/EXPERIMENTS.md`.

After the first run, `data/exp_NN_<name>.log` exists and
`audit_universe.py` will pick it up automatically -- no edits to
this script are needed.
