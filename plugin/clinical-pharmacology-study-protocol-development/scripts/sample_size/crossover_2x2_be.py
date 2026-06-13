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

Method (exact TOST power, noncentral-t)
---------------------------------------
For log-transformed data with equivalence limits (theta_L, theta_U):

    sigma_w^2 = ln(1 + CV_w^2)          (within-subject variance on log scale)
    delta     = |ln(GMR)|               (expected deviation from ratio = 1)

The estimated treatment contrast has variance sigma_w^2 / n_per_seq (i.e.
2*sigma_w^2 / N_total) with df = N_total - 2.  The sample size is the smallest
even N_total whose **exact** TOST power (the probability that the 90% CI lies
entirely within the limits) reaches the target.  Exact power is obtained by
integrating the conditional normal coverage over the chi-square distribution
of the variance estimate — this matches the PowerTOST package and is the
regulatory-grade approach (the earlier closed form 2*sigma_w^2*(z_a+z_b)^2/m^2
is only a normal approximation of the TOTAL N and was previously mis-applied
as the per-sequence count, doubling the result).

Note: alpha is one-sided (0.05) for each of the two one-sided tests (TOST),
corresponding to an overall 90% CI approach.

Reference
---------
Chow S-C, Liu J-P. Design and Analysis of Bioavailability and Bioequivalence
Studies, 3rd ed. CRC Press, 2009, Chapter 5.
Diletti E, Hauschke D, Steinijans VW. Sample size determination for
bioequivalence assessment by means of confidence intervals. Int J Clin
Pharmacol Ther Toxicol 1991; 29:1-8.
MFDS. Guidance on Bioequivalence Studies (생물학적동등성시험 기준).
"""

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.power_analysis import (
    solve_n_2x2_tost,
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
    max_n: int = 4000,
) -> dict:
    """Calculate sample size for a 2x2 crossover BE study (exact TOST).

    Finds the smallest even total N whose exact TOST power (``tost_power``)
    reaches ``power``.  The result matches the PowerTOST package.

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
    max_n : int
        Upper bound for the search (raises if exceeded).

    Returns
    -------
    dict
        n_per_sequence, n_total, adjusted values, achieved power, and all
        parameters.

    Examples
    --------
    >>> r = calculate_sample_size(intra_cv=25.0, gmr=0.95, power=0.80)
    >>> r["n_total"]
    28
    >>> r = calculate_sample_size(intra_cv=20.0, gmr=0.95, power=0.80)
    >>> r["n_total"]
    20
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

    # Exact TOST sample size (single source of truth in utils.power_analysis).
    n_total, achieved = solve_n_2x2_tost(
        sigma_w, gmr, power, alpha, equivalence_limits, max_n
    )
    n_per_seq = n_total // 2

    n_per_seq_adj = adjust_for_dropout(n_per_seq, dropout_rate)
    n_total_adj = 2 * n_per_seq_adj

    params = {
        "design": "2x2 Crossover BE (exact TOST)",
        "intra_cv (%)": intra_cv,
        "sigma_w (log-scale)": round(sigma_w, 4),
        "equivalence_limits": equivalence_limits,
        "theta (log upper limit)": round(theta, 4),
        "gmr": gmr,
        "delta (|ln(GMR)|)": round(delta, 4),
        "alpha (one-sided)": alpha,
        "power (target)": power,
        "power (achieved)": round(achieved, 4),
        "method": "exact TOST (noncentral-t / chi-square integration)",
        "dropout_rate": dropout_rate,
    }

    return {
        "n_per_group": n_per_seq,
        "n_total": n_total,
        "n_per_group_adjusted": n_per_seq_adj,
        "n_total_adjusted": n_total_adj,
        "achieved_power": achieved,
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
