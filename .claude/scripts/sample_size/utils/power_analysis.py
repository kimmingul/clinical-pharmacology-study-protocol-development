"""
Common utility functions for sample size and power analysis.

Provides shared helpers used across all sample size calculation scripts:
  - Statistical quantile functions (normal, t)
  - Dropout adjustment
  - Standardised result printing

Dependencies: scipy
"""

import math
from typing import Optional

from scipy.stats import norm, t as t_dist


def normal_quantile(p: float) -> float:
    """Return the quantile (inverse CDF) of the standard normal distribution.

    Parameters
    ----------
    p : float
        Cumulative probability (0 < p < 1).

    Returns
    -------
    float
        z-value such that P(Z <= z) = p.

    Examples
    --------
    >>> round(normal_quantile(0.975), 4)
    1.96
    >>> round(normal_quantile(0.80), 4)
    0.8416
    """
    return float(norm.ppf(p))


def t_quantile(df: int, p: float) -> float:
    """Return the quantile (inverse CDF) of Student's t distribution.

    Parameters
    ----------
    df : int
        Degrees of freedom (positive integer).
    p : float
        Cumulative probability (0 < p < 1).

    Returns
    -------
    float
        t-value such that P(T <= t) = p for the given df.

    Examples
    --------
    >>> round(t_quantile(20, 0.975), 4)
    2.086
    """
    return float(t_dist.ppf(p, df))


def adjust_for_dropout(n: int, dropout_rate: float) -> int:
    """Adjust sample size upward to account for expected dropout.

    Applies the formula: N_adjusted = ceil(n / (1 - dropout_rate)).

    Parameters
    ----------
    n : int
        Sample size before dropout adjustment.
    dropout_rate : float
        Expected proportion of subjects who will drop out (0 <= rate < 1).
        For example, 0.10 for 10% dropout.

    Returns
    -------
    int
        Adjusted sample size (always rounded up).

    Raises
    ------
    ValueError
        If dropout_rate is not in [0, 1).

    Examples
    --------
    >>> adjust_for_dropout(24, 0.10)
    27
    >>> adjust_for_dropout(24, 0.0)
    24
    """
    if not (0.0 <= dropout_rate < 1.0):
        raise ValueError(
            f"dropout_rate must be in [0, 1), got {dropout_rate}"
        )
    if dropout_rate == 0.0:
        return n
    return math.ceil(n / (1.0 - dropout_rate))


def print_result(
    design: str,
    n_per_group: int,
    n_total: int,
    params: dict,
    *,
    n_per_group_adjusted: Optional[int] = None,
    n_total_adjusted: Optional[int] = None,
) -> None:
    """Print a standardised sample-size result block.

    Parameters
    ----------
    design : str
        Name of the study design (e.g. "2x2 Crossover BE").
    n_per_group : int
        Evaluable subjects per group/sequence (before dropout adjustment).
    n_total : int
        Total evaluable subjects (before dropout adjustment).
    params : dict
        Dictionary of parameters used in the calculation.
    n_per_group_adjusted : int, optional
        Subjects per group after dropout adjustment.
    n_total_adjusted : int, optional
        Total subjects after dropout adjustment.
    """
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  Sample Size Calculation — {design}")
    print(sep)

    print("\n  Parameters:")
    for key, value in params.items():
        if isinstance(value, float):
            print(f"    {key:30s} = {value:.4f}")
        else:
            print(f"    {key:30s} = {value}")

    print(f"\n  Results (evaluable):")
    print(f"    {'N per group/sequence':30s} = {n_per_group}")
    print(f"    {'N total':30s} = {n_total}")

    if n_per_group_adjusted is not None and n_total_adjusted is not None:
        dropout_pct = params.get("dropout_rate", 0) * 100
        print(f"\n  Results (adjusted for {dropout_pct:.0f}% dropout):")
        print(f"    {'N per group/sequence':30s} = {n_per_group_adjusted}")
        print(f"    {'N total':30s} = {n_total_adjusted}")

    print(f"\n{sep}\n")
