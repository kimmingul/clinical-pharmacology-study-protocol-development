"""
Sample size calculation for a parallel design with binary endpoints.

Design
------
Subjects are randomised to one of two independent groups.  The primary
endpoint is a proportion (binary outcome).

When to use
-----------
- Less common in clinical pharmacology, but applicable when:
  - Comparing response rates (e.g. proportion achieving target exposure)
  - Comparing incidence of a specific PD effect
  - Phase 1b/2a dose-finding with a binary efficacy signal

Formula (Chi-squared / normal approximation)
---------------------------------------------
For comparing two proportions p1 and p2 (two-sided test):

    n_per_group = ((z_{alpha/2} * sqrt(2 * p_bar * q_bar) +
                    z_beta * sqrt(p1*q1 + p2*q2)) / (p1 - p2))^2

where
    p_bar = (p1 + p2) / 2
    q_bar = 1 - p_bar
    q1 = 1 - p1, q2 = 1 - p2

This is the uncorrected normal approximation.  For small samples,
a continuity correction (Yates) or Fisher's exact test may be more
appropriate.

Reference
---------
Fleiss JL, Levin B, Paik MC. Statistical Methods for Rates and
Proportions, 3rd ed. Wiley, 2003, Chapter 4.
Chow S-C, Shao J, Wang H. Sample Size Calculations in Clinical
Research, 3rd ed. CRC Press, 2018, Chapter 4.
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


def calculate_sample_size(
    *,
    p1: float,
    p2: float,
    alpha: float = 0.05,
    power: float = 0.80,
    dropout_rate: float = 0.0,
    continuity_correction: bool = False,
) -> dict:
    """Calculate sample size for comparing two proportions (parallel design).

    Parameters
    ----------
    p1 : float
        Expected proportion in group 1 (e.g. 0.30 for 30%).
    p2 : float
        Expected proportion in group 2.
    alpha : float
        Two-sided significance level (default 0.05).
    power : float
        Desired power (default 0.80).
    dropout_rate : float
        Expected dropout proportion.
    continuity_correction : bool
        If True, apply Yates' continuity correction (default False).

    Returns
    -------
    dict
        Sample size results and parameters.

    Raises
    ------
    ValueError
        If p1 == p2 (no difference to detect) or proportions are out of (0, 1).
    """
    for name, p in [("p1", p1), ("p2", p2)]:
        if not (0.0 < p < 1.0):
            raise ValueError(f"{name} must be in (0, 1), got {p}")

    if p1 == p2:
        raise ValueError("p1 and p2 must differ for sample size calculation")

    diff = abs(p1 - p2)
    p_bar = (p1 + p2) / 2.0
    q_bar = 1.0 - p_bar
    q1 = 1.0 - p1
    q2 = 1.0 - p2

    z_alpha_half = normal_quantile(1.0 - alpha / 2.0)
    z_beta = normal_quantile(power)

    numerator = (
        z_alpha_half * math.sqrt(2.0 * p_bar * q_bar)
        + z_beta * math.sqrt(p1 * q1 + p2 * q2)
    )
    n_per_group = math.ceil((numerator / diff) ** 2)

    if continuity_correction:
        # Yates' continuity correction
        n_cc = (n_per_group / 4.0) * (
            1.0 + math.sqrt(1.0 + 4.0 / (n_per_group * diff))
        ) ** 2
        n_per_group = math.ceil(n_cc)

    n_total = 2 * n_per_group
    n_per_group_adj = adjust_for_dropout(n_per_group, dropout_rate)
    n_total_adj = 2 * n_per_group_adj

    params = {
        "design": "Two-sample parallel (binary endpoint)",
        "p1": p1,
        "p2": p2,
        "difference (|p1 - p2|)": round(diff, 4),
        "alpha (two-sided)": alpha,
        "power": power,
        "z_alpha/2": round(z_alpha_half, 4),
        "z_beta": round(z_beta, 4),
        "continuity_correction": continuity_correction,
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
    # Example: comparing response rates 30% vs 60%
    print("Example: Parallel design with binary endpoint")
    print("  Group 1 proportion (p1) = 0.30")
    print("  Group 2 proportion (p2) = 0.60")
    print("  Alpha = 0.05 (two-sided), Power = 0.80, Dropout = 10%\n")

    result = calculate_sample_size(
        p1=0.30,
        p2=0.60,
        alpha=0.05,
        power=0.80,
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

    # With continuity correction
    print("\n--- With Yates' continuity correction ---")
    result_cc = calculate_sample_size(
        p1=0.30,
        p2=0.60,
        alpha=0.05,
        power=0.80,
        dropout_rate=0.10,
        continuity_correction=True,
    )
    print_result(
        design=result_cc["params"]["design"],
        n_per_group=result_cc["n_per_group"],
        n_total=result_cc["n_total"],
        params=result_cc["params"],
        n_per_group_adjusted=result_cc["n_per_group_adjusted"],
        n_total_adjusted=result_cc["n_total_adjusted"],
    )
