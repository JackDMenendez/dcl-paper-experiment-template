"""
audit_universe.py
Verify the paper's audit table against cached experiment results.

The authority is `paper/sections/audit_table.tex` -- every row whose
evidence cell names an experiment ID (`exp_NN_<name>`) maps to a
script in `src/experiments/` and to one or more log files in
`data/`.  This script reads the audit table, locates the most recent
log for each experiment, parses it for a PASS / PART / STUB / FAIL
marker, and reports whether the cached state agrees with the
declared state.

The script does NOT re-execute experiments by default.  Real research
projects accumulate experiments that take 24+ hours to run; rerunning
the whole suite on every commit is not viable.  The default mode runs
in seconds against whatever logs are already on disk.

Modes
-----
    python audit_universe.py
        Default.  Parse audit table + parse logs, print status,
        exit non-zero only when a log contradicts a declared
        non-FAIL status (i.e., a regression).

    python audit_universe.py --check-freshness
        Also flag experiments whose log is older than its `.py`
        script (the script has been edited but the log is stale).

    python audit_universe.py --run-quick
        Re-run every experiment whose `RUNTIME_BUDGET_SECONDS`
        attribute is below QUICK_BUDGET (default 60), then audit.
        Useful in CI.

    python audit_universe.py --run <exp_id>
        Re-run one experiment by ID, regardless of budget.

    python audit_universe.py --list
        List rows from the audit table without running or parsing.

Companion doc: `audit_universe.md`.
"""

from __future__ import annotations

import argparse
import importlib
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent
AUDIT_TABLE = REPO_ROOT / "paper" / "sections" / "audit_table.tex"
EXPERIMENTS_DIR = REPO_ROOT / "src" / "experiments"
DATA_DIR = REPO_ROOT / "data"

QUICK_BUDGET_SECONDS = 60
STATUS_TOKENS = ("PASS", "PART", "STUB", "FAIL")

# Regex that finds an experiment ID inside the evidence column.  The
# audit table escapes underscores as `\_` in LaTeX; we strip those
# before matching.  IDs look like exp_00, exp_00_example, exp_12c,
# exp_12d_tight, exp_12d_outlier_trace -- digits, optional letter,
# optional underscore-separated descriptor.
EXP_ID_RE = re.compile(r"\bexp_\d+\w*\b")

# Regex that finds a status declaration in the audit table's status
# column: the column may contain `\texttt{PASS}` or just `PASS`.
STATUS_RE = re.compile(r"\\texttt\{(PASS|PART|STUB|FAIL)\}|\b(PASS|PART|STUB|FAIL)\b")

# Regex that finds the experiment's status in its log.  Conventions:
# the script prints e.g. "exp_00_example PASS" near the end.
LOG_STATUS_RE = re.compile(
    r"\b(?:exp_\w+\s+)?(PASS|PART|STUB|FAIL)\b", re.MULTILINE
)


# ---------------------------------------------------------------------------
# Audit-table parsing
# ---------------------------------------------------------------------------

@dataclass
class AuditRow:
    """One row of paper/sections/audit_table.tex."""

    claim: str
    evidence: str
    declared_status: str
    exp_ids: list[str] = field(default_factory=list)


def _strip_line_comments(latex: str) -> str:
    """Remove %-comments from LaTeX source, preserving escaped \\%."""
    cleaned = []
    for line in latex.splitlines():
        out_chars = []
        i = 0
        while i < len(line):
            if line[i] == "%" and (i == 0 or line[i - 1] != "\\"):
                break
            out_chars.append(line[i])
            i += 1
        cleaned.append("".join(out_chars))
    return "\n".join(cleaned)


def _extract_longtable_body(latex: str) -> str:
    """Return only the row body of the longtable (skip prologue / footer)."""
    # The actual body starts after \endlastfoot if present (the
    # standard longtable header/footer block ends there), else
    # after \endhead.  These checks must be ordered: in a normal
    # longtable, \endhead appears before \endlastfoot, so a single
    # alternation regex would pick \endhead and the body would
    # wrongly include the \endfoot / \endlastfoot rows.
    start_match = re.search(r"\\endlastfoot", latex)
    if start_match is None:
        start_match = re.search(r"\\endhead", latex)
    end_match = re.search(r"\\end\{longtable\}", latex)
    if not start_match or not end_match:
        raise RuntimeError(
            "audit_table.tex: could not locate longtable body bounds"
        )
    return latex[start_match.end():end_match.start()]


def parse_audit_table(path: Path = AUDIT_TABLE) -> list[AuditRow]:
    """Parse the audit table; return one AuditRow per data row."""
    raw = path.read_text(encoding="utf-8")
    body = _extract_longtable_body(_strip_line_comments(raw))

    # Rows end with `\\`.  Splitting on the literal `\\` token gives
    # the rows; we then split each row on `&` to get the five cells.
    rows: list[AuditRow] = []
    for raw_row in body.split(r"\\"):
        cells = [c.strip() for c in raw_row.split("&")]
        if len(cells) != 5:
            continue  # blank lines, \hline-only rows, etc.

        claim, _mechanism, _continuum, evidence, status_cell = cells
        if not claim or claim.startswith("\\"):
            continue  # \hline entries

        status_match = STATUS_RE.search(status_cell)
        if not status_match:
            continue
        declared_status = status_match.group(1) or status_match.group(2)

        evidence_unescaped = evidence.replace(r"\_", "_")
        exp_ids = sorted({m.group(0) for m in EXP_ID_RE.finditer(evidence_unescaped)})

        rows.append(
            AuditRow(
                claim=claim,
                evidence=evidence,
                declared_status=declared_status,
                exp_ids=exp_ids,
            )
        )
    return rows


# ---------------------------------------------------------------------------
# Log inspection
# ---------------------------------------------------------------------------

def find_experiment_script(exp_id: str) -> Path | None:
    """Locate src/experiments/<exp_id>*.py for a given audit-row exp_id."""
    matches = sorted(EXPERIMENTS_DIR.glob(f"{exp_id}*.py"))
    return matches[0] if matches else None


def find_latest_log(exp_id: str) -> Path | None:
    """Most recent data/<exp_id>*.log file (by mtime)."""
    matches = list(DATA_DIR.glob(f"{exp_id}*.log"))
    if not matches:
        return None
    return max(matches, key=lambda p: p.stat().st_mtime)


def parse_log_status(log_path: Path) -> str | None:
    """Last PASS / PART / STUB / FAIL marker in the log, if any."""
    try:
        text = log_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    last = None
    for match in LOG_STATUS_RE.finditer(text):
        last = match.group(1)
    return last


def is_stale(log_path: Path, script_path: Path) -> bool:
    """True if the script has been modified more recently than the log."""
    return script_path.stat().st_mtime > log_path.stat().st_mtime


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

@dataclass
class RowResult:
    row: AuditRow
    log_status_per_exp: dict[str, str | None] = field(default_factory=dict)
    log_path_per_exp: dict[str, Path | None] = field(default_factory=dict)
    stale_per_exp: dict[str, bool] = field(default_factory=dict)
    discrepancy: bool = False
    notes: list[str] = field(default_factory=list)


def audit(
    rows: Iterable[AuditRow],
    *,
    check_freshness: bool = False,
) -> list[RowResult]:
    results: list[RowResult] = []
    for row in rows:
        result = RowResult(row=row)

        if not row.exp_ids:
            # Analytical / derivation row.  Nothing to look up; declared
            # status stands.  Note this so the report shows it.
            result.notes.append("analytical (no experiment evidence)")
            results.append(result)
            continue

        for exp_id in row.exp_ids:
            log_path = find_latest_log(exp_id)
            result.log_path_per_exp[exp_id] = log_path
            log_status = parse_log_status(log_path) if log_path else None
            result.log_status_per_exp[exp_id] = log_status

            if check_freshness and log_path is not None:
                script_path = find_experiment_script(exp_id)
                if script_path is not None:
                    result.stale_per_exp[exp_id] = is_stale(log_path, script_path)

        # Discrepancy = any exp's log status is FAIL while declared
        # status is PASS / PART, OR no log present for an experiment
        # the audit table marks PASS.
        for exp_id, log_status in result.log_status_per_exp.items():
            declared = row.declared_status
            if declared in ("PASS", "PART") and log_status == "FAIL":
                result.discrepancy = True
                result.notes.append(
                    f"{exp_id}: declared {declared} but log says FAIL"
                )
            elif declared == "PASS" and log_status is None:
                result.discrepancy = True
                result.notes.append(
                    f"{exp_id}: declared PASS but no log found"
                )

        results.append(result)
    return results


def format_report(results: list[RowResult], *, check_freshness: bool) -> str:
    out: list[str] = []
    out.append("=" * 78)
    out.append("AUDIT UNIVERSE  --  cached-result roll-up")
    out.append(f"  authority:  {AUDIT_TABLE.relative_to(REPO_ROOT)}")
    out.append("=" * 78)

    for result in results:
        row = result.row
        marker = "!!" if result.discrepancy else "  "
        head = f"{marker} [{row.declared_status:<4}]  {row.claim}"
        if len(head) > 74:
            head = head[:71] + "..."
        out.append(head)

        if not row.exp_ids:
            out.append(f"      analytical / derivation row")
            continue

        for exp_id in row.exp_ids:
            log_status = result.log_status_per_exp.get(exp_id)
            log_path = result.log_path_per_exp.get(exp_id)
            stale = result.stale_per_exp.get(exp_id, False)

            if log_path is None:
                out.append(f"      {exp_id:<24}  no log found")
            else:
                rel_log = log_path.relative_to(REPO_ROOT)
                marker_log = log_status or "no PASS/FAIL marker"
                stale_tag = "  [STALE]" if (check_freshness and stale) else ""
                out.append(
                    f"      {exp_id:<24}  log: {marker_log:<5}  "
                    f"{rel_log}{stale_tag}"
                )

        for note in result.notes:
            out.append(f"      ! {note}")

    out.append("=" * 78)
    out.append("SUMMARY")
    out.append("=" * 78)
    declared_counts: dict[str, int] = {tok: 0 for tok in STATUS_TOKENS}
    for result in results:
        declared_counts[result.row.declared_status] += 1
    summary = "  ".join(f"{tok}:{declared_counts[tok]}" for tok in STATUS_TOKENS)
    out.append(f"  declared:  {summary}")

    discrepancies = [r for r in results if r.discrepancy]
    out.append(f"  discrepancies:  {len(discrepancies)}")
    if discrepancies:
        for r in discrepancies:
            out.append(f"    - {r.row.claim}")

    return "\n".join(out)


# ---------------------------------------------------------------------------
# Optional re-execution
# ---------------------------------------------------------------------------

def _runtime_budget(exp_id: str) -> int | None:
    """Read the RUNTIME_BUDGET_SECONDS attribute from an experiment module."""
    script = find_experiment_script(exp_id)
    if script is None:
        return None
    module_name = f"src.experiments.{script.stem}"
    try:
        module = importlib.import_module(module_name)
    except Exception:
        return None
    return getattr(module, "RUNTIME_BUDGET_SECONDS", None)


def run_experiment(exp_id: str) -> bool:
    """Re-execute one experiment and capture its stdout to data/."""
    script = find_experiment_script(exp_id)
    if script is None:
        print(f"  no script found for {exp_id}", file=sys.stderr)
        return False
    DATA_DIR.mkdir(exist_ok=True)
    log_path = DATA_DIR / f"{script.stem}.log"
    print(f"  running {script.name} -> {log_path.relative_to(REPO_ROOT)}")
    with log_path.open("w", encoding="utf-8") as log_file:
        result = subprocess.run(
            [sys.executable, "-u", str(script)],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            cwd=REPO_ROOT,
        )
    return result.returncode == 0


def run_quick(rows: list[AuditRow], budget: int = QUICK_BUDGET_SECONDS) -> None:
    seen: set[str] = set()
    for row in rows:
        for exp_id in row.exp_ids:
            if exp_id in seen:
                continue
            seen.add(exp_id)
            ttl = _runtime_budget(exp_id)
            if ttl is None:
                print(f"  skip {exp_id}: no RUNTIME_BUDGET_SECONDS declared")
                continue
            if ttl > budget:
                print(f"  skip {exp_id}: budget {ttl}s exceeds {budget}s")
                continue
            run_experiment(exp_id)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.strip().splitlines()[1])
    p.add_argument(
        "--check-freshness", action="store_true",
        help="flag experiments whose log is older than its .py script",
    )
    p.add_argument(
        "--run-quick", action="store_true",
        help=f"re-run experiments with RUNTIME_BUDGET_SECONDS <= {QUICK_BUDGET_SECONDS}",
    )
    p.add_argument(
        "--run", metavar="EXP_ID",
        help="re-run one experiment by ID, regardless of budget",
    )
    p.add_argument(
        "--list", action="store_true",
        help="list audit-table rows without running or parsing logs",
    )
    args = p.parse_args(argv)

    rows = parse_audit_table()

    if args.list:
        for row in rows:
            exp_tag = ", ".join(row.exp_ids) if row.exp_ids else "analytical"
            print(f"  [{row.declared_status:<4}]  {row.claim}  ({exp_tag})")
        return 0

    if args.run:
        ok = run_experiment(args.run)
        return 0 if ok else 1

    if args.run_quick:
        run_quick(rows)

    results = audit(rows, check_freshness=args.check_freshness)
    print(format_report(results, check_freshness=args.check_freshness))
    return 1 if any(r.discrepancy for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
