# exp_00_example -- Companion Doc

**Audit row:** "Example claim, partial evidence" in
`paper/sections/audit_table.tex`.
**Status:** STUB
**Last run:** -

## What this experiment claims

One paragraph naming the specific quantitative claim being tested.
What is computed, what it is compared to, and what tolerance counts as
PASS.

## Parameters

| Name | Value | Why |
|---|---|---|
| seed | 0 | Determinism |
| sample_size | 10000 | Sufficient for the central-limit bound |
| tolerance | 0.05 | 95% CI on standard-normal mean of N=10000 |

## How to run

Direct invocation (and capture the log so `audit_universe.py` can
inspect it later):

```sh
python -u src/experiments/exp_00_example.py 2>&1 \
    | tee data/exp_00_example.log
```

Or via the audit-script's run helper, which captures the log
automatically:

```sh
python audit_universe.py --run exp_00_example
```

Approximate runtime: <1 s on a laptop. The script declares
`RUNTIME_BUDGET_SECONDS = 1`, so it is included in
`audit_universe.py --run-quick`.

## Output

| File | Contents |
|---|---|
| `data/exp_00_example.npy` | The 10000-sample array |
| `data/exp_00_example.log` | Captured stdout, parsed by `audit_universe.py` for PASS / FAIL marker |

## What PASS means

`|sample mean - 0| < 0.05`.

## What to do if it fails

This is a deterministic seeded test; a FAIL means either NumPy's RNG
behaviour changed or the code was edited. Inspect the saved `.npy`,
diff against the prior commit's data file, and update either the
code, the tolerance, or the audit row -- whichever is the actual
truth.

## Replacing this exemplar

When you write your first real experiment:
1. Delete this file and `exp_00_example.py`.
2. Drop the `Example claim, partial evidence` row from
   `paper/sections/audit_table.tex` and add a real one.
3. Update the index row in `src/experiments/EXPERIMENTS.md`.
4. Add the experiment's entry to `audit_universe.py` (or its
   `EXPERIMENTS` list).
