"""
Sample size calculation for a 2x2 crossover bioequivalence (BE) study.

Design
------
Two-sequence, two-period crossover (AB | BA).  Each subject receives both
test (T) and reference (R) formulations in randomised order with a washout
between periods.

When to use
-----------
- Standard bioequivalence studies comparing a generic to a reference product
- PK endpoints: AUC_0-t, AUC_0-inf, Cmax (log-transformed)
- Equivalence limits: typically 80.00%-125.00% (MFDS / FDA / EMA)

Formula (TOST-based)
--------------------
For log-transformed data with equivalence limits (theta_L, theta_U):

    sigma_w^2 = ln(1 + CV_w^2)          (within-subject variance on log scale)
    delta     = |ln(GMR)|               (expected deviation from ratio = 1)
    theta     = ln(theta_U)             (upper equivalence limit on log scale)

    n_per_seq = (z_{alpha} + z_{beta})^2 * 2 * sigma_w^2 / (theta - delta)^2

Note: alpha is one-sided (0.05) for each of the two one-sided tests (TOST),
corresponding to an overall 90% CI approach.

Reference
---------
Chow S-C, Liu J-P. Design and Analysis of Bioavailability and Bioequivalence
Studies, 3rd ed. CRC Press, 2009, Chapter 5.
MFDS. Guidance on Bioequivalence Studies (생물학적동등성시험 기준).
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
) -> dict:
    """Calculate sample size for a 2x2 crossover BE study (TOST).

    Parameters
    ----------
    intra_cv : float
        Intra-subject coefficient of variation in percent (e.g. 25 for 25%).
    equivalence_limits : tuple of float
        Lower and upper bioequivalence limits on the original scale
        (default 0.80, 1.25).
    power : float
        Desired power (default 0.80).  For BE studies, 0.80 or 0.90.
    alpha : float
        One-sided significance level for each TOST test (default 0.05,
        corresponding to a 90% confidence interval).
    gmr : float
        Expected geometric mean ratio T/R (default 1.00).
    dropout_rate : float
        Expected dropout proportion.

    Returns
    -------
    dict
        n_per_sequence, n_total, adjusted values, and all parameters.
    """
    sigma_w = _cv_to_sigma_w(intra_cv)
    delta = abs(math.log(gmr))
    theta = math.log(equivalence_limits[1])  # ln(1.25) ≈ 0.2231

    margin = theta - delta
    if margin <= 0:
        raise ValueError(
            f"Expected GMR ({gmr}) is outside equivalence limits "
            f"{equivalence_limits}. No finite sample size exists."
        )

    # One-sided alpha for TOST
    z_alpha = normal_quantile(1.0 - alpha)
    z_beta = normal_quantile(power)

    # n per sequence for 2x2 crossover
    n_per_seq = math.ceil(
        (z_alpha + z_beta) ** 2 * 2.0 * sigma_w ** 2 / margin ** 2
    )
    # Ensure even total (2 sequences)
    if n_per_seq % 2 != 0:
        pass  # Each sequence gets n_per_seq; total = 2*n_per_seq
    n_total = 2 * n_per_seq

    n_per_seq_adj = adjust_for_dropout(n_per_seq, dropout_rate)
    n_total_adj = 2 * n_per_seq_adj

    params = {
        "design": "2x2 Crossover BE (TOST)",
        "intra_cv (%)": intra_cv,
        "sigma_w (log-scale)": round(sigma_w, 4),
        "equivalence_limits": equivalence_limits,
        "theta (log upper limit)": round(theta, 4),
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
    # Example: standard BE study, CV=25%, GMR=0.95, 80% power
    print("Example: Standard 2x2 Crossover Bioequivalence Study")
    print("  Intra-subject CV = 25%")
    print("  GMR (T/R) = 0.95, Equivalence limits = (0.80, 1.25)")
    print("  Alpha = 0.05 (one-sided, 90% CI), Power = 0.80")
    print("  Dropout rate = 10%\n")

    result = calculate_sample_size(
        intra_cv=25.0,
        gmr=0.95,
        power=0.80,
        alpha=0.05,
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

    # Sensitivity: also show for 90% power
    print("\n--- Sensitivity: Power = 0.90 ---")
    result90 = calculate_sample_size(
        intra_cv=25.0,
        gmr=0.95,
        power=0.90,
        alpha=0.05,
        dropout_rate=0.10,
    )
    print_result(
        design=result90["params"]["design"],
        n_per_group=result90["n_per_group"],
        n_total=result90["n_total"],
        params=result90["params"],
        n_per_group_adjusted=result90["n_per_group_adjusted"],
        n_total_adjusted=result90["n_total_adjusted"],
    )
