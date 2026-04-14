"""
Dose escalation scheme generators for first-in-human (FIH) studies.

Provides functions to generate dose escalation tables for SAD (single
ascending dose) and MAD (multiple ascending dose) studies.

Methods
-------
1. **Modified Fibonacci**: The classic escalation pattern used in Phase 1
   oncology and clinical pharmacology.  Increment ratios decrease as doses
   increase: 100%, 67%, 50%, 33%, 33%, ...

2. **Constant ratio**: Fixed multiplicative factor between doses.  Common
   ratios include 2x (doubling) for early dose levels and 1.5x for later
   levels.

Reference
---------
Storer BE. Design and Analysis of Phase I Clinical Trials. Biometrics 1989;
45(3):925-937.

FDA Guidance. Estimating the Maximum Safe Starting Dose in Initial Clinical
Trials for Therapeutics in Adult Healthy Volunteers. July 2005.

EMA Guideline. Strategies to Identify and Mitigate Risks for First-in-Human
and Early Clinical Trials with Investigational Medicinal Products. 2017.
"""

from dataclasses import dataclass


# Modified Fibonacci increment ratios (applied sequentially)
# Level 1 -> 2: +100%, Level 2 -> 3: +67%, Level 3 -> 4: +50%,
# Level 4 -> 5: +33%, Level 5+: +33% each
FIBONACCI_INCREMENTS = [1.00, 0.67, 0.50, 0.33]


@dataclass
class DoseLevel:
    """A single dose level in an escalation scheme."""

    level: int
    dose: float
    increment_pct: float | None  # percentage increase from previous level
    fold_from_start: float       # fold increase from starting dose


def modified_fibonacci(
    start_dose: float,
    n_levels: int,
) -> list[DoseLevel]:
    """Generate dose levels using the modified Fibonacci escalation scheme.

    The increment from each dose to the next follows the pattern:
    100%, 67%, 50%, 33%, 33%, 33%, ...

    Parameters
    ----------
    start_dose : float
        Starting dose (e.g. MRSD in mg).
    n_levels : int
        Number of dose levels to generate (including the starting dose).

    Returns
    -------
    list of DoseLevel
        Dose escalation table.

    Examples
    --------
    >>> levels = modified_fibonacci(5.0, 6)
    >>> [round(l.dose, 1) for l in levels]
    [5.0, 10.0, 16.7, 25.0, 33.3, 44.3]
    """
    if n_levels < 1:
        raise ValueError("n_levels must be >= 1")

    levels = [
        DoseLevel(level=1, dose=start_dose, increment_pct=None, fold_from_start=1.0)
    ]

    current_dose = start_dose
    for i in range(1, n_levels):
        # Use the predefined increments; after exhaustion, repeat the last one
        if i - 1 < len(FIBONACCI_INCREMENTS):
            increment = FIBONACCI_INCREMENTS[i - 1]
        else:
            increment = FIBONACCI_INCREMENTS[-1]

        current_dose = current_dose * (1.0 + increment)
        levels.append(
            DoseLevel(
                level=i + 1,
                dose=round(current_dose, 4),
                increment_pct=round(increment * 100, 1),
                fold_from_start=round(current_dose / start_dose, 2),
            )
        )

    return levels


def constant_ratio(
    start_dose: float,
    ratio: float,
    n_levels: int,
) -> list[DoseLevel]:
    """Generate dose levels with a fixed multiplicative ratio.

    Parameters
    ----------
    start_dose : float
        Starting dose (mg).
    ratio : float
        Multiplicative factor between consecutive doses (e.g. 2.0 for
        doubling, 1.5 for 50% increments).
    n_levels : int
        Number of dose levels (including the starting dose).

    Returns
    -------
    list of DoseLevel
        Dose escalation table.

    Examples
    --------
    >>> levels = constant_ratio(10.0, 2.0, 5)
    >>> [round(l.dose, 1) for l in levels]
    [10.0, 20.0, 40.0, 80.0, 160.0]
    """
    if n_levels < 1:
        raise ValueError("n_levels must be >= 1")
    if ratio <= 0:
        raise ValueError("ratio must be positive")

    levels = [
        DoseLevel(level=1, dose=start_dose, increment_pct=None, fold_from_start=1.0)
    ]

    current_dose = start_dose
    increment_pct = round((ratio - 1.0) * 100, 1)
    for i in range(1, n_levels):
        current_dose = current_dose * ratio
        levels.append(
            DoseLevel(
                level=i + 1,
                dose=round(current_dose, 4),
                increment_pct=increment_pct,
                fold_from_start=round(current_dose / start_dose, 2),
            )
        )

    return levels


def print_escalation_table(doses: list[DoseLevel], title: str = "") -> None:
    """Print a formatted dose escalation table.

    Parameters
    ----------
    doses : list of DoseLevel
        Dose levels to display.
    title : str, optional
        Title for the table.
    """
    sep = "=" * 65
    print(f"\n{sep}")
    if title:
        print(f"  {title}")
        print(sep)

    header = (
        f"  {'Level':>5s}  "
        f"{'Dose (mg)':>12s}  "
        f"{'Increment':>10s}  "
        f"{'Fold from Start':>16s}"
    )
    print(header)
    print(f"  {'-'*5}  {'-'*12}  {'-'*10}  {'-'*16}")

    for dl in doses:
        inc_str = f"+{dl.increment_pct:.0f}%" if dl.increment_pct is not None else "—"
        dose_str = f"{dl.dose:.1f}" if dl.dose >= 1 else f"{dl.dose:.2f}"
        print(
            f"  {dl.level:>5d}  "
            f"{dose_str:>12s}  "
            f"{inc_str:>10s}  "
            f"{dl.fold_from_start:>16.1f}x"
        )

    print(f"\n{sep}\n")


if __name__ == "__main__":
    # Example 1: SAD study using modified Fibonacci
    print("Example 1: SAD study — Modified Fibonacci escalation")
    print("  Starting dose (MRSD) = 5 mg\n")

    fib_doses = modified_fibonacci(start_dose=5.0, n_levels=8)
    print_escalation_table(fib_doses, "SAD — Modified Fibonacci (start = 5 mg)")

    # Example 2: SAD with constant 2x ratio (aggressive early escalation)
    print("Example 2: SAD study — Constant 2x ratio")
    print("  Starting dose = 1 mg, Ratio = 2.0\n")

    double_doses = constant_ratio(start_dose=1.0, ratio=2.0, n_levels=7)
    print_escalation_table(double_doses, "SAD — Constant 2x Ratio (start = 1 mg)")

    # Example 3: MAD study with conservative 1.5x ratio
    print("Example 3: MAD study — Constant 1.5x ratio")
    print("  Starting dose = 10 mg, Ratio = 1.5\n")

    mad_doses = constant_ratio(start_dose=10.0, ratio=1.5, n_levels=5)
    print_escalation_table(mad_doses, "MAD — Constant 1.5x Ratio (start = 10 mg)")

    # Example 4: Combined — Fibonacci for SAD, then select MAD doses
    print("Example 4: Practical SAD -> MAD dose selection")
    print("  SAD uses modified Fibonacci starting at 5 mg")
    print("  MAD uses selected SAD doses: levels 2, 4, 6\n")

    sad_levels = modified_fibonacci(start_dose=5.0, n_levels=8)
    mad_selected = [sad_levels[1], sad_levels[3], sad_levels[5]]
    for i, dl in enumerate(mad_selected, 1):
        dl_new = DoseLevel(
            level=i,
            dose=dl.dose,
            increment_pct=None,
            fold_from_start=round(dl.dose / mad_selected[0].dose, 2),
        )
        mad_selected[i - 1] = dl_new
    print_escalation_table(mad_selected, "MAD — Selected from SAD Fibonacci")
