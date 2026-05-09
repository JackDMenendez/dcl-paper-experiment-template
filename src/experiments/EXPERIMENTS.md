# Experiment Index

| ID | Status | What it claims | Audit row | Companion doc |
|---|---|---|---|---|
| `exp_00_example` | STUB | Placeholder for the first experiment | `Example claim, partial evidence` (Table~\ref{tab:audit}) | [exp_00_example.md](exp_00_example.md) |

Replace the example row above with real entries as experiments are
added. Keep this table in sync with `paper/sections/audit_table.tex`
-- the audit table is the public record; this file is the
implementer's index.

## Status legend

- `STUB` -- audit row added, experiment script not yet written or
  not yet producing a clean signal.
- `PART` -- experiment runs and demonstrates the mechanism but the
  quantitative match is incomplete; specific gap noted in the
  companion doc.
- `PASS` -- experiment confirms the audit row to stated precision.
- `FAIL` -- experiment disconfirms the audit row. Keep the row;
  failure is evidence too.

Status here should equal status in `audit_table.tex`. If they
disagree, the audit table is the authority and this file is wrong.
The `audit_universe.py` master roll-up uses `audit_table.tex` as its
authority and parses each experiment's most recent `data/*.log` for
the actual cached PASS/FAIL marker -- see `../../audit_universe.md`
for the full model.
