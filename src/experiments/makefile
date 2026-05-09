# src/experiments/makefile -- per-experiment targets.
#
# Invoked from the repo root either via:
#   make experiments              (runs every target in EXPERIMENTS, slow)
#   make -C src/experiments exp_00_example
#
# Add a new experiment by:
#   1. dropping exp_NN_<name>.py and exp_NN_<name>.md alongside this file
#   2. appending the target name to EXPERIMENTS
#   3. adding a target rule below

RELATIVE_PATH := ../../
include $(RELATIVE_PATH)common.mak

EXPERIMENTS := exp_00_example

.PHONY: all $(EXPERIMENTS)

all: $(EXPERIMENTS)

# --- Individual experiments -------------------------------------------------
exp_00_example:
	$(PYTHON) exp_00_example.py
