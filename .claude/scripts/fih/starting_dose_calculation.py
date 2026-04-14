"""
First-in-Human (FIH) Starting Dose Calculation — MRSD and MABEL methods.

This module implements the FDA-recommended approach for estimating the maximum
recommended starting dose (MRSD) for first-in-human clinical trials.

Methods
-------
1. **MRSD via NOAEL-HED-Safety Factor**:
   - Convert the No-Observed-Adverse-Effect Level (NOAEL) from animal studies
     to a Human Equivalent Dose (HED) using body surface area (BSA) scaling.
   - Apply a safety factor (default 1/10) to derive the MRSD.

2. **MABEL (Minimum Anticipated Biological Effect Level)**:
   - Used for high-risk biologics, immunomodulators, and novel mechanisms.
   - Based on in vitro EC50 and target receptor occupancy.

BSA Conversion Factors (Km values)
-----------------------------------
Species-specific Km values for BSA-based dose conversion (mg/kg to mg/m^2):

    | Species        | Km    | Conversion factor (÷Km_species × Km_human) |
    |----------------|-------|---------------------------------------------|
    | Mouse          |  3    | ÷ 12.3                                      |
    | Rat            |  6    | ÷ 6.2                                       |
    | Ferret         |  7    | ÷ 5.3                                       |
    | Rabbit         | 12    | ÷ 3.1                                       |
    | Cynomolgus     | 12    | ÷ 3.1                                       |
    | Rhesus monkey  | 12    | ÷ 3.1                                       |
    | Dog            | 20    | ÷ 1.8                                       |
    | Human (60 kg)  | 37    | (reference)                                 |

    HED (mg/kg) = Animal dose (mg/kg) × (Km_animal / Km_human)
               = Animal dose (mg/kg) / conversion_factor

Reference
---------
FDA Guidance for Industry. Estimating the Maximum Safe Starting Dose in
Initial Clinical Trials for Therapeutics in Adult Healthy Volunteers.
July 2005. CDER, FDA.

EMA Guideline. Strategies to Identify and Mitigate Risks for First-in-Human
and Early Clinical Trials with Investigational Medicinal Products. 2017.
"""

import math
from dataclasses import dataclass

# BSA conversion factors: divide animal NOAEL (mg/kg) by this factor to get HED
# Factor = Km_human / Km_animal
BSA_CONVERSION_FACTORS: dict[str, float] = {
    "mouse": 12.3,
    "rat": 6.2,
    "ferret": 5.3,
    "rabbit": 3.1,
    "cynomolgus": 3.1,
    "monkey": 3.1,       # alias for cynomolgus/rhesus
    "rhesus": 3.1,
    "dog": 1.8,
    "minipig": 1.4,
}

# Km values (mg/kg -> mg/m^2) for reference
KM_VALUES: dict[str, float] = {
    "mouse": 3.0,
    "rat": 6.0,
    "ferret": 7.0,
    "rabbit": 12.0,
    "cynomolgus": 12.0,
    "monkey": 12.0,
    "rhesus": 12.0,
    "dog": 20.0,
    "minipig": 27.0,
    "human": 37.0,
}


@dataclass
class MRSDResult:
    """Result of MRSD calculation."""

    species: str
    noael_mg_kg: float
    hed_mg_kg: float
    safety_factor: float
    mrsd_mg_kg: float
    body_weight_kg: float
    mrsd_mg: float
    mrsd_mg_rounded: float


@dataclass
class MABELResult:
    """Result of MABEL calculation."""

    ec50: float
    target_occupancy: float
    mabel: float


def noael_to_hed(noael_mg_kg: float, species: str) -> float:
    """Convert NOAEL (mg/kg) to Human Equivalent Dose (mg/kg) using BSA scaling.

    Parameters
    ----------
    noael_mg_kg : float
        No-Observed-Adverse-Effect Level in mg/kg from the animal study.
    species : str
        Animal species (e.g. "mouse", "rat", "dog", "monkey").
        Case-insensitive.

    Returns
    -------
    float
        Human Equivalent Dose in mg/kg.

    Raises
    ------
    ValueError
        If the species is not recognised.

    Examples
    --------
    >>> round(noael_to_hed(100, "mouse"), 2)
    8.13
    >>> round(noael_to_hed(30, "rat"), 2)
    4.84
    >>> round(noael_to_hed(10, "dog"), 2)
    5.56
    """
    species_lower = species.lower().strip()
    factor = BSA_CONVERSION_FACTORS.get(species_lower)
    if factor is None:
        valid = ", ".join(sorted(BSA_CONVERSION_FACTORS.keys()))
        raise ValueError(
            f"Unknown species '{species}'. Valid species: {valid}"
        )
    return noael_mg_kg / factor


def hed_to_mrsd(
    hed_mg_kg: float,
    safety_factor: float = 10.0,
    body_weight_kg: float = 60.0,
) -> tuple[float, float]:
    """Apply a safety factor to HED to obtain the MRSD.

    Parameters
    ----------
    hed_mg_kg : float
        Human Equivalent Dose in mg/kg.
    safety_factor : float
        Safety margin divisor (default 10, meaning MRSD = HED / 10).
    body_weight_kg : float
        Assumed human body weight in kg (default 60 kg, per FDA guidance).

    Returns
    -------
    tuple of float
        (mrsd_mg_kg, mrsd_mg) — MRSD in mg/kg and total mg.
    """
    mrsd_mg_kg = hed_mg_kg / safety_factor
    mrsd_mg = mrsd_mg_kg * body_weight_kg
    return mrsd_mg_kg, mrsd_mg


def calculate_mrsd(
    noael_mg_kg: float,
    species: str,
    safety_factor: float = 10.0,
    body_weight_kg: float = 60.0,
) -> MRSDResult:
    """Full MRSD calculation pipeline: NOAEL -> HED -> MRSD.

    Parameters
    ----------
    noael_mg_kg : float
        NOAEL from the most sensitive relevant animal species (mg/kg).
    species : str
        Animal species used in the toxicology study.
    safety_factor : float
        Safety margin divisor (default 10).
    body_weight_kg : float
        Assumed human body weight in kg (default 60).

    Returns
    -------
    MRSDResult
        Dataclass containing all intermediate and final values.

    Examples
    --------
    >>> result = calculate_mrsd(30, "rat")
    >>> round(result.mrsd_mg, 2)
    29.03
    """
    hed = noael_to_hed(noael_mg_kg, species)
    mrsd_mg_kg, mrsd_mg = hed_to_mrsd(hed, safety_factor, body_weight_kg)

    # Round to a practical dose (nearest 0.5 mg for small doses, 1 mg otherwise)
    if mrsd_mg < 5:
        mrsd_rounded = math.floor(mrsd_mg * 2) / 2  # round down to nearest 0.5
    else:
        mrsd_rounded = math.floor(mrsd_mg)  # round down to nearest integer

    return MRSDResult(
        species=species,
        noael_mg_kg=noael_mg_kg,
        hed_mg_kg=round(hed, 4),
        safety_factor=safety_factor,
        mrsd_mg_kg=round(mrsd_mg_kg, 4),
        body_weight_kg=body_weight_kg,
        mrsd_mg=round(mrsd_mg, 4),
        mrsd_mg_rounded=mrsd_rounded,
    )


def calculate_mabel(
    ec50: float,
    target_occupancy: float = 0.10,
) -> MABELResult:
    """Calculate MABEL (Minimum Anticipated Biological Effect Level).

    Used for biologics and immunomodulatory agents where pharmacological
    activity at very low doses poses safety concerns.

    MABEL is estimated as the dose/concentration that produces a specified
    target receptor occupancy (typically 10% of EC50).

    Parameters
    ----------
    ec50 : float
        Half-maximal effective concentration from in vitro studies
        (in appropriate units, e.g. ng/mL or nM).
    target_occupancy : float
        Fractional receptor occupancy at which to define MABEL
        (default 0.10 = 10%).

    Returns
    -------
    MABELResult
        Dataclass with ec50, target_occupancy, and calculated mabel.

    Notes
    -----
    The MABEL calculation here uses a simple Emax model:
        Occupancy = C / (C + EC50)
    Solving for C at a given occupancy fraction:
        C = occupancy * EC50 / (1 - occupancy)

    In practice, MABEL should integrate multiple data sources: in vitro
    potency, receptor binding, PK/PD modelling, and cross-species
    pharmacology.

    Examples
    --------
    >>> result = calculate_mabel(100.0, 0.10)
    >>> round(result.mabel, 2)
    11.11
    """
    if not (0 < target_occupancy < 1):
        raise ValueError(
            f"target_occupancy must be in (0, 1), got {target_occupancy}"
        )
    mabel = target_occupancy * ec50 / (1.0 - target_occupancy)
    return MABELResult(
        ec50=ec50,
        target_occupancy=target_occupancy,
        mabel=round(mabel, 4),
    )


def print_mrsd_result(result: MRSDResult) -> None:
    """Pretty-print an MRSD calculation result."""
    sep = "=" * 60
    print(f"\n{sep}")
    print("  MRSD Calculation (NOAEL -> HED -> MRSD)")
    print(sep)
    print(f"\n  Step 1: NOAEL")
    print(f"    Species:          {result.species}")
    print(f"    NOAEL:            {result.noael_mg_kg} mg/kg")
    print(f"\n  Step 2: HED (Body Surface Area scaling)")
    print(f"    Conversion factor (Km_human/Km_{result.species}): "
          f"1/{BSA_CONVERSION_FACTORS.get(result.species.lower(), '?')}")
    print(f"    HED = {result.noael_mg_kg} / "
          f"{BSA_CONVERSION_FACTORS.get(result.species.lower(), '?')} "
          f"= {result.hed_mg_kg} mg/kg")
    print(f"\n  Step 3: MRSD (with safety factor)")
    print(f"    Safety factor:    1/{int(result.safety_factor)}")
    print(f"    MRSD = {result.hed_mg_kg} / {int(result.safety_factor)} "
          f"= {result.mrsd_mg_kg} mg/kg")
    print(f"    MRSD = {result.mrsd_mg_kg} x {result.body_weight_kg} kg "
          f"= {result.mrsd_mg} mg")
    print(f"    MRSD (rounded):   {result.mrsd_mg_rounded} mg")
    print(f"\n{sep}\n")


def print_mabel_result(result: MABELResult) -> None:
    """Pretty-print a MABEL calculation result."""
    sep = "=" * 60
    print(f"\n{sep}")
    print("  MABEL Calculation")
    print(sep)
    print(f"\n  EC50:               {result.ec50}")
    print(f"  Target occupancy:   {result.target_occupancy * 100:.0f}%")
    print(f"  MABEL = {result.target_occupancy} x {result.ec50} / "
          f"(1 - {result.target_occupancy}) = {result.mabel}")
    print(f"\n  Note: MABEL should be further refined using integrated")
    print(f"  PK/PD modelling and cross-species pharmacology data.")
    print(f"\n{sep}\n")


if __name__ == "__main__":
    # Example 1: Small molecule — MRSD from rat NOAEL
    print("=" * 60)
    print("  Example 1: Small molecule MRSD from rat NOAEL")
    print("=" * 60)
    print("\n  Scenario: Novel compound XYZ-001")
    print("  28-day GLP toxicity study in rats")
    print("  NOAEL = 30 mg/kg/day\n")

    rat_result = calculate_mrsd(
        noael_mg_kg=30.0,
        species="rat",
        safety_factor=10.0,
        body_weight_kg=60.0,
    )
    print_mrsd_result(rat_result)

    # Example 2: Same compound — MRSD from dog NOAEL
    print("  Example 2: Same compound, dog toxicity study")
    print("  NOAEL = 10 mg/kg/day\n")

    dog_result = calculate_mrsd(
        noael_mg_kg=10.0,
        species="dog",
        safety_factor=10.0,
        body_weight_kg=60.0,
    )
    print_mrsd_result(dog_result)

    # Compare and select the more conservative (lower) MRSD
    print("  Comparison of MRSD from different species:")
    print(f"    Rat NOAEL 30 mg/kg  -> MRSD = {rat_result.mrsd_mg} mg")
    print(f"    Dog NOAEL 10 mg/kg  -> MRSD = {dog_result.mrsd_mg} mg")
    most_conservative = min(rat_result.mrsd_mg, dog_result.mrsd_mg)
    print(f"    -> Select the LOWER value: {most_conservative} mg\n")

    # Example 3: MABEL for a biologic
    print("=" * 60)
    print("  Example 3: MABEL for a monoclonal antibody")
    print("=" * 60)
    print("\n  EC50 from in vitro receptor binding = 100 ng/mL")
    print("  Target occupancy for MABEL = 10%\n")

    mabel_result = calculate_mabel(ec50=100.0, target_occupancy=0.10)
    print_mabel_result(mabel_result)
