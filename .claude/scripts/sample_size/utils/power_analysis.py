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

from scipy.stats import norm, t as t_dist, chi2
from scipy.integrate import quad


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


def tost_power_2x2(
    n_total: int,
    sigma_w: float,
    gmr: float,
    alpha: float = 0.05,
    equivalence_limits: tuple = (0.80, 1.25),
) -> float:
    """Exact TOST power for a 2x2 crossover (BE / DDI no-effect) design.

    The treatment contrast on the log scale has variance ``sigma_w**2 /
    n_per_seq`` (= ``2*sigma_w**2 / n_total``) with ``df = n_total - 2``.
    The power is the probability that the 90% CI lies entirely within the
    equivalence limits, obtained by integrating the conditional normal
    coverage over the chi-square distribution of the variance estimate.
    This matches the PowerTOST package (validated against published examples).

    Parameters
    ----------
    n_total : int
        Total number of subjects (``n_total / 2`` per sequence).
    sigma_w : float
        Within-subject SD on the log scale (``sqrt(ln(1 + CV**2))``).
    gmr : float
        True geometric mean ratio (test / reference, or with / without).
    alpha : float
        One-sided alpha for each of the two one-sided tests (default 0.05).
    equivalence_limits : tuple of float
        Equivalence (no-effect) limits on the original scale.

    Returns
    -------
    float
        Probability that the 90% CI is contained within the limits.

    Examples
    --------
    >>> sw = math.sqrt(math.log(1 + 0.25**2))
    >>> round(tost_power_2x2(28, sw, 0.95), 3)
    0.807
    """
    n_per_seq = n_total / 2.0
    df = n_total - 2
    if df < 1:
        return 0.0
    delta = math.log(gmr)
    ln_lower = math.log(equivalence_limits[0])
    ln_upper = math.log(equivalence_limits[1])
    se = sigma_w / math.sqrt(n_per_seq)            # SD of the point estimate
    t_crit = t_quantile(df, 1.0 - alpha)
    lo_u = float(chi2.ppf(1e-9, df))
    hi_u = float(chi2.ppf(1.0 - 1e-9, df))

    def integrand(u: float) -> float:
        s = sigma_w * math.sqrt(u / df)            # sampled SD
        half_width = t_crit * (s / math.sqrt(n_per_seq))
        a = ln_lower + half_width
        b = ln_upper - half_width
        if b <= a:
            return 0.0
        coverage = norm.cdf((b - delta) / se) - norm.cdf((a - delta) / se)
        return coverage * chi2.pdf(u, df)

    value, _ = quad(integrand, lo_u, hi_u, limit=300)
    return float(value)


def solve_n_2x2_tost(
    sigma_w: float,
    gmr: float,
    power: float = 0.80,
    alpha: float = 0.05,
    equivalence_limits: tuple = (0.80, 1.25),
    max_n: int = 4000,
) -> tuple:
    """Smallest even total N whose exact TOST power reaches ``power``.

    Seeds from the corrected normal approximation of the TOTAL N
    (``2*(z_a+z_b)**2*sigma_w**2/margin**2``), then climbs to the exact answer.

    Returns
    -------
    tuple
        ``(n_total, achieved_power)``.

    Examples
    --------
    >>> sw = math.sqrt(math.log(1 + 0.25**2))
    >>> solve_n_2x2_tost(sw, 0.95, 0.80)[0]
    28
    """
    delta = abs(math.log(gmr))
    margin = math.log(equivalence_limits[1]) - delta
    if margin <= 0:
        raise ValueError(
            f"GMR ({gmr}) is outside equivalence limits {equivalence_limits}; "
            f"no finite sample size exists."
        )
    z_alpha = normal_quantile(1.0 - alpha)
    z_beta = normal_quantile(power)
    n_approx = 2.0 * (z_alpha + z_beta) ** 2 * sigma_w ** 2 / margin ** 2
    n_total = max(4, (int(math.floor(n_approx / 2.0)) - 3) * 2)
    while n_total <= max_n:
        achieved = tost_power_2x2(n_total, sigma_w, gmr, alpha, equivalence_limits)
        if achieved >= power:
            return n_total, achieved
        n_total += 2
    raise ValueError(f"Required N exceeds max_n={max_n} (GMR={gmr}).")


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
