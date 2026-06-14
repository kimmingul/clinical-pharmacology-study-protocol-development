"""Tests for replicate-crossover RSABE sample size.

Locks in the fix for the scaled-limit formula: the widened log-scale limit is
(ln(1.25)/sigma_0) * sigma_w, NOT sigma_0 * sigma_w. The earlier code under-
stated the margin by a factor of ln(1.25)/sigma_0^2 (= 3.57 for FDA), producing
absurdly large sample sizes.
"""
import math
import warnings

import pytest

import replicate_crossover_be as rep


def _sigma_w(cv_pct):
    return math.sqrt(math.log(1.0 + (cv_pct / 100.0) ** 2))


def test_rsabe_emits_not_validated_warning():
    with pytest.warns(RuntimeWarning, match="NOT validated"):
        rep.calculate_sample_size(
            intra_cv=45.0, design_type="2x4", gmr=0.95, power=0.90,
            use_rsabe=True, regulatory_constant=0.25,
        )


def test_rsabe_scaled_margin_uses_correct_factor():
    """effective_margin must use k = ln(1.25)/sigma_0 = 0.8926 (FDA), not 0.25."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        r = rep.calculate_sample_size(
            intra_cv=45.0, design_type="2x4", gmr=0.95, power=0.90,
            use_rsabe=True, regulatory_constant=0.25,
        )
    sw = _sigma_w(45.0)
    k = math.log(1.25) / 0.25
    expected_margin = k * sw - abs(math.log(0.95))
    assert r["params"]["effective_margin (log)"] == pytest.approx(expected_margin, abs=1e-3)
    # The buggy value would have been 0.25*sw - delta ~ 0.056
    assert r["params"]["effective_margin (log)"] > 0.20


def test_rsabe_no_explosion_regression():
    """Corrected RSABE for a HVD must be a realistic size, not the buggy ~1000."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        r = rep.calculate_sample_size(
            intra_cv=45.0, design_type="2x4", gmr=0.95, power=0.90,
            use_rsabe=True, regulatory_constant=0.25,
        )
    assert 12 <= r["n_total"] <= 60


def test_standard_replicate_runs():
    r = rep.calculate_sample_size(
        intra_cv=35.0, design_type="2x3", gmr=1.00, power=0.80, use_rsabe=False,
    )
    assert r["n_total"] > 0
    assert "Standard" in r["params"]["method"]


def test_invalid_design_type_raises():
    with pytest.raises(ValueError):
        rep.calculate_sample_size(intra_cv=35.0, design_type="2x2")
