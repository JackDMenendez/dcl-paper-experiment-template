# Full-stack paper-and-experiment template -- root build
# ----------------------------------------------------------------------------
# Requirements
#   GNU Make >= 4.3   (uses grouped-target `&:` syntax in src/experiments)
#   pdflatex, bibtex  (MiKTeX or TeX Live)
#   Python 3 + venv
#
#   Run from an MSYS2 UCRT64 shell on Windows. The stock Windows GNU Make
#   port (3.81) is too old. Confirm with: `make --version` -> >= 4.3.
# ----------------------------------------------------------------------------
# Targets
#   all          env -> tests -> paper -> promote          (default)
#   env          create .venv, install requirements
#   tests        run pytest against tests/
#   paper        build PDF (3-pass pdflatex + bibtex)
#   promote      copy final PDF (and any PROMOTE_FIGS) into stage/
#   experiments  delegate to src/experiments/makefile (see WARNING below)
#   clean        remove build/ and stage/
#   clean-env    also remove .venv
#   help         print this list
#
# Long experiments -- prefer running them one at a time
#   `make experiments` runs every target in src/experiments/makefile.
#   Many experiments take hours; some take days. Prefer named targets:
#       make -C src/experiments exp_00_example
# ----------------------------------------------------------------------------

RELATIVE_PATH :=
include common.mak

# --- Paper ------------------------------------------------------------------
DOC_TITLE := Paper
DOC_PDF   := $(build_dir)/$(DOC_TITLE).pdf

PAPER_DIR    := paper
PAPER_INPUTS := $(PAPER_DIR)/main.tex \
                $(wildcard $(PAPER_DIR)/sections/*.tex) \
                $(wildcard $(PAPER_DIR)/macros/*.tex) \
                $(wildcard $(PAPER_DIR)/paper-bib/*.bib)

PDFLATEX_PAPER := cd $(PAPER_DIR) && $(PDFLATEX) -output-directory=../$(build_dir)
BIBTEX_PAPER   := cd $(PAPER_DIR) && $(BIBTEX) ../$(build_dir)

# --- Promote ----------------------------------------------------------------
PROMOTE_FIGS :=
PROMOTE_PDF_TARGETS := $(stage_dir)/$(DOC_TITLE).pdf
PROMOTE_FIG_TARGETS := $(addprefix $(stage_dir)/,$(PROMOTE_FIGS))

# --- Tests ------------------------------------------------------------------
TEST_DIR := tests

.PHONY: all help env tests paper promote experiments clean clean-env

all: env tests paper promote
	@echo "================ Build Complete ================"

help:
	@sed -n '1,30p' makefile

# --- Environment ------------------------------------------------------------
$(VENV):
	python -m venv $(VENV)

$(VENV)/touchfile: $(VENV) virtual-env-requirements.txt
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r virtual-env-requirements.txt
	touch $(VENV)/touchfile

env: $(VENV)/touchfile

# --- Tests ------------------------------------------------------------------
tests: $(VENV)/touchfile
	$(PYTHON) -m pytest $(TEST_DIR) -v

# --- Paper ------------------------------------------------------------------
paper: $(DOC_PDF)

$(build_dir) $(stage_dir):
	mkdir -p $@

$(DOC_PDF): $(PAPER_INPUTS) | $(build_dir)
	$(PDFLATEX_PAPER) -jobname=$(DOC_TITLE) main.tex
	$(BIBTEX_PAPER)/$(DOC_TITLE)
	$(PDFLATEX_PAPER) -jobname=$(DOC_TITLE) main.tex
	$(PDFLATEX_PAPER) -jobname=$(DOC_TITLE) main.tex

# --- Promote ----------------------------------------------------------------
promote: $(PROMOTE_PDF_TARGETS) $(PROMOTE_FIG_TARGETS)

$(stage_dir)/$(DOC_TITLE).pdf: $(DOC_PDF) | $(stage_dir)
	cp -v $< $@

$(stage_dir)/%: $(figures_dir)/% | $(stage_dir)
	cp -v $< $@

# --- Experiments ------------------------------------------------------------
experiments:
	@echo "WARNING: 'make experiments' runs every experiment in src/experiments/makefile."
	@echo "         Many take hours; some take days."
	@echo "         Prefer 'make -C src/experiments <target>' for individual runs."
	$(MAKE) -C src/experiments all

# --- Clean ------------------------------------------------------------------
clean:
	-rm -rf $(build_dir) $(stage_dir)
	@echo "================ Clean Complete ================"

clean-env:
	-rm -rf $(VENV)
	@echo "================ clean-env Complete ================"
