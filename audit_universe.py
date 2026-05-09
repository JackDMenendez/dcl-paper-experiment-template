"""
audit_universe.py
Master audit runner for the project.

Runs every experiment in EXPERIMENTS in sequence and reports
PASS / STUB / FAIL for each.  A row in the audit table
(`paper/sections/audit_table.tex`) should only carry status PASS
when the corresponding experiment passes here.

Usage:
    python audit_universe.py           # run all experiments
    python audit_universe.py --list    # list experiments without running
"""

import importlib
import sys
import traceback


# Each entry is (audit-id, dotted module path, function name).
# The function should return True on PASS, raise on FAIL, and raise
# NotImplementedError if it is still a stub.
EXPERIMENTS = [
    ("exp_00_example",
     "src.experiments.exp_00_example",
     "run_example_audit"),
]


def run_all() -> bool:
    results = []
    print("=" * 60)
    print("UNIVERSE AUDIT")
    print("=" * 60)

    for exp_id, module_path, function_name in EXPERIMENTS:
        print(f"\n[{exp_id}] {function_name}")
        try:
            module = importlib.import_module(module_path)
            func = getattr(module, function_name)
            func()
            results.append((exp_id, "PASS"))
            print(f"  --> PASS")
        except NotImplementedError:
            results.append((exp_id, "STUB"))
            print(f"  --> STUB (not yet implemented)")
        except Exception as e:
            results.append((exp_id, "FAIL"))
            print(f"  --> FAIL: {e}")
            traceback.print_exc()

    print("\n" + "=" * 60)
    print("AUDIT SUMMARY")
    print("=" * 60)
    for exp_id, status in results:
        print(f"  {exp_id:<32} {status}")

    passed = sum(1 for _, s in results if s == "PASS")
    total = len(results)
    print(f"\n{passed}/{total} experiments passing.")
    return passed == total


if __name__ == "__main__":
    if "--list" in sys.argv:
        for exp_id, _, fn in EXPERIMENTS:
            print(f"  {exp_id:<32} {fn}")
    else:
        success = run_all()
        sys.exit(0 if success else 1)
