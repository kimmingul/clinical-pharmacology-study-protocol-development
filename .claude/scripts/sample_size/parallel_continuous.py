"""
Sample size calculation for a two-sample parallel design with continuous endpoints.

Design
------
Subjects are randomised to one of two independent groups and each group receives
a single treatment.  The primary comparison is the difference in means between
the two groups.

When to use
-----------
- Drug-drug interaction (DDI) study with a parallel design
- Any clinical pharmacology study comparing two independent groups on a
  continuous endpoint (e.g. AUC, Cmax, clearance)

Formula
-------
    n_per_group = 2 * ((z_{alpha/2} + z_beta) * sigma / delta)^2

where
    sigma = common standard deviation (pooled)
    delta = clinically meaningful difference in means
    z_{alpha/2}, z_beta = standard normal quantiles

Alternatively the user can supply Cohen's d (effect_size = delta / sigma)
and omit sigma/delta individually.

Reference
---------
Chow S-C, Shao J, Wang H, Lokhnygina Y. Sample Size Calculations in
Clinical Research, 3rd ed. CRC Press, 2018, Chapter 3.
"""

import math
import sys
import os

# Allow running as a standalone script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.power_analysis import (
    normal_quantile,
    adjust_for_dropout,
    print_result,
)


def calculate_sample_size(
    *,
    mean_diff: float | None = None,
    sd: float | None = None,
    effect_size: float | None = None,
    alpha: float = 0.05,
    power: float = 0.80,
    dropout_rate: float = 0.0,
) -> dict:
    """Calculate sample size for a two-sample parallel design (continuous).

    Provide EITHER (mean_diff + sd) OR effect_size.

    Parameters
    ----------
    mean_diff : float, optional
        Expected difference in means between groups.
    sd : float, optional
        Common (pooled) standard deviation.
    effect_size : float, optional
        Cohen's d = mean_diff / sd.  Used when mean_diff and sd are not
        supplied individually.
    alpha : float
        Two-sided significance level (default 0.05).
    power : float
        Desired statistical power (default 0.80).
    dropout_rate : float
        Expected dropout proportion (default 0.0).

    Returns
    -------
    dict
        n_per_group, n_total, n_per_group_adjusted, n_total_adjusted, and
        all input parameters.
    """
    if effect_size is not None:
        d = effect_size
    elif mean_diff is not None and sd is not None:
        if sd <= 0:
            raise ValueError("sd must be positive")
        d = mean_diff / sd
    else:
        raise ValueError(
            "Provide either (mean_diff and sd) or effect_size"
        )

    if d == 0:
        raise ValueError("Effect size (delta/sigma) must be non-zero")

    z_alpha_half = normal_quantile(1.0 - alpha / 2.0)
    z_beta = normal_quantile(power)

    n_per_group = math.ceil(2.0 * ((z_alpha_half + z_beta) / d) ** 2)
    n_total = 2 * n_per_group

    n_per_group_adj = adjust_for_dropout(n_per_group, dropout_rate)
    n_total_adj = 2 * n_per_group_adj

    params = {
        "design": "Two-sample parallel (continuous)",
        "mean_diff": mean_diff,
        "sd": sd,
        "effect_size (Cohen's d)": round(d, 4),
        "alpha (two-sided)": alpha,
        "power": power,
        "z_alpha/2": round(z_alpha_half, 4),
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
    # Example: DDI parallel study
    # Expected difference in AUC ratio = 20%, SD of log-AUC ~ 0.35
    # => mean_diff on log scale ~ log(1.20) ≈ 0.182, sd ~ 0.35
    print("Example: DDI parallel design (continuous endpoint)")
    print("  Expected mean difference = 0.182 (log-scale ~20% change)")
    print("  SD = 0.35, alpha = 0.05 (two-sided), power = 0.80")
    print("  Dropout rate = 10%\n")

    result = calculate_sample_size(
        mean_diff=0.182,
        sd=0.35,
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
