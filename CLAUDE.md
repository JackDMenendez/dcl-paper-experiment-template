<!-- markdownlint-disable MD022 MD025 MD033 MD060 -->
# CLAUDE.md -- Working Brief for Claude Code

> Project: <PAPER SHORT TITLE>

This file is the project memory for Claude Code. Keep it updated so a
new conversation can continue work without the full chat history.

The structure below is a starting point: replace the placeholder
sections with project-specific content as the work develops, and keep
the **CURRENT STATUS** block at the top up to date.

---

## CURRENT STATUS (YYYY-MM-DD) -- vX.Y-DRAFT

One- or two-paragraph summary of where the project is right now:

- What the headline claim of the paper currently is.
- What experiments / derivations are in progress vs.\ blocked.
- Which audit-table rows are PASS / PART / STUB / FAIL.
- What the next concrete action is (the smallest next step that
  unsticks the project).

Update this block whenever the answer to "what is the next action"
changes.

---

## What This Project Is

One paragraph framing of the framework or claim. The aim is to load
enough context that a new agent can read the next two sentences of a
section file and know what symbols mean.

---

## Paper Title and Theme

**Title:** <full title>

**Core theme / framing:** what the paper is *really* arguing. The
title is for the reader; this is for future-you.

---

## Audit Table Status

| Row | Status | What it claims |
|---|---|---|
| <claim name> | STUB | <one-line description> |

Mirror of `paper/sections/audit_table.tex` -- update this table when
the audit table changes. The claim auditor agent
(`.claude/agents/claim-auditor.md`) treats `audit_table.tex` as the
authority; this section is for quick orientation only.

---

## Conventions

- **Status legend.** `PASS` / `PART` / `STUB` / `FAIL` (defined in
  the front-matter of `paper/main.tex`).
- **File naming.** Sections: `paper/sections/<topic>.tex`. Figures:
  `paper/figures/<name>.{tex,pdf,png}` with `.tex` fragment + binary
  pair. Notes: `notes/<topic>.md`. Experiments:
  `src/experiments/exp_NN_<name>.{py,md}`.
- **Cross-references.** Always `\label{}` + `\ref{}` / `\autoref{}`,
  never hard-coded numbers. Section labels: `sec:<name>`. Subsection:
  `subsec:<name>`. Equation: `eq:<name>`. Figure: `fig:<name>`. Table:
  `tab:<name>`. Theorem: `thm:<name>`.
- **Bibliography.** All cites flow through `paper/paper-bib/references.bib`.
  Style: `\bibliographystyle{unsrt}` (numeric, in citation order).
- **LaTeX layout idioms.** `\nolinkurl{}` for paths, `\url{}` for URLs
  inside `\href{}`. `longtable` for tables that may span pages.
- **Experiments.** Each row in `paper/sections/audit_table.tex` whose
  evidence cell names `exp_NN` is operationally defined by
  `src/experiments/exp_NN_<name>.py`. The companion `.md` doc records
  parameters, runtime, and what PASS/PART means for that row. The
  master roll-up is `python audit_universe.py` (treats
  `audit_table.tex` as authority, parses cached `data/*.log` for
  PASS/FAIL -- does not re-execute experiments by default; opt-in
  via `--run-quick` or `--run <exp_id>`); see `audit_universe.md`.

## Documentation convention for code

Every non-trivial line of physics/framework code should say what it
**is** in the theory, not just what it does in the program. Name the
mathematical object, cite the paper section/equation, and use "IS" for
exact correspondences, "approximates" for continuum limits.

---

## Release flow

See `release_notes/README.md` for the full procedure. Summary:

1. CI green on `main`.
2. Update `CITATION.cff` (`version`, `date-released`).
3. Draft `release_notes/vX.Y.md` and `release_notes/vX.Y-release-message.md`.
4. **Deposit on Zenodo first** -- the DOI lands in the title-page
   `\thanks{}` block and `CITATION.cff` *before* the release commit.
5. Commit version bump (DOI included).
6. Build final PDF, snapshot to `.stage/<DOC_TITLE>_vX.Y.pdf`
   (durable per-version archive, gitignored).
7. Tag `vX.Y`, push the tag.
8. Create the GitHub Release using the release-message body.

---

## What NOT to Change

- <load-bearing files / conventions to preserve>

---

## Notes Index (important theoretical / scratchpad files)

`notes/README.md` -- conventions for notes/

(List individual notes here as they accumulate. Notes are durable
working documents; the paper cites them indirectly via the audit
table's evidence column.)
