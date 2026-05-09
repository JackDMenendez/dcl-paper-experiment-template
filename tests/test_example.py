"""Exemplar test for src/core primitives.

Tests in this directory are *unit tests* for the framework's
primitives -- fast, deterministic, run on every commit.  Larger
PASS/FAIL claims about physics live in `src/experiments/`, not here.

A useful split:

  tests/         milliseconds-to-seconds; correctness of operators
  src/experiments/ seconds-to-days; correctness of physical claims
"""

import numpy as np
import pytest


def test_numpy_smoke():
    """Sanity check: numpy is importable and arithmetic is sane."""
    assert np.array([1, 2, 3]).sum() == 6


def test_seeded_rng_is_deterministic():
    """Two RNGs with the same seed produce identical samples."""
    a = np.random.default_rng(seed=42).standard_normal(100)
    b = np.random.default_rng(seed=42).standard_normal(100)
    np.testing.assert_array_equal(a, b)


@pytest.mark.parametrize("n", [10, 100, 1000])
def test_mean_converges_to_zero(n):
    """Mean of standard normals shrinks as 1/sqrt(n) -- loose bound."""
    samples = np.random.default_rng(seed=0).standard_normal(n)
    assert abs(samples.mean()) < 5.0 / np.sqrt(n)
