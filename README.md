# Paper + Experiment Template (full-stack)

A starting scaffold for a research paper that ships with companion
numerical experiments, derived from the *Geometry First* (A=1
Discrete Causal Lattice) project's infrastructure. Use this when the
paper's claims are operationally defined by code that runs and
produces verifiable output. For pure-theory papers without
experiments, use the paper-only sibling template instead.

## Click "Use this template" on GitHub

This repo is configured as a GitHub Template Repository. From the
GitHub web UI on the template's page, click **Use this template ->
Create a new repository**, then `git clone` the new repo locally.

## What you get

```
.
+-- paper/                        (LaTeX paper -- same shell as the paper-only template)
|   +-- main.tex                 -- title page, front matter, section wiring
|   +-- macros/                  -- packages.tex, commands.tex
|   +-- sections/                -- placeholders + 1 exemplar (introduction.tex)
|   |   +-- audit_table.tex      -- longtable seed, two example rows
|   +-- figures/                 -- example_figure.tex fragment + README
|   +-- paper-bib/references.bib -- BibTeX seed
+-- src/
|   +-- core/                    -- framework primitives (README only)
|   +-- experiments/             -- one exemplar (exp_00_example.{py,md})
|   |   +-- README.md            -- conventions
|   |   +-- EXPERIMENTS.md       -- index of experiments
|   |   +-- makefile             -- per-experiment make targets
|   +-- utilities/               -- figure generators, verification scripts
+-- tests/
|   +-- test_example.py          -- exemplar pytest unit test
+-- data/
|   +-- README.md                -- data-file conventions
+-- notes/                        -- working theoretical notes
+-- release_notes/                -- per-version change log + Release body
+-- .claude/agents/claim-auditor.md  -- read-only audit agent
+-- audit_universe.py             -- master PASS/STUB/FAIL audit (parses audit_table.tex + data/*.log)
+-- audit_universe.md             -- companion doc explaining the audit model
+-- virtual-env-requirements.txt  -- Python dependencies (read by make env and by the wcde repo-setup.sh bootstrap)
+-- CLAUDE.md                     -- project memory for Claude Code
+-- CITATION.cff                  -- machine-readable citation
+-- LICENSE                       -- MIT
+-- makefile common.mak           -- root build (paper + tests + experiments)
+-- build.sh build.cmd            -- platform wrappers around make
+-- setup.sh setup.cmd            -- create venv + install requirements
+-- .gitignore .gitattributes .gitmessage
```

## First steps after creating your repo

1. **Search-and-replace the placeholders** in:
   - `paper/main.tex` -- title, author, ORCID, email, repo URL
   - `paper/macros/packages.tex` -- pdftitle, pdfauthor, pdfsubject,
     pdfkeywords
   - `CITATION.cff` -- title, author, ORCID, repo URL
   - `LICENSE` -- year and copyright holder
   - `CLAUDE.md` -- short title, current status block
   - `README.md` (this file) -- replace with your project's own README
2. **Set up the environment** (creates `.venv`, installs requirements):
   ```sh
   ./setup.sh                  # POSIX / MSYS2 UCRT64 on Windows
   setup.cmd                   # Windows cmd / PowerShell
   ```
3. **Sanity-check the toolchain**:
   ```sh
   ./build.sh tests            # pytest against tests/
   ./build.sh paper            # pdflatex 3-pass + bibtex
   python -u src/experiments/exp_00_example.py
   python audit_universe.py    # PASS/STUB/FAIL roll-up
   ```
4. **Replace the exemplars** with the first real piece of the paper:
   - the introduction (`paper/sections/introduction.tex`)
   - the first experiment (`src/experiments/exp_00_example.{py,md}`)
   - the audit-table rows in `paper/sections/audit_table.tex`
5. **Each new experiment** gets three things in lock-step: a row in
   `paper/sections/audit_table.tex`, a `.py` script + `.md` companion
   doc in `src/experiments/`, and an entry in `audit_universe.py` and
   `src/experiments/EXPERIMENTS.md`. The `claim-auditor` agent under
   `.claude/agents/` flags prose that drifts out of sync with the
   audit table.

## Build requirements

- GNU Make >= 4.3 (the stock Windows port is too old; on Windows use
  MSYS2 UCRT64 with `pacman -S make`).
- Python 3 with `venv` (created by `setup.sh` / `setup.cmd`).
- `pdflatex` + `bibtex` (TeX Live or MiKTeX).

## Running experiments

A single experiment:
```sh
python -u src/experiments/exp_00_example.py
```

The whole suite, with PASS/STUB/FAIL summary:
```sh
python audit_universe.py
```

The `make experiments` target delegates to `src/experiments/makefile`
where individual targets (`make -C src/experiments exp_NN`) are wired
up. Many experiments take hours to days to run -- prefer named
targets to the suite-level `all`.

## Release flow

See `release_notes/README.md`. Short version: deposit on Zenodo
first to get the DOI, *then* commit the version bump. The DOI is part
of the title-page `\thanks{}` block and `CITATION.cff`.

## License

Paper text and figures: CC BY 4.0.
Source (this scaffolding): MIT (see `LICENSE`).
