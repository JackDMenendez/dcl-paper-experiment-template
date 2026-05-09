# src/core/

The framework's primitives -- the data structures and operators that
every experiment depends on. Anything that an experiment in
`src/experiments/` would import lives here.

## Documentation convention

Every non-trivial line of code should say what it **is** in the
theory, not just what it does in the program. Name the mathematical
object, cite the paper section / equation where one exists, and state
the correspondence explicitly: "this IS X" when exact, "this
approximates X" in the continuum limit.

When adding new physics code, follow the same pattern:

- Name the mathematical object (e.g. "L = integral of (r x p) . rho dV").
- State what the variable IS, not what you are doing with it.
- Use "IS" for exact correspondences, "approximates" for continuum
  limits.
- Cross-reference the paper section or equation label where one
  exists.

## What goes here

- Core lattice / state primitives.
- Time-evolution operators.
- Constraint enforcement (e.g. the unity / conservation law).

## What does NOT go here

- Experiment scripts (those go in `src/experiments/`).
- Plotting and figure generation (those go in `src/utilities/`).
- One-off analysis scripts.
