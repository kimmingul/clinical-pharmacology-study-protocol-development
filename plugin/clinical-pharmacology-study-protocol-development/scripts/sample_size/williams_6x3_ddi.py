"""
Sample size calculation for a Williams 6x3 (6-sequence, 3-period) crossover
design for bidirectional DDI evaluation.

Design
------
Six sequences, three periods. Three treatments — the full Williams design for
3 treatments uses all 3! = 6 sequences so that every treatment is followed
by every other treatment an equal number of times (first-order carry-over
balance).

Typical 3 treatments for a bidirectional DDI between drugs X and Y:
    A = X alone (reference for X)
    B = Y alone (reference for Y)
    C = X + Y together (test for both directions)

Six sequences (all 3! permutations):
    Seq 1: A B C
    Seq 2: A C B
    Seq 3: B A C
    Seq 4: B C A
    Seq 5: C A B
    Seq 6: C B A

When to use
-----------
- **Bidirectional DDI** where both X and Y may affect each other's PK
  (e.g. both are CYP substrates and each has inhibition/induction potential
  for the other's metabolism).
- A single crossover trial evaluating both directions simultaneously:
    * Direction 1 (X's PK):  A vs C  (X alone vs X+Y)
    * Direction 2 (Y's PK):  B vs C  (Y alone vs X+Y)
- Requires balanced carry-over (Williams structure) because 3 treatments
  with non-trivial carry-over risk (especially irreversible CYP inhibitors
  like omeprazole).

Statistical framework — Intersection-Union Test (IUT)
-----------------------------------------------------
Both directions are 1차(1º) endpoints.  Equivalence (no-effect boundary) is
claimed only when BOTH directions pass 90% CI ⊂ (0.80, 1.25).

Type I error (size): Under IUT the family-wise error rate is controlled at
alpha WITHOUT adjustment, because a false equivalence claim requires BOTH
component nulls to be rejected; P(reject all) ≤ P(reject any one true null)
≤ α.  No independence assumption is needed.  No Bonferroni correction.

Power (the opposite story — DO NOT conflate with the size result above):
Because the study succeeds only when BOTH directions pass, the JOINT power is
P(pass_x AND pass_y).  If each direction has marginal power p and the two
tests were independent, the joint power would be p² (e.g. 0.80 × 0.80 = 0.64,
NOT 0.80).  Sizing each direction to marginal power 0.80 and taking the larger
n therefore does NOT deliver 80% study-level power.  To target a joint power
γ we inflate the per-direction marginal power.  Under the independence (worst-
case) bound the required marginal power is √γ; the positive within-subject
correlation between the two contrasts (they share the combination arm C) makes
the true joint power higher than this bound, so √γ is conservative.  The exact
joint power requires modelling that correlation (and finite-sample noncentral-t)
— ideally by simulation.  This module reports BOTH the marginal and the
independence-bound joint power so the assumption is explicit.

Formula (Williams 3-treatment, pairwise comparison)
---------------------------------------------------
For each direction, the within-subject variance applies to the paired
comparison of two specific treatments among the 3 in the Williams square.
With 3 treatments and 6 balanced sequences:
    n_total = ⌈ 2 · σ_w² · (z_α + z_β)² / margin² ⌉
    margin  = ln(upper_bound) − |ln(GMR_expected)|   (equivalence)
              or |ln(GMR_expected)|                    (DDI detection)

The total is then rounded up to the nearest multiple of 6 so each sequence
has an equal number of subjects (balance).

Reference
---------
- Williams EJ. Experimental designs balanced for the estimation of residual
  effects of treatments. Australian J Sci Res A 1949; 2:149–168.
- Jones B, Kenward MG. Design and Analysis of Cross-Over Trials, 3rd ed.
  CRC Press, 2014, Chapter 4 (Williams designs).
- FDA Clinical Drug Interaction Studies Guidance (2020) — bidirectional DDI
  considerations.
- ICH M12 Drug Interaction Studies (2024) — two-way evaluation when both
  drugs can act as perpetrator and victim.
"""

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.power_analysis import (
    normal_quantile,
    adjust_for_dropout,
    print_result,
)


N_SEQUENCES = 6  # Full Williams design for 3 treatments


def _cv_to_sigma_w(cv_pct: float) -> float:
    """Convert intra-subject CV (%) to within-subject SD on the log scale."""
    cv = cv_pct / 100.0
    return math.sqrt(math.log(1.0 + cv ** 2))


def _n_one_direction(
    *,
    sigma_w: float,
    expected_gmr: float,
    approach: str,
    equivalence_limits: tuple[float, float],
    precision_margin: float | None,
    z_alpha: float,
    z_beta: float,
) -> tuple[int, float]:
    """Return (n_total, margin) for a single direction of the DDI."""
    if approach == "equivalence":
        delta = abs(math.log(expected_gmr))
        theta = math.log(equivalence_limits[1])
        margin = theta - delta
        if margin <= 0:
            raise ValueError(
                f"Expected GMR {expected_gmr} is outside equivalence limits "
                f"{equivalence_limits}. Use approach='detection' instead."
            )
    elif approach == "detection":
        # DDI detection: test H0: GMR=1 vs H1: GMR=expected_gmr.
        margin = abs(math.log(expected_gmr))
        if margin == 0:
            raise ValueError(
                "Detection approach requires expected_gmr != 1.0."
            )
    elif approach == "fold_change":
        margin = (
            math.log(1.25) if precision_margin is None else precision_margin
        )
    else:
        raise ValueError(f"Unknown approach: {approach!r}")

    n_total = math.ceil(
        2.0 * sigma_w ** 2 * (z_alpha + z_beta) ** 2 / margin ** 2
    )
    return n_total, margin


def calculate_sample_size(
    *,
    # Direction 1 — effect on drug X's PK
    cv_x: float,
    expected_gmr_x: float,
    # Direction 2 — effect on drug Y's PK
    cv_y: float,
    expected_gmr_y: float,
    # Common
    approach: str = "equivalence",
    equivalence_limits: tuple[float, float] = (0.80, 1.25),
    precision_margin: float | None = None,
    power: float = 0.80,
    target_is_joint: bool = True,
    alpha: float = 0.05,
    dropout_rate: float = 0.0,
) -> dict:
    """Sample size for bidirectional DDI using Williams 6x3 design.

    Computes the required n for each direction independently and returns
    the MAXIMUM (so that both directions meet the target power; IUT
    preserves family-wise α without adjustment).  Total n is rounded up
    to the nearest multiple of 6 for sequence balance.

    Parameters
    ----------
    cv_x, cv_y : float
        Intra-subject CV (%) for the PK parameter of drug X and drug Y.
    expected_gmr_x, expected_gmr_y : float
        Expected geometric mean ratio for each direction.
        * equivalence approach: values near 1.0 (demonstrating no DDI).
        * detection approach: values away from 1.0 (quantifying DDI).
    approach : str
        "equivalence" (TOST, 90% CI ⊂ (0.80, 1.25)),
        "detection"   (one-sided paired test against GMR=1),
        "fold_change" (precision of the 90% CI half-width).
    equivalence_limits : tuple of float
        No-effect boundary when approach='equivalence'.
    precision_margin : float, optional
        Log-scale half-width target for 'fold_change'.
    power : float
        Desired power.  When ``target_is_joint=True`` (default) this is the
        STUDY-LEVEL joint power (probability BOTH directions pass); the per-
        direction marginal power is set to √power as an independence-bound
        (conservative) target.  When ``target_is_joint=False`` this is the
        per-direction marginal power (legacy behaviour — does NOT guarantee
        study-level power for the co-primary design).
    target_is_joint : bool
        If True, treat ``power`` as the joint (co-primary) target and inflate
        the per-direction power to √power.  See the module docstring "Power".
    alpha : float
        One-sided alpha for each direction.  No Bonferroni correction is
        needed (IUT controls size without adjustment).
    dropout_rate : float
        Expected dropout proportion.

    Returns
    -------
    dict
        Sample size results with per-direction details and the final
        (larger) n for the study.
    """
    sigma_x = _cv_to_sigma_w(cv_x)
    sigma_y = _cv_to_sigma_w(cv_y)

    # Co-primary power: the study passes only if BOTH directions pass.
    # Treating `power` as the JOINT target, the per-direction marginal power
    # under the independence (worst-case) bound is sqrt(power). Positive within-
    # subject correlation between the two contrasts makes the true joint power
    # higher, so this is conservative. See the module docstring "Power".
    if not (0.0 < power < 1.0):
        raise ValueError(f"power must be in (0, 1), got {power}")
    per_direction_power = math.sqrt(power) if target_is_joint else power

    z_alpha = normal_quantile(1.0 - alpha)
    z_beta = normal_quantile(per_direction_power)

    n_x, margin_x = _n_one_direction(
        sigma_w=sigma_x,
        expected_gmr=expected_gmr_x,
        approach=approach,
        equivalence_limits=equivalence_limits,
        precision_margin=precision_margin,
        z_alpha=z_alpha,
        z_beta=z_beta,
    )
    n_y, margin_y = _n_one_direction(
        sigma_w=sigma_y,
        expected_gmr=expected_gmr_y,
        approach=approach,
        equivalence_limits=equivalence_limits,
        precision_margin=precision_margin,
        z_alpha=z_alpha,
        z_beta=z_beta,
    )

    # Larger of the two directions drives the study
    n_raw = max(n_x, n_y)

    # Round up to the nearest multiple of 6 for Williams sequence balance
    n_total = math.ceil(n_raw / N_SEQUENCES) * N_SEQUENCES
    n_per_seq = n_total // N_SEQUENCES

    n_per_seq_adj = adjust_for_dropout(n_per_seq, dropout_rate)
    n_total_adj = n_per_seq_adj * N_SEQUENCES

    params = {
        "design": "Williams 6x3 Crossover (bidirectional DDI)",
        "n_sequences": N_SEQUENCES,
        "n_periods": 3,
        "treatments": "A=X alone, B=Y alone, C=X+Y",
        "approach": approach,
        "equivalence_limits": (
            equivalence_limits if approach == "equivalence" else "N/A"
        ),
        "precision_margin (log)": (
            round(precision_margin, 4)
            if approach == "fold_change" and precision_margin is not None
            else "N/A"
        ),
        "alpha (one-sided)": alpha,
        "power_requested": power,
        "power_basis": (
            "joint (study-level)" if target_is_joint
            else "per-direction (marginal)"
        ),
        "per_direction_power_used": round(per_direction_power, 4),
        "joint_power_independence_bound": round(per_direction_power ** 2, 4),
        "z_alpha": round(z_alpha, 4),
        "z_beta": round(z_beta, 4),
        "dropout_rate": dropout_rate,
        "direction_x": {
            "cv (%)": cv_x,
            "sigma_w": round(sigma_x, 4),
            "expected_gmr": expected_gmr_x,
            "margin (log)": round(margin_x, 4),
            "n_required": n_x,
        },
        "direction_y": {
            "cv (%)": cv_y,
            "sigma_w": round(sigma_y, 4),
            "expected_gmr": expected_gmr_y,
            "margin (log)": round(margin_y, 4),
            "n_required": n_y,
        },
        "multiplicity": (
            "IUT controls Type I error without α adjustment. Power is the "
            "co-primary JOINT power; per-direction power inflated to √(target) "
            "under the independence bound (conservative — true within-subject "
            "correlation raises joint power above this bound)."
        ),
    }

    return {
        "n_per_group": n_per_seq,          # per sequence
        "n_total": n_total,                # across 6 sequences
        "n_per_group_adjusted": n_per_seq_adj,
        "n_total_adjusted": n_total_adj,
        "params": params,
    }


if __name__ == "__main__":
    # Example 1: symmetric bidirectional DDI (both drugs affect each other similarly)
    print("Example 1: Bidirectional DDI, symmetric (equivalence)")
    print("  Drugs X and Y both CYP substrates with mutual inhibition potential")
    print("  Intra-subject CV (X) = 30%, Intra-subject CV (Y) = 30%")
    print("  Expected GMR (X) = 1.05, Expected GMR (Y) = 1.05")
    print("  No-effect boundary = (0.80, 1.25)")
    print("  Alpha = 0.05 (one-sided), Power = 0.80, Dropout = 15%\n")

    result1 = calculate_sample_size(
        cv_x=30.0, expected_gmr_x=1.05,
        cv_y=30.0, expected_gmr_y=1.05,
        approach="equivalence",
        equivalence_limits=(0.80, 1.25),
        power=0.80,
        alpha=0.05,
        dropout_rate=0.15,
    )
    print_result(
        design=result1["params"]["design"],
        n_per_group=result1["n_per_group"],
        n_total=result1["n_total"],
        params=result1["params"],
        n_per_group_adjusted=result1["n_per_group_adjusted"],
        n_total_adjusted=result1["n_total_adjusted"],
    )

    # Example 2: asymmetric bidirectional DDI — one direction has higher CV
    print("\nExample 2: Bidirectional DDI, asymmetric variability (equivalence)")
    print("  Drug X has low CV (20%), Drug Y has high CV (50%)")
    print("  Expected GMR both = 1.0 (no interaction expected)")
    print("  Power = 0.80, Alpha = 0.05, Dropout = 15%\n")

    result2 = calculate_sample_size(
        cv_x=20.0, expected_gmr_x=1.00,
        cv_y=50.0, expected_gmr_y=1.00,
        approach="equivalence",
        power=0.80,
        alpha=0.05,
        dropout_rate=0.15,
    )
    print_result(
        design=result2["params"]["design"],
        n_per_group=result2["n_per_group"],
        n_total=result2["n_total"],
        params=result2["params"],
        n_per_group_adjusted=result2["n_per_group_adjusted"],
        n_total_adjusted=result2["n_total_adjusted"],
    )

    # Example 3: detection mode — quantifying known bidirectional interaction
    print("\nExample 3: Bidirectional DDI, detection (quantify known interaction)")
    print("  Direction X: expected GMR 0.60 (40% decrease)")
    print("  Direction Y: expected GMR 1.40 (40% increase)")
    print("  Both CV = 40%")
    print("  Power = 0.80, Alpha = 0.05, Dropout = 15%\n")

    result3 = calculate_sample_size(
        cv_x=40.0, expected_gmr_x=0.60,
        cv_y=40.0, expected_gmr_y=1.40,
        approach="detection",
        power=0.80,
        alpha=0.05,
        dropout_rate=0.15,
    )
    print_result(
        design=result3["params"]["design"],
        n_per_group=result3["n_per_group"],
        n_total=result3["n_total"],
        params=result3["params"],
        n_per_group_adjusted=result3["n_per_group_adjusted"],
        n_total_adjusted=result3["n_total_adjusted"],
    )
