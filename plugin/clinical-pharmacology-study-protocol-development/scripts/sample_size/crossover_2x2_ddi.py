"""
Sample size calculation for a 2x2 crossover drug-drug interaction (DDI) study.

Design
------
Two-sequence, two-period crossover where subjects receive the substrate alone
and the substrate with an inhibitor/inducer in randomised order.

When to use
-----------
- DDI studies evaluating the effect of a perpetrator drug on a victim drug's PK
- Can use equivalence-based approach (no-effect boundary) or fold-change approach
- Primary endpoints: AUC and Cmax ratios (with vs. without perpetrator)

Approaches
----------
1. **Equivalence (no-effect boundary)**: demonstrate that the 90% CI for the
   GMR falls within pre-specified bounds (e.g. 0.80-1.25).
   Same TOST framework as BE.

2. **Fold-change**: when an interaction IS expected, the study is sized to
   characterise the magnitude of change with adequate precision.  The sample
   size ensures the 90% CI for the GMR is within a desired margin of the
   point estimate.

Reference
---------
FDA Guidance. Clinical Drug Interaction Studies — Cytochrome P450 Enzyme- and
Transporter-Mediated Drug Interactions (2020).
FDA Guidance. In Vitro Drug Interaction Studies (2020).
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
    expected_gmr: float = 1.00,
    approach: str = "equivalence",
    equivalence_limits: tuple[float, float] = (0.80, 1.25),
    precision_margin: float | None = None,
    power: float = 0.80,
    alpha: float = 0.05,
    dropout_rate: float = 0.0,
) -> dict:
    """Calculate sample size for a 2x2 crossover DDI study.

    Parameters
    ----------
    intra_cv : float
        Intra-subject CV (%) for the PK parameter of interest.
    expected_gmr : float
        Expected geometric mean ratio (with perpetrator / without).
        For no interaction, use 1.0; for inhibition, e.g. 1.25.
    approach : str
        "equivalence" — TOST for no-effect boundary (default).
        "fold_change" — precision-based sizing for expected interaction.
    equivalence_limits : tuple of float
        No-effect boundary limits (default 0.80, 1.25).
        Used only when approach="equivalence".
    precision_margin : float, optional
        Desired half-width of the 90% CI on the log scale for the
        fold-change approach.  If None, defaults to ln(1.25) ≈ 0.223.
    power : float
        Desired power.
    alpha : float
        One-sided alpha (for TOST) or alpha/2 for fold-change CI.
    dropout_rate : float
        Expected dropout proportion.

    Returns
    -------
    dict
        Sample size results and parameters.
    """
    sigma_w = _cv_to_sigma_w(intra_cv)

    if approach == "equivalence":
        delta = abs(math.log(expected_gmr))
        theta = math.log(equivalence_limits[1])
        margin = theta - delta
        if margin <= 0:
            raise ValueError(
                f"Expected GMR ({expected_gmr}) exceeds equivalence limits "
                f"{equivalence_limits}. Cannot demonstrate no effect."
            )
        z_alpha = normal_quantile(1.0 - alpha)
        z_beta = normal_quantile(power)
        n_per_seq = math.ceil(
            (z_alpha + z_beta) ** 2 * 2.0 * sigma_w ** 2 / margin ** 2
        )

    elif approach == "fold_change":
        if precision_margin is None:
            precision_margin = math.log(1.25)
        z_alpha = normal_quantile(1.0 - alpha)
        z_beta = normal_quantile(power)
        # Precision-based: ensure 90% CI half-width <= precision_margin
        n_per_seq = math.ceil(
            (z_alpha + z_beta) ** 2 * 2.0 * sigma_w ** 2
            / precision_margin ** 2
        )

    else:
        raise ValueError(f"Unknown approach: {approach!r}")

    n_total = 2 * n_per_seq
    n_per_seq_adj = adjust_for_dropout(n_per_seq, dropout_rate)
    n_total_adj = 2 * n_per_seq_adj

    params = {
        "design": f"2x2 Crossover DDI ({approach})",
        "intra_cv (%)": intra_cv,
        "sigma_w (log-scale)": round(sigma_w, 4),
        "expected_gmr": expected_gmr,
        "approach": approach,
        "equivalence_limits": equivalence_limits if approach == "equivalence" else "N/A",
        "precision_margin (log)": (
            round(precision_margin, 4) if approach == "fold_change" else "N/A"
        ),
        "alpha": alpha,
        "power": power,
        "z_alpha": round(z_alpha, 4),
        "z_beta": round(z_beta, 4),
        "dropout_rate": dropout_rate,
    }

    return {
        "n_per_group": n_per_seq,
        "n_total": n_total,
        "n_per_group_adjusted": n_per_seq_adj,
        "n_total_adjusted": n_total_adj,
        "params": params,
    }


if __name__ == "__main__":
    # Example 1: DDI no-effect boundary (equivalence approach)
    print("Example 1: DDI study — no-effect boundary (equivalence)")
    print("  Intra-subject CV = 30%, Expected GMR = 1.05")
    print("  No-effect boundary = (0.80, 1.25)")
    print("  Alpha = 0.05 (one-sided), Power = 0.90, Dropout = 10%\n")

    result1 = calculate_sample_size(
        intra_cv=30.0,
        expected_gmr=1.05,
        approach="equivalence",
        equivalence_limits=(0.80, 1.25),
        power=0.90,
        alpha=0.05,
        dropout_rate=0.10,
    )
    print_result(
        design=result1["params"]["design"],
        n_per_group=result1["n_per_group"],
        n_total=result1["n_total"],
        params=result1["params"],
        n_per_group_adjusted=result1["n_per_group_adjusted"],
        n_total_adjusted=result1["n_total_adjusted"],
    )

    # Example 2: DDI with expected 1.25-fold increase (fold-change approach)
    print("Example 2: DDI study — fold-change characterisation")
    print("  Intra-subject CV = 30%, Expected GMR = 1.25")
    print("  Precision margin = ln(1.25) ~ 0.223")
    print("  Alpha = 0.05, Power = 0.80, Dropout = 10%\n")

    result2 = calculate_sample_size(
        intra_cv=30.0,
        expected_gmr=1.25,
        approach="fold_change",
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
