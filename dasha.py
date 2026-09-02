"""
Vimshottari Dasha Calculator
Calculates Mahadasha, Antardasha (Bhukti), and Pratyantardasha
based on Moon's nakshatra position at birth.
"""

from datetime import datetime, timedelta

# Dasha sequence and periods (years)
DASHA_SEQUENCE = [
    ("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10),
    ("Mars", 7), ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19),
    ("Mercury", 17),
]
TOTAL_YEARS = 120

NAKSHATRA_SPAN = 13.333333333  # degrees per nakshatra

# Nakshatra to starting dasha lord mapping
NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
]


def compute_vimshottari_dasha(moon_longitude: float, birth_date: str) -> list:
    """Compute Vimshottari Mahadasha and Antardasha periods.

    Args:
        moon_longitude: Moon's sidereal longitude (0-360)
        birth_date: "YYYY-MM-DD"

    Returns:
        List of Mahadasha periods with nested Antardasha
    """
    dt_parts = birth_date.split("-")
    birth_dt = datetime(int(dt_parts[0]), int(dt_parts[1]), int(dt_parts[2]))

    # Find current nakshatra
    nak_index = int(moon_longitude / NAKSHATRA_SPAN)
    nak_index = min(nak_index, 26)

    # Starting dasha lord
    start_lord = NAKSHATRA_LORDS[nak_index]

    # Calculate elapsed portion of current dasha at birth
    degree_in_nak = moon_longitude % NAKSHATRA_SPAN
    fraction_elapsed = degree_in_nak / NAKSHATRA_SPAN

    # Find position in dasha sequence
    start_idx = next(
        i for i, (lord, _) in enumerate(DASHA_SEQUENCE)
        if lord == start_lord
    )

    # Calculate remaining period of first dasha
    first_lord, first_years = DASHA_SEQUENCE[start_idx]
    remaining_years = first_years * (1 - fraction_elapsed)

    # Build Mahadasha periods
    dashas = []
    current_date = birth_dt

    for cycle in range(2):  # Go through 2 full cycles to cover 240 years
        for offset in range(9):
            idx = (start_idx + offset) % 9
            lord, total_years = DASHA_SEQUENCE[idx]

            if cycle == 0 and offset == 0:
                years = remaining_years
            else:
                years = total_years

            days = years * 365.25
            end_date = current_date + timedelta(days=days)

            # Calculate Antardashas within this Mahadasha
            antardashas = _compute_antardashas(
                lord, idx, years, current_date
            )

            dashas.append({
                "lord": lord,
                "years": round(years, 2),
                "total_years": total_years,
                "start": current_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
                "antardashas": antardashas,
            })

            current_date = end_date

            # Stop after sufficient coverage
            if current_date > birth_dt + timedelta(days=120 * 365.25):
                return dashas

    return dashas


def _compute_antardashas(
    maha_lord: str,
    maha_idx: int,
    maha_years: float,
    maha_start: datetime,
) -> list:
    """Compute Antardasha (Bhukti) periods within a Mahadasha.

    Antardasha sequence starts with the Mahadasha lord itself,
    then follows the Vimshottari sequence.
    """
    antardashas = []
    current_date = maha_start

    for offset in range(9):
        idx = (maha_idx + offset) % 9
        antar_lord, antar_total_years = DASHA_SEQUENCE[idx]

        # Antardasha duration = (Mahadasha years × Antardasha years) / 120
        # But proportioned to actual Mahadasha duration
        proportion = antar_total_years / TOTAL_YEARS
        antar_years = maha_years * proportion
        antar_days = antar_years * 365.25

        end_date = current_date + timedelta(days=antar_days)

        antardashas.append({
            "lord": antar_lord,
            "years": round(antar_years, 2),
            "start": current_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
        })

        current_date = end_date

    return antardashas


def get_current_dasha(dashas: list, check_date: str = None) -> dict:
    """Find which Mahadasha and Antardasha is active on a given date."""
    if check_date:
        dt = datetime.strptime(check_date, "%Y-%m-%d")
    else:
        dt = datetime.now()

    for dasha in dashas:
        start = datetime.strptime(dasha["start"], "%Y-%m-%d")
        end = datetime.strptime(dasha["end"], "%Y-%m-%d")

        if start <= dt <= end:
            current_antar = None
            for antar in dasha["antardashas"]:
                a_start = datetime.strptime(antar["start"], "%Y-%m-%d")
                a_end = datetime.strptime(antar["end"], "%Y-%m-%d")
                if a_start <= dt <= a_end:
                    current_antar = antar
                    break

            return {
                "mahadasha": dasha["lord"],
                "mahadasha_start": dasha["start"],
                "mahadasha_end": dasha["end"],
                "antardasha": current_antar["lord"] if current_antar else None,
                "antardasha_start": current_antar["start"] if current_antar else None,
                "antardasha_end": current_antar["end"] if current_antar else None,
            }

    return {"mahadasha": "Unknown", "antardasha": "Unknown"}
