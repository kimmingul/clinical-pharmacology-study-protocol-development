"""
Sample size calculation for Clopidogrel + Omeprazole DDI study.

Study Title: Two-period fixed-sequence crossover DDI study
             Clopidogrel (victim) + Omeprazole (CYP2C19 inhibitor)

Primary endpoint: H4 (active metabolite) AUC₀₋₂₄ and Cmax GMR
                  Omeprazole co-administration vs Clopidogrel alone

Statistical Framework
---------------------
This study aims to CHARACTERIZE/DETECT a DDI, NOT to show equivalence.

H0: No DDI — ln(GMR) = 0  (i.e., GMR = 1.0)
H1: DDI exists — ln(GMR) = ln(0.55) = -0.598  (expected ~45% AUC decrease)

The 90% CI of GMR is computed and reported.
The study is powered so that the 90% CI EXCLUDES 1.0 (confirms DDI significance).

alpha = 0.10 (two-sided) → equivalent to reporting 90% CI
      = standard for DDI characterization studies
      = α=0.05 one-sided is equivalent to α=0.10 two-sided for 90% CI

Formula (paired crossover, 2-period one-sequence)
-------------------------------------------------
Each subject serves as own control (paired difference):
    d_i = ln(AUC_Period2_i) - ln(AUC_Period1_i)

Under H0: E[d_i] = 0
Under H1: E[d_i] = ln(GMR_expected) = ln(0.55) = -0.598

Var(d_i) = 2 * sigma_w^2   (within-subject variance over 2 periods)

One-sample t-test (or normal approximation for sample size):
    n = (z_alpha/2 + z_beta)^2 * 2 * sigma_w^2 / delta^2

where:
    sigma_w = sqrt[ln(1 + CV^2)]  — within-subject SD on log scale
    delta   = |ln(GMR_expected)|  — effect size (minimum detectable effect)
    alpha   = 0.10 (two-sided, for 90% CI)
    beta    = 0.20 (power = 80%)

Key parameters
--------------
- Intra-subject CV = 75% (conservative: mixed CYP2C19 EM/IM/PM cohort,
  no genotyping per sponsor decision)
  Source: H4 CV ~50-60% in EM subjects (01_research_report.md §3.1);
          upward adjustment to 75% per design_decisions.md §9.1
- Expected GMR = 0.55 (H4 AUC 45% decrease)
  Source: Angiolillo 2011, PMID 20844485 (GMR range 0.53-0.60)
- No-effect boundary: 80.00-125.00% (MFDS/FDA/ICH M12)
- Alpha = 0.10 two-sided (→ 90% CI), Power = 80%, Dropout = 15%

References
----------
FDA. Drug Interaction Studies — Study Design, Data Analysis,
Implications for Dosing, and Labeling Recommendations. 2020.

Angiolillo DJ et al. Impact of Concomitant Oral Clopidogrel Loading and
Intravenous Unfractionated Heparin... Clin Pharmacol Ther 2011; 89(1):65-74.
PMID 20844485.
"""

import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.power_analysis import normal_quantile, adjust_for_dropout, print_result


def cv_to_sigma_w(cv_pct: float) -> float:
    """Convert intra-subject CV (%) to within-subject SD on the log scale."""
    cv = cv_pct / 100.0
    return math.sqrt(math.log(1.0 + cv ** 2))


def calculate_sample_size_ddi_detection(
    *,
    intra_cv: float,
    expected_gmr: float,
    power: float = 0.80,
    alpha_two_sided: float = 0.10,
    dropout_rate: float = 0.0,
) -> dict:
    """Calculate sample size to DETECT a DDI in a fixed-sequence crossover.

    Parameters
    ----------
    intra_cv : float
        Intra-subject CV (%) for the substrate PK parameter.
    expected_gmr : float
        Expected GMR (AUC ratio: with perpetrator / without).
        0.55 = 45% decrease in H4 AUC expected.
    power : float
        Desired statistical power (default 0.80).
    alpha_two_sided : float
        Two-sided alpha level (default 0.10, yielding 90% CI).
        alpha_two_sided=0.10 is the standard for DDI studies where
        we report 90% confidence intervals.
    dropout_rate : float
        Expected dropout proportion (default 0.0).

    Returns
    -------
    dict
        Sample size results and parameters.
    """
    sigma_w = cv_to_sigma_w(intra_cv)
    delta = abs(math.log(expected_gmr))

    # Two-sided alpha for 90% CI
    z_alpha2 = normal_quantile(1.0 - alpha_two_sided / 2.0)
    z_beta = normal_quantile(power)

    # Paired one-sample formula:  n = (z_a/2 + z_b)^2 * 2*sigma_w^2 / delta^2
    n_evaluable = math.ceil(
        (z_alpha2 + z_beta) ** 2 * 2.0 * sigma_w ** 2 / delta ** 2
    )
    n_enrolled = adjust_for_dropout(n_evaluable, dropout_rate)

    params = {
        "design": "Fixed-sequence DDI (DDI detection, 90% CI)",
        "hypothesis": "H0: GMR=1.0  H1: GMR=expected_gmr",
        "intra_cv (%)": intra_cv,
        "sigma_w (log-scale)": round(sigma_w, 4),
        "expected_gmr": expected_gmr,
        "delta (|ln(GMR)|)": round(delta, 4),
        "alpha (two-sided)": alpha_two_sided,
        "CI level": f"{int((1-alpha_two_sided)*100)}%",
        "power (1-beta)": power,
        "z_alpha/2": round(z_alpha2, 4),
        "z_beta": round(z_beta, 4),
        "dropout_rate": dropout_rate,
    }

    return {
        "n_evaluable": n_evaluable,
        "n_enrolled": n_enrolled,
        "params": params,
    }


def run_sensitivity_analyses():
    """Run all sensitivity analyses and print results."""
    sep = "=" * 78

    print(f"\n{sep}")
    print("  ONE-SEQUENCE (FIXED-ORDER) DDI SAMPLE SIZE CALCULATION")
    print("  Study: Clopidogrel 300/75 mg + Omeprazole 80 mg")
    print("  Endpoint: H4 Active Metabolite AUC₀₋₂₄ and Cmax GMR (90% CI)")
    print("  Design: Two-period fixed-sequence crossover (one-sequence)")
    print("  Framework: DDI detection (H0: GMR=1.0 vs H1: GMR=expected)")
    print("  Boundary: 80.00-125.00%  |  alpha=0.10 two-sided  |  power=0.80")
    print(f"{sep}\n")

    # ---------------------------------------------------------------
    # Sensitivity Analysis 1: CV% varying, GMR=0.55 fixed
    # ---------------------------------------------------------------
    print("=== Sensitivity Analysis 1: CV% (intra-subject) × GMR=0.55 (dropout=15%) ===")
    print()
    print(f"  {'CV%':>5}  {'sigma_w':>8}  {'delta':>8}  "
          f"{'n evaluable':>12}  {'n enrolled':>12}")
    print("  " + "-" * 55)

    for cv in [50, 60, 75, 85]:
        result = calculate_sample_size_ddi_detection(
            intra_cv=cv,
            expected_gmr=0.55,
            power=0.80,
            alpha_two_sided=0.10,
            dropout_rate=0.15,
        )
        p = result["params"]
        print(f"  {cv:>5}  {p['sigma_w (log-scale)']:>8.4f}  "
              f"{p['delta (|ln(GMR)|)']:>8.4f}  "
              f"{result['n_evaluable']:>12}  {result['n_enrolled']:>12}")

    print()
    print("  Note: sigma_w = sqrt[ln(1 + CV²)];  delta = |ln(0.55)| = 0.5978")

    # ---------------------------------------------------------------
    # Sensitivity Analysis 2: GMR varying, CV%=75% fixed
    # ---------------------------------------------------------------
    print()
    print("=== Sensitivity Analysis 2: CV%=75% × GMR (dropout=15%) ===")
    print()
    print(f"  {'GMR':>6}  {'delta':>8}  "
          f"{'n evaluable':>12}  {'n enrolled':>12}  Interpretation")
    print("  " + "-" * 72)

    gmr_labels = {
        0.50: "Strong DDI (worst case)",
        0.55: "Moderate DDI (Angiolillo 2011, primary) *",
        0.60: "Conservative (upper bound of literature range)",
    }
    for gmr in [0.50, 0.55, 0.60]:
        result = calculate_sample_size_ddi_detection(
            intra_cv=75,
            expected_gmr=gmr,
            power=0.80,
            alpha_two_sided=0.10,
            dropout_rate=0.15,
        )
        p = result["params"]
        delta = p["delta (|ln(GMR)|)"]
        print(f"  {gmr:>6.2f}  {delta:>8.4f}  "
              f"{result['n_evaluable']:>12}  {result['n_enrolled']:>12}  "
              f"{gmr_labels[gmr]}")

    # ---------------------------------------------------------------
    # Primary scenario detailed output
    # ---------------------------------------------------------------
    print()
    print("=== PRIMARY SCENARIO DETAILED CALCULATION ===")
    print("    CV%=75%, GMR=0.55, power=0.80, alpha=0.10 two-sided, dropout=15%")
    print()
    result = calculate_sample_size_ddi_detection(
        intra_cv=75,
        expected_gmr=0.55,
        power=0.80,
        alpha_two_sided=0.10,
        dropout_rate=0.15,
    )
    p = result["params"]
    sw = p["sigma_w (log-scale)"]
    delta = p["delta (|ln(GMR)|)"]
    z_a2 = p["z_alpha/2"]
    z_b = p["z_beta"]

    print(f"  sigma_w = sqrt[ln(1 + 0.75²)]       = {sw:.4f}")
    print(f"  delta   = |ln(0.55)|                  = {delta:.4f}")
    print(f"  z_alpha/2 (alpha/2=0.05, z=1.6449)   = {z_a2:.4f}")
    print(f"  z_beta    (power=0.80, z=0.8416)      = {z_b:.4f}")
    print(f"  (z_a/2 + z_b)^2                       = {(z_a2 + z_b)**2:.4f}")
    print(f"  2 * sigma_w^2                          = {2*sw**2:.4f}")
    print(f"  2 * sigma_w^2 / delta^2                = {2*sw**2/delta**2:.4f}")
    print(f"  n evaluable (ceiling)                  = {result['n_evaluable']}")
    print(f"  n enrolled  (15% dropout: n/0.85)      = {result['n_enrolled']}")
    print()
    print("  RECOMMENDATION: Enroll 20 subjects (evaluable target: ≥17)")
    print()
    print("  Rationale for rounding 19→20:")
    print("  - Even numbers are operationally preferred for fixed-sequence DDI")
    print("  - Provides slight buffer above 15% dropout adjustment (19)")
    print("  - Conservative approach given unusually high CV% (75%)")
    print("  - Consistent with NCT01129375 design (n~24 for 4-arm version)")

    # ---------------------------------------------------------------
    # Package versions
    # ---------------------------------------------------------------
    print()
    print(f"{sep}")
    import scipy
    import sys as _sys
    print(f"  Python  : {_sys.version.split()[0]}")
    print(f"  scipy   : {scipy.__version__}")
    print(f"  numpy   : ", end="")
    import numpy as np
    print(np.__version__)
    print(f"{sep}\n")


if __name__ == "__main__":
    run_sensitivity_analyses()
