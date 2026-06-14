"""Unit tests for utils.power_analysis (shared statistical helpers)."""
import math

import pytest

from utils.power_analysis import (
    normal_quantile,
    t_quantile,
    adjust_for_dropout,
    tost_power_2x2,
    solve_n_2x2_tost,
)


def _sigma_w(cv_pct: float) -> float:
    return math.sqrt(math.log(1.0 + (cv_pct / 100.0) ** 2))


def test_normal_quantile():
    assert round(normal_quantile(0.975), 2) == 1.96
    assert round(normal_quantile(0.80), 4) == 0.8416


def test_t_quantile():
    assert round(t_quantile(20, 0.975), 3) == 2.086


@pytest.mark.parametrize(
    "n,rate,expected",
    [(24, 0.10, 27), (24, 0.0, 24), (10, 0.20, 13)],
)
def test_adjust_for_dropout(n, rate, expected):
    assert adjust_for_dropout(n, rate) == expected


def test_adjust_for_dropout_invalid():
    with pytest.raises(ValueError):
        adjust_for_dropout(10, 1.0)


# --- Exact TOST power, validated against the PowerTOST package -------------
@pytest.mark.parametrize(
    "cv,gmr,n_total,expected_power",
    [
        (25.0, 0.95, 28, 0.807),
        (20.0, 0.95, 20, 0.835),
        (30.0, 0.95, 40, 0.816),
    ],
)
def test_tost_power_matches_powertost(cv, gmr, n_total, expected_power):
    p = tost_power_2x2(n_total, _sigma_w(cv), gmr)
    assert p == pytest.approx(expected_power, abs=0.005)


def test_tost_power_monotonic_in_n():
    sw = _sigma_w(25.0)
    assert tost_power_2x2(24, sw, 0.95) < tost_power_2x2(28, sw, 0.95)


@pytest.mark.parametrize(
    "cv,gmr,power,expected_n",
    [
        (25.0, 0.95, 0.80, 28),  # textbook PowerTOST value
        (20.0, 0.95, 0.80, 20),
        (30.0, 0.95, 0.80, 40),
        (25.0, 0.95, 0.90, 38),
    ],
)
def test_solve_n_matches_powertost(cv, gmr, power, expected_n):
    n, achieved = solve_n_2x2_tost(_sigma_w(cv), gmr, power)
    assert n == expected_n
    assert achieved >= power


def test_solve_n_is_minimal():
    """The returned N must meet power, but N-2 must not (true minimum)."""
    sw = _sigma_w(25.0)
    n, _ = solve_n_2x2_tost(sw, 0.95, 0.80)
    assert tost_power_2x2(n, sw, 0.95) >= 0.80
    assert tost_power_2x2(n - 2, sw, 0.95) < 0.80


def test_solve_n_raises_when_gmr_outside_limits():
    with pytest.raises(ValueError):
        solve_n_2x2_tost(_sigma_w(25.0), 1.30, 0.80)
