"""Tests for 2x2 crossover BE and DDI sample size.

Locks in the fix for the factor-of-2 over-estimation bug (the old code applied
the TOTAL-N formula as a per-sequence count and then doubled it) and verifies
the exact-TOST results against PowerTOST-known values.
"""
import pytest

import crossover_2x2_be as be
import crossover_2x2_ddi as ddi


# --- BE: exact TOST values (PowerTOST) -----------------------------------
@pytest.mark.parametrize(
    "cv,gmr,power,expected_n",
    [
        (25.0, 0.95, 0.80, 28),
        (20.0, 0.95, 0.80, 20),
        (30.0, 0.95, 0.80, 40),
        (25.0, 0.95, 0.90, 38),
    ],
)
def test_be_sample_size(cv, gmr, power, expected_n):
    r = be.calculate_sample_size(intra_cv=cv, gmr=gmr, power=power)
    assert r["n_total"] == expected_n
    assert r["achieved_power"] >= power
    assert r["n_total"] == 2 * r["n_per_group"]


def test_be_no_factor_of_two_regression():
    """Regression guard: CV25/GMR0.95/0.80 must be 28, NOT the buggy 52."""
    r = be.calculate_sample_size(intra_cv=25.0, gmr=0.95, power=0.80)
    assert r["n_total"] == 28
    assert r["n_total"] < 52


def test_be_dropout_adjustment():
    r = be.calculate_sample_size(intra_cv=25.0, gmr=0.95, power=0.80, dropout_rate=0.10)
    # 14 per sequence -> ceil(14/0.9) = 16 per sequence
    assert r["n_per_group_adjusted"] == 16
    assert r["n_total_adjusted"] == 32


def test_be_raises_when_gmr_outside_limits():
    with pytest.raises(ValueError):
        be.calculate_sample_size(intra_cv=25.0, gmr=1.30, power=0.80)


# --- DDI: equivalence uses the same exact TOST engine --------------------
def test_ddi_equivalence_equals_be():
    """DDI no-effect equivalence is the same TOST problem as BE."""
    r_ddi = ddi.calculate_sample_size(
        intra_cv=25.0, expected_gmr=0.95, approach="equivalence", power=0.80
    )
    r_be = be.calculate_sample_size(intra_cv=25.0, gmr=0.95, power=0.80)
    assert r_ddi["n_total"] == r_be["n_total"] == 28


def test_ddi_equivalence_no_factor_of_two_regression():
    r = ddi.calculate_sample_size(
        intra_cv=30.0, expected_gmr=1.05, approach="equivalence", power=0.90
    )
    # Old buggy code doubled an already-total formula (~104). Correct ~52.
    assert r["n_total"] < 80
    assert r["achieved_power"] >= 0.90


def test_ddi_fold_change_runs_and_is_even():
    r = ddi.calculate_sample_size(
        intra_cv=30.0, expected_gmr=1.25, approach="fold_change", power=0.80
    )
    assert r["n_total"] % 2 == 0
    assert r["n_total"] == 2 * r["n_per_group"]


def test_ddi_unknown_approach_raises():
    with pytest.raises(ValueError):
        ddi.calculate_sample_size(intra_cv=30.0, approach="nonsense")
