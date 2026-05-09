# src/utilities/

Helper scripts that support the paper but are not themselves
experiments. Things that produce figures, validate symbolic
identities, or set up calibration constants.

Typical contents:

- Figure generators that read from `data/` and write to
  `paper/figures/` or the repo-root `figures/` directory.
- Symbolic / sympy verification scripts (e.g. confirming an algebraic
  identity holds in the framework).
- Calibration scripts that derive constants used by experiments.

A utility script should be reproducible (deterministic seed,
documented dependencies) but does not need a PASS/FAIL contract --
it is a build step, not a claim. If a utility is exercising a
falsifiable claim, promote it to `src/experiments/`.
