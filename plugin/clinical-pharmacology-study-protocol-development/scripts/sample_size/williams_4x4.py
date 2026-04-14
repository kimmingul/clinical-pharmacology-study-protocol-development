"""
Sample size calculation for a Williams 4x4 (4-sequence, 4-period) crossover design.

Design
------
Four sequences, four periods, balanced for first-order carry-over.
The Williams design is a special type of Latin square that balances
carry-over effects.

Typical sequences (for treatments A, B, C, D):
    Seq 1: A B D C
    Seq 2: B C A D
    Seq 3: C D B A
    Seq 4: D A C B

When to use
-----------
- Comparing 4 treatments (e.g. 3 dose levels of a perpetrator + placebo
  in a DDI study)
- Multi-dose DDI studies
- Studies requiring all pairwise comparisons among 4 treatments
- When carry-over effects need to be balanced

Formula
-------
For a comparison of any two treatments in a Williams 4x4:
    n_per_seq = (z_alpha + z_beta)^2 * 2 * sigma_w^2 / (k * margin^2)

where k is the design efficiency factor.  For a Williams square with
t treatments and p periods (t = p = 4), the efficiency for pairwise
comparison is improved compared to a simple 2x2 because each subject
contributes data under multiple treatments.  However, the per-comparison
variance reduction factor depends on specific contrasts.

For the simple case of comparing two specific treatments:
    Each treatment appears once per subject across 4 periods.
    The effective n for a pairwise comparison: n_per_seq subjects per
    sequence, 4 sequences, each comparison uses 2 of 4 periods per subject.

Reference
---------
Williams EJ. Experimental designs balanced for the estimation of residual
effects of treatments. Australian J Sci Res A 1949; 2:149-168.
Jones B, Kenward MG. Design and Analysis of Cross-Over Trials, 3rd ed.
CRC Press, 2014, Chapter 4.
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
    equivalence_limits: tuple[float, float] = (0.80, 1.25),
    power: float = 0.80,
    alpha: float = 0.05,
    gmr: float = 1.00,
    dropout_rate: float = 0.0,
    n_treatments: int = 4,
) -> dict:
    """Calculate sample size for a Williams 4x4 crossover design.

    The calculation is for a pairwise comparison of two specific treatments
    within the Williams square (e.g. test vs. reference in a 4-treatment DDI).

    Parameters
    ----------
    intra_cv : float
        Intra-subject CV (%) for the primary PK parameter.
    equivalence_limits : tuple of float
        Equivalence limits on the original scale (default 0.80-1.25).
    power : float
        Desired power (default 0.80).
    alpha : float
        One-sided significance level for TOST (default 0.05).
    gmr : float
        Expected geometric mean ratio for the comparison of interest.
    dropout_rate : float
        Expected dropout proportion.
    n_treatments : int
        Number of treatments in the Williams design (default 4).

    Returns
    -------
    dict
        Sample size results and parameters.
    """
    sigma_w = _cv_to_sigma_w(intra_cv)
    delta = abs(math.log(gmr))
    theta = math.log(equivalence_limits[1])

    margin = theta - delta
    if margin <= 0:
        raise ValueError(
            f"Expected GMR ({gmr}) is outside equivalence limits "
            f"{equivalence_limits}. No finite sample size exists."
        )

    z_alpha = normal_quantile(1.0 - alpha)
    z_beta = normal_quantile(power)

    n_sequences = n_treatments  # 4 sequences for Williams 4x4

    # In a Williams 4x4, each subject receives all 4 treatments.
    # For a pairwise comparison (TOST), the within-subject variance
    # applies and the effective design factor for the paired difference
    # of two treatments is 2*sigma_w^2/n_total (same as 2x2 crossover
    # per subject, but total subjects are spread across 4 sequences).
    # n_total needed for the pairwise comparison:
    n_total_evaluable = math.ceil(
        2.0 * (z_alpha + z_beta) ** 2 * sigma_w ** 2 / margin ** 2
    )

    # Ensure total is divisible by number of sequences for balance
    n_per_seq = math.ceil(n_total_evaluable / n_sequences)
    n_total = n_per_seq * n_sequences

    n_per_seq_adj = adjust_for_dropout(n_per_seq, dropout_rate)
    n_total_adj = n_per_seq_adj * n_sequences

    params = {
        "design": f"Williams {n_treatments}x{n_treatments} Crossover",
        "n_treatments": n_treatments,
        "n_sequences": n_sequences,
        "intra_cv (%)": intra_cv,
        "sigma_w (log-scale)": round(sigma_w, 4),
        "equivalence_limits": equivalence_limits,
        "gmr": gmr,
        "delta (|ln(GMR)|)": round(delta, 4),
        "alpha (one-sided)": alpha,
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
    # Example: DDI study with 3 dose levels + placebo (4 treatments)
    print("Example: DDI study with Williams 4x4 design")
    print("  4 treatments: Substrate alone, Sub + Low Inhibitor,")
    print("                Sub + High Inhibitor, Sub + Placebo")
    print("  Intra-subject CV = 28%, GMR = 0.95 (for key comparison)")
    print("  Equivalence limits = (0.80, 1.25)")
    print("  Alpha = 0.05 (one-sided), Power = 0.80, Dropout = 15%\n")

    result = calculate_sample_size(
        intra_cv=28.0,
        gmr=0.95,
        power=0.80,
        alpha=0.05,
        dropout_rate=0.15,
    )
    print_result(
        design=result["params"]["design"],
        n_per_group=result["n_per_group"],
        n_total=result["n_total"],
        params=result["params"],
        n_per_group_adjusted=result["n_per_group_adjusted"],
        n_total_adjusted=result["n_total_adjusted"],
    )

    # Sensitivity with higher power
    print("\n--- Sensitivity: Power = 0.90, CV = 35% ---")
    result2 = calculate_sample_size(
        intra_cv=35.0,
        gmr=0.95,
        power=0.90,
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
