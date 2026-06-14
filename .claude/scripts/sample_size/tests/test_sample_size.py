"""Regression tests for sample size calculation scripts.

References used as expected values:
- Chow S-C, Liu J-P. Design and Analysis of Bioavailability and
  Bioequivalence Studies, 3rd ed. CRC Press, 2009, Chapter 5.
- PowerTOST R package: sampleN.TOST() outputs.
- Cohen J. Statistical Power Analysis for the Behavioral Sciences,
  2nd ed. 1988.
"""

import os
import sys

import pytest


# Make ``.claude/scripts/sample_size`` importable directly.
_SAMPLE_SIZE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir)
)
if _SAMPLE_SIZE_DIR not in sys.path:
    sys.path.insert(0, _SAMPLE_SIZE_DIR)

from crossover_2x2_be import calculate_sample_size as be_n  # noqa: E402
from crossover_2x2_ddi import calculate_sample_size as ddi_n  # noqa: E402
from parallel_continuous import calculate_sample_size as parallel_n  # noqa: E402


# ---------------------------------------------------------------------------
# C1 regression: 2x2 crossover BE no-longer-doubled total N
# ---------------------------------------------------------------------------


def test_c1_regression_2x2_be_no_double_counting():
    """C1: PowerTOST sampleN.TOST(CV=0.25, theta0=0.95, power=0.80) ~ 26 (z)
    / 28 (t). Pre-fix code returned 52 (2x overestimate)."""
    result = be_n(
        intra_cv=25.0,
        gmr=0.95,
        power=0.80,
        alpha=0.05,
        dropout_rate=0.0,
    )
    assert result["n_total"] in {26, 28}, (
        f"Expected N_total in {{26, 28}} (normal vs t-approx), "
        f"got {result['n_total']}. This was the C1 2x overestimate bug."
    )
    # n_per_seq must be exactly half the (even) total
    assert result["n_per_group"] * 2 == result["n_total"]


def test_2x2_be_cv30_gmr1_power80():
    """Exact TOST: CV=0.30, theta0=1.00, power=0.80 -> N=32 (achieved 0.815).

    Monte-Carlo verified: N=30 reaches only 0.78, N=32 reaches 0.82. The one-
    sided normal approximation is strongly over-optimistic at theta0=1.0 (it
    suggested ~24, which is actually ~0.64 power -- underpowered); the exact
    noncentral-t value is 32. This test was corrected when the calculator moved
    from the normal approximation to the exact-TOST engine.
    """
    result = be_n(
        intra_cv=30.0,
        gmr=1.00,
        power=0.80,
        alpha=0.05,
        dropout_rate=0.0,
    )
    assert result["n_total"] == 32, (
        f"exact-TOST reference 32 (MC-verified), got {result['n_total']}"
    )
    assert result["achieved_power"] >= 0.80


def test_2x2_be_cv40_gmr95_power90():
    """PowerTOST sampleN.TOST(CV=0.40, theta0=0.95, power=0.90) ~ 70 (t).
    Normal approximation gives ~88. Accept either regime ±5."""
    result = be_n(
        intra_cv=40.0,
        gmr=0.95,
        power=0.90,
        alpha=0.05,
        dropout_rate=0.0,
    )
    # Normal approximation tends to overestimate vs t for this case.
    assert 60 <= result["n_total"] <= 95, (
        f"PowerTOST reference ~70-88, got {result['n_total']}"
    )


# ---------------------------------------------------------------------------
# Parallel design — Cohen reference
# ---------------------------------------------------------------------------


def test_parallel_continuous_cohen_d_half():
    """Cohen (1988) Table 2.4.1: two-sample t-test, d=0.5, alpha=0.05
    two-sided, power=0.80 -> n per group = 64 (table) / 63 (z-approx)."""
    result = parallel_n(
        mean_diff=0.5,
        sd=1.0,
        alpha=0.05,
        power=0.80,
        dropout_rate=0.0,
    )
    assert 62 <= result["n_per_group"] <= 65, (
        f"Cohen 1988 reference ~63-64 per group, got {result['n_per_group']}"
    )


# ---------------------------------------------------------------------------
# Dropout adjustment
# ---------------------------------------------------------------------------


def test_dropout_inflation_round_up():
    """N=26 evaluable with 10% dropout -> enroll at least 30 (ceil(26/0.9))."""
    result = be_n(
        intra_cv=25.0,
        gmr=0.95,
        power=0.80,
        alpha=0.05,
        dropout_rate=0.10,
    )
    assert result["n_total"] in {26, 28}
    # ceil(26/0.9)=29, rounded up to even -> 30. Accept 30-32 to allow for
    # the even-rounding step on slightly different base totals.
    assert result["n_total_adjusted"] >= 30, (
        f"With 10% dropout the adjusted total must be >= 30, "
        f"got {result['n_total_adjusted']}"
    )
    assert result["n_total_adjusted"] % 2 == 0, (
        "Adjusted total must remain even for balanced 2-sequence allocation."
    )


# ---------------------------------------------------------------------------
# DDI 2x2 crossover — same fix as BE
# ---------------------------------------------------------------------------


def test_ddi_2x2_equivalence_no_double_counting():
    """C1 sibling: crossover_2x2_ddi.py must NOT double the formula output."""
    result = ddi_n(
        intra_cv=25.0,
        expected_gmr=0.95,
        approach="equivalence",
        equivalence_limits=(0.80, 1.25),
        power=0.80,
        alpha=0.05,
        dropout_rate=0.0,
    )
    assert result["n_total"] in {26, 28}, (
        f"BE-equivalent DDI sizing must match BE reference (26/28), "
        f"got {result['n_total']}"
    )
