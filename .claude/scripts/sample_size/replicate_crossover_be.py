"""
Sample size calculation for replicate crossover BE designs (2x3, 2x4),
including Reference-Scaled Average Bioequivalence (RSABE) for high-variability drugs.

Design
------
- **2x3 (partial replicate)**: Sequences TRR, RTR (or TRR, RRT).
  Reference is given twice; allows estimation of within-reference variability.
- **2x4 (full replicate)**: Sequences TRTR, RTRT.
  Both T and R are given twice; allows estimation of within-subject variability
  for each formulation.

When to use
-----------
- High-variability drugs (intra-subject CV > 30%)
- When reference-scaled average bioequivalence (RSABE) is applicable
- When individual bioequivalence or within-subject variability comparison
  is of interest

RSABE (Reference-Scaled Average Bioequivalence)
------------------------------------------------
For high-variability drugs with within-reference CV > 30%:
- The equivalence limit is scaled by the within-reference variability
- Criterion: (ln(T) - ln(R))^2 - theta * sigma_WR^2 <= 0
  where theta = (ln(1.25) / sigma_0)^2
  sigma_0 = regulatory constant (0.25 for FDA, log(1.25) for MFDS)
- A point estimate constraint may also apply (e.g. 0.80-1.25)

Formula (standard, non-RSABE)
------------------------------
For 2x3 design:
    n_per_seq = 1.5 * (z_alpha + z_beta)^2 * sigma_w^2 / (theta - delta)^2

For 2x4 design (same variance reduction as 2x2, plus replication benefit):
    n_per_seq = (z_alpha + z_beta)^2 * sigma_w^2 / (theta - delta)^2

Note: The 2x4 full replicate has the same per-sequence formula as 2x2 but
the total is also 2 * n_per_seq.  The advantage is the ability to estimate
within-subject variability for each product.

Reference
---------
Howe WG. Approximate confidence limits on the mean of X + Y where X and Y
are two tabled independent random variables. JASA 1974.
FDA Guidance. Bioequivalence Studies With Pharmacokinetic Endpoints for Drugs
Submitted Under an ANDA (2021). — RSABE methodology.
MFDS. 고변동 약물의 생물학적동등성시험 평가 가이드라인.
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
    design_type: str = "2x4",
    equivalence_limits: tuple[float, float] = (0.80, 1.25),
    power: float = 0.80,
    alpha: float = 0.05,
    gmr: float = 1.00,
    dropout_rate: float = 0.0,
    use_rsabe: bool = False,
    regulatory_constant: float = 0.25,
) -> dict:
    """Calculate sample size for a replicate crossover BE study.

    Parameters
    ----------
    intra_cv : float
        Intra-subject CV (%) for the reference product.
    design_type : str
        "2x3" for partial replicate or "2x4" for full replicate.
    equivalence_limits : tuple of float
        BE limits on the original scale (default 0.80-1.25).
    power : float
        Desired power (default 0.80).
    alpha : float
        One-sided significance level for TOST (default 0.05).
    gmr : float
        Expected geometric mean ratio T/R.
    dropout_rate : float
        Expected dropout proportion.
    use_rsabe : bool
        If True, use Reference-Scaled Average Bioequivalence for
        high-variability drugs (CV > 30%).
    regulatory_constant : float
        Sigma_0 for RSABE scaling.  FDA uses 0.25; MFDS uses ln(1.25)
        ≈ 0.2231.

    Returns
    -------
    dict
        Sample size results and parameters.
    """
    if design_type not in ("2x3", "2x4"):
        raise ValueError(f"design_type must be '2x3' or '2x4', got {design_type!r}")

    sigma_w = _cv_to_sigma_w(intra_cv)
    delta = abs(math.log(gmr))

    z_alpha = normal_quantile(1.0 - alpha)
    z_beta = normal_quantile(power)

    if use_rsabe and intra_cv > 30.0:
        # RSABE: scaled equivalence limit
        # Expanded limit: theta_s = regulatory_constant * (sigma_WR / sigma_0)
        # But if sigma_WR > sigma_0, limit expands
        # Linearised approach: treat the scaled limit as the effective theta
        # For power calculation, the effective margin is sigma_0 * (sigma_WR / sigma_0) = sigma_WR
        # Simplified power formula using the regulatory constant:
        theta_scaled = regulatory_constant * sigma_w  # scaled limit on log scale
        # In RSABE the margin increases with variability, making it easier to
        # show equivalence for high-CV drugs.
        # Effective margin for power calculation:
        effective_margin = theta_scaled - delta
        if effective_margin <= 0:
            raise ValueError(
                f"With RSABE scaling, the effective margin is non-positive. "
                f"GMR={gmr} is too far from 1."
            )
        rsabe_note = "RSABE (scaled limits)"
    else:
        theta = math.log(equivalence_limits[1])
        effective_margin = theta - delta
        if effective_margin <= 0:
            raise ValueError(
                f"GMR ({gmr}) with CV={intra_cv}% exceeds equivalence limits. "
                f"No finite sample size exists with standard (unscaled) limits."
            )
        rsabe_note = "Standard (unscaled) limits"

    # Variance multiplier depends on design
    if design_type == "2x3":
        # Partial replicate: variance multiplier is 1.5 (3 periods, 2 sequences)
        var_multiplier = 1.5
        n_sequences = 2
    else:  # 2x4
        # Full replicate: variance multiplier is 1.0 (each product given twice)
        var_multiplier = 1.0
        n_sequences = 2

    n_per_seq = math.ceil(
        var_multiplier
        * (z_alpha + z_beta) ** 2
        * sigma_w ** 2
        / effective_margin ** 2
    )

    n_total = n_sequences * n_per_seq
    n_per_seq_adj = adjust_for_dropout(n_per_seq, dropout_rate)
    n_total_adj = n_sequences * n_per_seq_adj

    params = {
        "design": f"Replicate Crossover BE ({design_type})",
        "method": rsabe_note,
        "intra_cv (%)": intra_cv,
        "sigma_w (log-scale)": round(sigma_w, 4),
        "design_type": design_type,
        "variance_multiplier": var_multiplier,
        "equivalence_limits": equivalence_limits,
        "gmr": gmr,
        "delta (|ln(GMR)|)": round(delta, 4),
        "effective_margin (log)": round(effective_margin, 4),
        "use_rsabe": use_rsabe,
        "regulatory_constant (sigma_0)": regulatory_constant if use_rsabe else "N/A",
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
    # Example 1: High-variability drug, 2x4 full replicate with RSABE
    print("Example 1: High-variability drug — 2x4 replicate with RSABE")
    print("  Intra-subject CV = 45%, GMR = 0.95")
    print("  RSABE with regulatory constant sigma_0 = 0.25 (FDA)")
    print("  Alpha = 0.05 (one-sided), Power = 0.90, Dropout = 20%\n")

    result1 = calculate_sample_size(
        intra_cv=45.0,
        design_type="2x4",
        gmr=0.95,
        power=0.90,
        alpha=0.05,
        dropout_rate=0.20,
        use_rsabe=True,
        regulatory_constant=0.25,
    )
    print_result(
        design=result1["params"]["design"],
        n_per_group=result1["n_per_group"],
        n_total=result1["n_total"],
        params=result1["params"],
        n_per_group_adjusted=result1["n_per_group_adjusted"],
        n_total_adjusted=result1["n_total_adjusted"],
    )

    # Example 2: Moderate-variability drug, 2x3 partial replicate, standard limits
    print("Example 2: Moderate-variability drug — 2x3 partial replicate")
    print("  Intra-subject CV = 35%, GMR = 1.00")
    print("  Standard limits (0.80-1.25)")
    print("  Alpha = 0.05 (one-sided), Power = 0.80, Dropout = 15%\n")

    result2 = calculate_sample_size(
        intra_cv=35.0,
        design_type="2x3",
        gmr=1.00,
        power=0.80,
        alpha=0.05,
        dropout_rate=0.15,
        use_rsabe=False,
    )
    print_result(
        design=result2["params"]["design"],
        n_per_group=result2["n_per_group"],
        n_total=result2["n_total"],
        params=result2["params"],
        n_per_group_adjusted=result2["n_per_group_adjusted"],
        n_total_adjusted=result2["n_total_adjusted"],
    )
