"""Tests for FIH starting-dose calculation (MRSD via NOAEL-HED, MABEL).

Validates the body-surface-area conversion factors against the FDA 2005
guidance (Km_human / Km_animal) and the Emax-based MABEL formula.
"""
import math

import pytest

import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fih")
)

import starting_dose_calculation as fih


@pytest.mark.parametrize(
    "noael,species,expected_hed",
    [
        (100.0, "mouse", 8.13),   # 100 / 12.3
        (30.0, "rat", 4.84),      # 30 / 6.2
        (10.0, "dog", 5.56),      # 10 / 1.8
        (10.0, "monkey", 3.23),   # 10 / 3.1
    ],
)
def test_noael_to_hed(noael, species, expected_hed):
    assert fih.noael_to_hed(noael, species) == pytest.approx(expected_hed, abs=0.02)


def test_hed_conversion_factors_match_fda():
    """Factor = Km_human / Km_animal (FDA 2005 Table 1, published rounding)."""
    km_human = fih.KM_VALUES["human"]
    for sp, factor in fih.BSA_CONVERSION_FACTORS.items():
        if sp in ("monkey",):  # alias
            continue
        km = fih.KM_VALUES[sp]
        # The guidance tabulates rounded factors (e.g. dog 1.8 vs 37/20=1.85).
        assert factor == pytest.approx(km_human / km, abs=0.1)


def test_noael_to_hed_unknown_species():
    with pytest.raises(ValueError):
        fih.noael_to_hed(100.0, "elephant")


def test_calculate_mrsd_pipeline():
    r = fih.calculate_mrsd(30.0, "rat", safety_factor=10.0, body_weight_kg=60.0)
    # HED = 30/6.2 = 4.838; /10 = 0.4838 mg/kg; *60 = 29.03 mg
    assert r.hed_mg_kg == pytest.approx(4.84, abs=0.02)
    assert r.mrsd_mg == pytest.approx(29.03, abs=0.05)


def test_mrsd_selects_lower_across_species():
    rat = fih.calculate_mrsd(30.0, "rat")   # HED 4.84 -> MRSD 29.03 mg
    dog = fih.calculate_mrsd(10.0, "dog")   # HED 5.56 -> MRSD 33.33 mg
    # The rat here yields the lower (more conservative) MRSD; practice selects
    # the lowest across the relevant species.
    assert rat.mrsd_mg < dog.mrsd_mg
    assert min(rat.mrsd_mg, dog.mrsd_mg) == rat.mrsd_mg


def test_calculate_mabel():
    r = fih.calculate_mabel(ec50=100.0, target_occupancy=0.10)
    # C = occ * EC50 / (1 - occ) = 0.10 * 100 / 0.90 = 11.11
    assert r.mabel == pytest.approx(11.11, abs=0.02)


def test_mabel_invalid_occupancy():
    with pytest.raises(ValueError):
        fih.calculate_mabel(ec50=100.0, target_occupancy=1.0)
