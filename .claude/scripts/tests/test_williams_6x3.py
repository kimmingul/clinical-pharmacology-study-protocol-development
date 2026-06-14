"""Tests for the Williams 6x3 bidirectional DDI design.

Locks in the co-primary (joint) power fix: sizing each direction to marginal
power 0.80 and taking max(n) does NOT deliver 80% study-level power, because
the study passes only when BOTH directions pass.
"""
import math

import pytest

import williams_6x3_ddi as w


def test_joint_power_inflation():
    r = w.calculate_sample_size(
        cv_x=30.0, expected_gmr_x=1.05,
        cv_y=30.0, expected_gmr_y=1.05,
        approach="equivalence", power=0.80, target_is_joint=True,
    )
    p = r["params"]
    assert p["per_direction_power_used"] == pytest.approx(math.sqrt(0.80), abs=1e-3)
    assert p["joint_power_independence_bound"] == pytest.approx(0.80, abs=1e-3)
    assert p["power_basis"].startswith("joint")


def test_joint_requires_more_than_marginal():
    """Co-primary (joint) target must require >= subjects vs marginal target."""
    common = dict(
        cv_x=30.0, expected_gmr_x=1.05,
        cv_y=30.0, expected_gmr_y=1.05,
        approach="equivalence", power=0.80,
    )
    n_joint = w.calculate_sample_size(target_is_joint=True, **common)["n_total"]
    n_marg = w.calculate_sample_size(target_is_joint=False, **common)["n_total"]
    assert n_joint > n_marg


def test_total_is_multiple_of_six():
    r = w.calculate_sample_size(
        cv_x=20.0, expected_gmr_x=1.0,
        cv_y=50.0, expected_gmr_y=1.0,
        approach="equivalence", power=0.80,
    )
    assert r["n_total"] % 6 == 0
    assert r["n_total"] == 6 * r["n_per_group"]


def test_larger_direction_drives_n():
    """The higher-CV direction should drive the required n."""
    r = w.calculate_sample_size(
        cv_x=20.0, expected_gmr_x=1.0,
        cv_y=50.0, expected_gmr_y=1.0,
        approach="equivalence", power=0.80,
    )
    dx = r["params"]["direction_x"]["n_required"]
    dy = r["params"]["direction_y"]["n_required"]
    assert dy > dx  # CV 50% needs more than CV 20%


def test_detection_approach_runs():
    r = w.calculate_sample_size(
        cv_x=40.0, expected_gmr_x=0.60,
        cv_y=40.0, expected_gmr_y=1.40,
        approach="detection", power=0.80,
    )
    assert r["n_total"] % 6 == 0


def test_invalid_power_raises():
    with pytest.raises(ValueError):
        w.calculate_sample_size(
            cv_x=30.0, expected_gmr_x=1.05,
            cv_y=30.0, expected_gmr_y=1.05,
            power=1.5,
        )
