"""
exp_00_example.py
EXEMPLAR experiment.  Replace with the first real experiment.

This file shows the conventions the rest of the suite follows:

  - Top docstring states what claim is being tested, names the audit
    row it backs, and points to the companion .md doc.
  - A `RUNTIME_BUDGET_SECONDS` module attribute lets
    `audit_universe.py --run-quick` decide whether to re-execute this
    experiment in a CI window.  Omit the attribute (or set to None)
    for experiments that take longer than the QUICK_BUDGET_SECONDS
    threshold (default 60 s).
  - The script prints `<exp_id> PASS` (or PART/FAIL) on its own line
    near the end.  `audit_universe.py` parses the most recent
    `data/<exp_id>*.log` for the last such marker.
  - Data outputs go to data/<exp_id>_<descriptor>.{npy,log} so they
    live alongside the experiment.

Audit row (paper/sections/audit_table.tex):
  "Example claim, partial evidence"
Companion doc:
  src/experiments/exp_00_example.md
"""

import sys
from pathlib import Path

import numpy as np

# Wall-clock estimate read by `audit_universe.py --run-quick`.
# Set to None (or omit the attribute) for experiments that don't fit
# in a CI window.
RUNTIME_BUDGET_SECONDS = 1

# Output directory (data/) lives at repo root, not inside src/.
REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"


def run_example_audit() -> bool:
    """Run the example audit; return True on PASS, raise on FAIL.

    The companion .md doc describes what this checks and what
    "PASS" means.  Replace the body with the real experiment.
    """
    DATA_DIR.mkdir(exist_ok=True)

    # Trivial check: a deterministic computation produces the
    # expected value to within tolerance.  Replace this block with
    # the actual mechanism the experiment is exercising.
    rng = np.random.default_rng(seed=0)
    samples = rng.normal(loc=0.0, scale=1.0, size=10_000)
    mean = float(samples.mean())
    expected = 0.0
    tolerance = 0.05

    np.save(DATA_DIR / "exp_00_example.npy", samples)
    print(f"sample mean = {mean:.4f} (expected {expected}, tol {tolerance})")

    if abs(mean - expected) > tolerance:
        raise AssertionError(
            f"exp_00_example FAIL: |mean - expected| = "
            f"{abs(mean - expected):.4f} > {tolerance}"
        )

    print("exp_00_example PASS")
    return True


if __name__ == "__main__":
    try:
        ok = run_example_audit()
    except AssertionError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    sys.exit(0 if ok else 1)
