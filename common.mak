# Shared make variables. Included from the root makefile (and, in the
# full-stack template, from src/experiments/makefile via RELATIVE_PATH=../../).

# Get the absolute path of the current Makefile
MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR := $(dir $(MKFILE_PATH))

# Virtual environment (used by the full-stack template; harmless here).
VENV := $(RELATIVE_PATH).venv
ARGS ?= -u
PYTHON = "$(VENV)/Scripts/python" $(ARGS)
PIP = "$(VENV)/Scripts/pip.exe"

# Build directories.
build_dir := $(RELATIVE_PATH)build
stage_dir := $(RELATIVE_PATH)stage
data_dir := $(RELATIVE_PATH)data
figures_dir := $(RELATIVE_PATH)figures

# pdflatex flags: bail on first error, give file:line errors.
PDFLATEX = pdflatex -interaction=nonstopmode -halt-on-error -file-line-error
BIBTEX = bibtex

# For substituting spaces in file names, if needed.
nullstring :=
space := $(nullstring) $(nullstring)
