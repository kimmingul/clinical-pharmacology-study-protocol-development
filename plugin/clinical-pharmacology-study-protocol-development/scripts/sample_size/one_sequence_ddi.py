"""
Sample size calculation for a one-sequence (fixed-order) DDI design.

Design
------
All subjects receive the same treatment sequence:
    Period 1: Substrate alone (baseline PK)
    Washout
    Period 2: Substrate + Inhibitor/Inducer (DDI PK)

This is NOT randomised — the order is fixed because the perpetrator drug
may have a long washout or irreversible mechanism (e.g. enzyme induction).

When to use
-----------
- DDI studies where the perpetrator has a long half-life or irreversible effect
- Enzyme induction studies (inducer effect takes days to develop and dissipate)
- When a crossover is impractical due to carry-over risk
- Most common DDI design in practice

Formula
-------
Same TOST framework as crossover, but uses a one-sample paired comparison.
Each subject serves as their own control.

    n = (z_alpha + z_beta)^2 * sigma_w^2 / margin^2

where sigma_w is the within-subject variability of the substrate PK parameter
and margin = ln(no_effect_boundary_upper) - |ln(expected_fold_change)|.

For enzyme inhibition/induction DDI:
    expected_fold_change = AUC(with perpetrator) / AUC(without)
    no_effect_boundary = (0.80, 1.25) by default

Reference
---------
FDA Guidance. Clinical Drug Interaction Studies (2020).
Huang S-M et al. New Era in Drug Interaction Evaluation.
Clin Pharmacol Ther 2008; 83:435-442.
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


def _cv_to_sigma_w(cv_pct: float) -> float:
    """Convert intra-subject CV (%) to within-subject SD on the log scale."""
    cv = cv_pct / 100.0
    return math.sqrt(math.log(1.0 + cv ** 2))


def calculate_sample_size(
    *,
    intra_cv: float,
    expected_fold_change: float = 1.0,
    no_effect_boundary: tuple[float, float] = (0.80, 1.25),
    power: float = 0.80,
    alpha: float = 0.05,
    n_periods: int = 2,
    dropout_rate: float = 0.0,
) -> dict:
    """Calculate sample size for a one-sequence DDI study.

    Parameters
    ----------
    intra_cv : float
        Intra-subject CV (%) for the substrate PK parameter.
    expected_fold_change : float
        Expected ratio of AUC (with perpetrator / without).
        1.0 = no interaction; >1.0 = inhibition; <1.0 = induction.
    no_effect_boundary : tuple of float
        Limits for the no-effect conclusion (default 0.80-1.25).
    power : float
        Desired power (default 0.80).
    alpha : float
        One-sided alpha for TOST (default 0.05).
    n_periods : int
        Number of periods (default 2).  Typically 2 for a standard
        one-sequence DDI (substrate alone, then substrate + perpetrator).
        Some designs may have 3 periods (e.g. pre-dose, co-admin, post-washout).
    dropout_rate : float
        Expected dropout proportion.

    Returns
    -------
    dict
        Sample size results and parameters.
    """
    sigma_w = _cv_to_sigma_w(intra_cv)
    delta = abs(math.log(expected_fold_change))
    theta = math.log(no_effect_boundary[1])

    margin = theta - delta
    if margin <= 0:
        raise ValueError(
            f"Expected fold change ({expected_fold_change}) exceeds the "
            f"no-effect boundary {no_effect_boundary}. "
            f"The study cannot demonstrate no effect."
        )

    z_alpha = normal_quantile(1.0 - alpha)
    z_beta = normal_quantile(power)

    # One-sequence design: each subject provides a paired difference.
    # The variance of the difference is 2 * sigma_w^2 / n (for 2 periods).
    # For n_periods > 2, the variance per comparison decreases.
    variance_factor = 2.0 / n_periods  # each period provides one observation
    # Standard formula for paired design:
    n_total = math.ceil(
        (z_alpha + z_beta) ** 2 * 2.0 * sigma_w ** 2 / margin ** 2
    )

    # No "groups" — all subjects receive the same sequence
    n_per_group = n_total  # single group

    n_total_adj = adjust_for_dropout(n_total, dropout_rate)
    n_per_group_adj = n_total_adj

    params = {
        "design": "One-sequence (fixed-order) DDI",
        "intra_cv (%)": intra_cv,
        "sigma_w (log-scale)": round(sigma_w, 4),
        "expected_fold_change": expected_fold_change,
        "delta (|ln(fold change)|)": round(delta, 4),
        "no_effect_boundary": no_effect_boundary,
        "theta (log upper limit)": round(theta, 4),
        "margin (theta - delta)": round(margin, 4),
        "n_periods": n_periods,
        "alpha (one-sided)": alpha,
        "power": power,
        "z_alpha": round(z_alpha, 4),
        "z_beta": round(z_beta, 4),
        "dropout_rate": dropout_rate,
    }

    return {
        "n_per_group": n_per_group,
        "n_total": n_total,
        "n_per_group_adjusted": n_per_group_adj,
        "n_total_adjusted": n_total_adj,
        "params": params,
    }


if __name__ == "__main__":
    # Example: CYP3A4 inhibition DDI study
    print("Example: One-sequence DDI study (CYP3A4 enzyme inhibition)")
    print("  Design: Midazolam alone -> Washout -> Midazolam + Itraconazole")
    print("  Intra-subject CV = 25%")
    print("  Expected fold change = 1.05 (near no effect for this example)")
    print("  No-effect boundary = (0.80, 1.25)")
    print("  Alpha = 0.05 (one-sided), Power = 0.90, Dropout = 10%\n")

    result = calculate_sample_size(
        intra_cv=25.0,
        expected_fold_change=1.05,
        no_effect_boundary=(0.80, 1.25),
        power=0.90,
        alpha=0.05,
        n_periods=2,
        dropout_rate=0.10,
    )
    print_result(
        design=result["params"]["design"],
        n_per_group=result["n_per_group"],
        n_total=result["n_total"],
        params=result["params"],
        n_per_group_adjusted=result["n_per_group_adjusted"],
        n_total_adjusted=result["n_total_adjusted"],
    )

    # Example 2: Induction DDI (expected AUC decrease)
    print("\n--- Example 2: Enzyme induction (AUC decrease expected) ---")
    print("  Expected fold change = 0.85 (15% decrease in AUC)")
    print("  CV = 30%, Power = 0.80\n")

    result2 = calculate_sample_size(
        intra_cv=30.0,
        expected_fold_change=0.85,
        no_effect_boundary=(0.80, 1.25),
        power=0.80,
        alpha=0.05,
        dropout_rate=0.10,
    )
    print_result(
        design=result2["params"]["design"],
        n_per_group=result2["n_per_group"],
        n_total=result2["n_total"],
        params=result2["params"],
        n_per_group_adjusted=result2["n_per_group_adjusted"],
        n_total_adjusted=result2["n_total_adjusted"],
    )
