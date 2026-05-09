# src/experiments/

Numerical experiments backing the paper's claims. Each experiment is
the operational definition of one row in
`paper/sections/audit_table.tex` -- if the audit row says "evidence:
exp_NN", running `exp_NN` is what produces that evidence.

## Naming

Every experiment has three files:

| File | Role |
|---|---|
| `exp_NN_short_name.py` | Runnable script. Prints PASS/FAIL/STUB to stdout, drops data into `data/`. |
| `exp_NN_short_name.md` | Companion doc. What the experiment claims, parameters, expected output, what to do if it fails. |
| (entry in `EXPERIMENTS.md`) | Index row pointing at both. |

`NN` is a two-digit zero-padded sequence number. Sub-experiments use a
letter suffix (`exp_12b`, `exp_12c`, `exp_12d_tight`).

## Running

A single experiment:
```sh
python -u src/experiments/exp_00_example.py
```

The whole suite, with PASS/FAIL/STUB summary:
```sh
python audit_universe.py        # from repo root
python audit_universe.py --list # show planned experiments without running
```

The `make experiments` target delegates to `src/experiments/makefile`
where individual targets (`make -C src/experiments exp_NN`) are wired
up. Many experiments take hours to days to run -- prefer named
targets to the suite-level `all`.

## Lifecycle of an experiment

1. **STUB**: row added to `audit_table.tex` with status `STUB`. The
   `.py` file may not exist yet; the `.md` describes what the
   experiment will check.
2. **In progress**: `.py` runs but output is not yet a clean PASS.
   Keep status `STUB` or `PART` in the audit table; the `.md` records
   what is missing.
3. **PART**: experiment runs and demonstrates the mechanism, but the
   quantitative match is not yet at the stated precision. The `.md`
   names the specific gap.
4. **PASS**: experiment runs cleanly and confirms the audit-row
   claim. Numbers in the audit-table evidence column match the
   experiment's printed output.
5. **FAIL**: experiment runs cleanly and disconfirms the claim.
   Promote this to first-class status -- a confirmed FAIL is a more
   important result than a PASS. The `.md` records the disconfirming
   evidence; the audit row stays as `FAIL` rather than being deleted.

## Conventions

- Experiments write data files to `data/<exp_id>_<descriptor>.npy`
  (NumPy arrays) and `data/<exp_id>_<descriptor>.log` (stdout
  captures). Both are tracked by git when reasonably small.
- Long-running experiments should print incremental progress so the
  user can `tail -f` the log file.
- A failing experiment exits non-zero so `audit_universe.py` and CI
  catch it. Every script ends with
  `if __name__ == "__main__": sys.exit(0 if success else 1)`.
