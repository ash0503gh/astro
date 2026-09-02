"""
Vedic Astrology Dosha Detection
Identifies Mangal Dosha, Kaal Sarp Dosha, Pitra Dosha, and others.
"""


def _planet_by_name(planets: list, name: str) -> dict:
    return next((p for p in planets if p["name"] == name), None)


def detect_doshas(planets: list, houses: list) -> list:
    """Detect all significant doshas in the birth chart."""
    doshas = []

    doshas.extend(_check_mangal_dosha(planets))
    doshas.extend(_check_kaal_sarp_dosha(planets))
    doshas.extend(_check_pitra_dosha(planets, houses))
    doshas.extend(_check_grahan_dosha(planets))
    doshas.extend(_check_kemdrum_dosha(planets))
    doshas.extend(_check_shani_dosha(planets))

    return doshas


def _check_mangal_dosha(planets: list) -> list:
    """Mangal (Manglik) Dosha: Mars in houses 1, 2, 4, 7, 8, or 12 from Lagna."""
    mars = _planet_by_name(planets, "Mars")
    if not mars:
        return []

    manglik_houses = [1, 2, 4, 7, 8, 12]
    doshas = []

    if mars["house"] in manglik_houses:
        severity = "high" if mars["house"] in [7, 8] else "moderate"

        # Check for cancellation conditions
        cancellation = _check_mangal_cancellation(planets, mars)

        doshas.append({
            "name": "Mangal Dosha (Manglik)",
            "present": True,
            "severity": severity if not cancellation else "cancelled",
            "house": mars["house"],
            "description": (
                f"Mars is in House {mars['house']} from the Ascendant. "
                f"{'This is a strong Mangal Dosha.' if severity == 'high' else 'Partial Mangal Dosha.'}"
            ),
            "effects": (
                "Can cause delays or challenges in marriage and partnerships. "
                "High energy needs constructive channeling."
            ),
            "remedies": [
                "Perform Mangal Shanti Puja",
                "Chant Hanuman Chalisa on Tuesdays",
                "Wear a coral gemstone (after consulting an astrologer)",
                "Manglik-Manglik marriage can neutralize effects",
            ],
            "cancellation": cancellation,
        })
    else:
        doshas.append({
            "name": "Mangal Dosha (Manglik)",
            "present": False,
            "severity": "none",
            "description": f"Mars is in House {mars['house']}. No Mangal Dosha present.",
        })

    return doshas


def _check_mangal_cancellation(planets: list, mars: dict) -> str:
    """Check if Mangal Dosha is cancelled."""
    cancellations = []

    # Mars in own sign (Aries/Scorpio) or exalted (Capricorn)
    if mars["dignity"] in ("own_sign", "exalted"):
        cancellations.append(
            f"Mars is in {mars['dignity'].replace('_', ' ')} ({mars['sign']}), reducing dosha effects"
        )

    # Jupiter aspects Mars (Jupiter in 1, 5, 7, 9 from Mars)
    jupiter = _planet_by_name(planets, "Jupiter")
    if jupiter:
        dist = ((jupiter["house"] - mars["house"]) % 12) or 12
        if dist in [5, 7, 9]:  # Jupiter's special aspects
            cancellations.append("Jupiter aspects Mars, providing cancellation")

    # Venus or Jupiter in 7th house
    for name in ["Venus", "Jupiter"]:
        p = _planet_by_name(planets, name)
        if p and p["house"] == 7:
            cancellations.append(f"{name} in 7th house reduces Mangal Dosha")

    return "; ".join(cancellations) if cancellations else ""


def _check_kaal_sarp_dosha(planets: list) -> list:
    """Kaal Sarp Dosha: All planets hemmed between Rahu and Ketu."""
    rahu = _planet_by_name(planets, "Rahu")
    ketu = _planet_by_name(planets, "Ketu")
    if not rahu or not ketu:
        return []

    rahu_lon = rahu["longitude"]
    ketu_lon = ketu["longitude"]

    # Check if all other planets are on one side of the Rahu-Ketu axis
    other_planets = [p for p in planets if p["name"] not in ("Rahu", "Ketu")]

    # Planets between Rahu and Ketu (going forward from Rahu)
    between_count = 0
    for p in other_planets:
        lon = p["longitude"]
        if rahu_lon < ketu_lon:
            if rahu_lon <= lon <= ketu_lon:
                between_count += 1
        else:
            if lon >= rahu_lon or lon <= ketu_lon:
                between_count += 1

    all_between = between_count == len(other_planets)
    all_outside = between_count == 0

    if all_between or all_outside:
        # Determine type based on Rahu's house
        ksp_types = {
            1: "Anant", 2: "Kulik", 3: "Vasuki", 4: "Shankhpal",
            5: "Padma", 6: "Mahapadma", 7: "Takshak", 8: "Karkotak",
            9: "Shankhchud", 10: "Ghatak", 11: "Vishdhar", 12: "Sheshnag",
        }
        ksp_name = ksp_types.get(rahu["house"], "")

        return [{
            "name": "Kaal Sarp Dosha",
            "present": True,
            "severity": "high",
            "subtype": f"{ksp_name} Kaal Sarp" if ksp_name else "Kaal Sarp",
            "description": (
                f"All planets are hemmed between Rahu (House {rahu['house']}) "
                f"and Ketu (House {ketu['house']}). "
                f"This is {ksp_name} Kaal Sarp Dosha."
            ),
            "effects": (
                "Can bring sudden ups and downs, karmic patterns, "
                "obstacles that transform into growth. "
                "Effects reduce after age 33-36."
            ),
            "remedies": [
                "Perform Kaal Sarp Dosha Puja at Trimbakeshwar",
                "Chant Rahu mantra on Saturdays",
                "Visit Nag temple and offer milk",
                "Keep a silver snake idol at home",
            ],
        }]

    return [{
        "name": "Kaal Sarp Dosha",
        "present": False,
        "severity": "none",
        "description": "Planets are not hemmed between Rahu-Ketu axis. No Kaal Sarp Dosha.",
    }]


def _check_pitra_dosha(planets: list, houses: list) -> list:
    """Pitra Dosha: Sun conjunct/aspected by Rahu, or Sun in 9th with malefics."""
    sun = _planet_by_name(planets, "Sun")
    rahu = _planet_by_name(planets, "Rahu")
    if not sun or not rahu:
        return []

    dosha_present = False
    reasons = []

    # Sun conjunct Rahu
    if sun["sign_num"] == rahu["sign_num"]:
        dosha_present = True
        reasons.append(f"Sun conjunct Rahu in {sun['sign']}")

    # Sun in 9th house with malefic influence
    if sun["house"] == 9:
        malefics = ["Mars", "Saturn", "Rahu", "Ketu"]
        for m in malefics:
            mp = _planet_by_name(planets, m)
            if mp and mp["house"] == 9 and m != "Sun":
                dosha_present = True
                reasons.append(f"Sun in 9th house with {m}")

    # 9th lord afflicted
    house_9 = next((h for h in houses if h["house"] == 9), None)
    if house_9:
        lord_9 = _planet_by_name(planets, house_9["lord"])
        if lord_9:
            for m in ["Rahu", "Ketu", "Saturn"]:
                mp = _planet_by_name(planets, m)
                if mp and mp["sign_num"] == lord_9["sign_num"]:
                    dosha_present = True
                    reasons.append(f"9th lord {house_9['lord']} conjunct {m}")

    if dosha_present:
        return [{
            "name": "Pitra Dosha",
            "present": True,
            "severity": "moderate",
            "description": f"Ancestral karma patterns detected: {'; '.join(reasons)}.",
            "effects": (
                "May indicate unresolved ancestral karma. "
                "Can affect father's wellbeing, career obstacles, or delayed results."
            ),
            "remedies": [
                "Perform Pitra Tarpan during Pitru Paksha",
                "Donate food to Brahmins on Amavasya",
                "Chant Surya mantra daily",
                "Plant a Peepal tree and water it regularly",
            ],
        }]

    return [{
        "name": "Pitra Dosha",
        "present": False,
        "severity": "none",
        "description": "No significant Pitra Dosha found.",
    }]


def _check_grahan_dosha(planets: list) -> list:
    """Grahan Dosha: Sun or Moon conjunct Rahu or Ketu (eclipse yoga)."""
    doshas = []
    luminaries = [("Sun", "Surya Grahan"), ("Moon", "Chandra Grahan")]

    for lum_name, dosha_name in luminaries:
        lum = _planet_by_name(planets, lum_name)
        if not lum:
            continue

        for node in ["Rahu", "Ketu"]:
            node_p = _planet_by_name(planets, node)
            if node_p and lum["sign_num"] == node_p["sign_num"]:
                # Check degree proximity for severity
                deg_diff = abs(lum["longitude"] - node_p["longitude"])
                if deg_diff > 180:
                    deg_diff = 360 - deg_diff
                severity = "high" if deg_diff < 10 else "moderate"

                doshas.append({
                    "name": f"{dosha_name} Dosha",
                    "present": True,
                    "severity": severity,
                    "description": (
                        f"{lum_name} conjunct {node} in {lum['sign']}. "
                        f"Eclipse-like energy affecting the {lum_name}'s significations."
                    ),
                    "effects": (
                        f"{'Challenges with authority, father, vitality' if lum_name == 'Sun' else 'Emotional turbulence, mother-related concerns, mental restlessness'}. "
                        f"Periodic intensity in {lum_name}-related matters."
                    ),
                    "remedies": [
                        f"Chant {lum_name} beej mantra",
                        f"Donate items associated with {lum_name} on its day",
                        f"Perform {node} shanti puja",
                    ],
                })

    return doshas


def _check_kemdrum_dosha(planets: list) -> list:
    """Kemdrum Dosha: Moon with no planets in 2nd or 12th from it."""
    moon = _planet_by_name(planets, "Moon")
    if not moon:
        return []

    moon_house = moon["house"]
    house_2_from_moon = ((moon_house) % 12) + 1  # next house
    house_12_from_moon = ((moon_house - 2) % 12) + 1  # previous house

    # Exclude Rahu, Ketu, Sun from count (traditional)
    real_planets = [p for p in planets if p["name"] not in ("Rahu", "Ketu", "Sun", "Moon")]

    adjacent = [
        p for p in real_planets
        if p["house"] in (house_2_from_moon, house_12_from_moon)
    ]

    if not adjacent:
        # Check cancellation: Moon in Kendra or with Jupiter
        cancellation = ""
        if moon["house"] in [1, 4, 7, 10]:
            cancellation = "Moon in Kendra cancels Kemdrum Dosha"
        jupiter = _planet_by_name(planets, "Jupiter")
        if jupiter and jupiter["sign_num"] == moon["sign_num"]:
            cancellation = "Jupiter conjunct Moon cancels Kemdrum Dosha"

        return [{
            "name": "Kemdrum Dosha",
            "present": True,
            "severity": "moderate" if not cancellation else "cancelled",
            "description": (
                "No planets in 2nd or 12th house from Moon. "
                "Moon is isolated without planetary support."
            ),
            "effects": "May bring periods of loneliness, financial fluctuation, or emotional isolation.",
            "remedies": [
                "Chant Chandra beej mantra on Mondays",
                "Wear a pearl or moonstone",
                "Fast on Mondays",
                "Offer milk and water to Shivling",
            ],
            "cancellation": cancellation,
        }]

    return [{
        "name": "Kemdrum Dosha",
        "present": False,
        "severity": "none",
        "description": "Moon has planetary support in adjacent houses. No Kemdrum Dosha.",
    }]


def _check_shani_dosha(planets: list) -> list:
    """Check Saturn-related afflictions."""
    saturn = _planet_by_name(planets, "Saturn")
    if not saturn:
        return []

    issues = []

    # Saturn in 1st, 4th, 7th, 8th, or 10th can be challenging
    challenging_houses = [1, 4, 7, 8]
    if saturn["house"] in challenging_houses and saturn["dignity"] == "debilitated":
        issues.append(f"Debilitated Saturn in House {saturn['house']}")

    # Saturn conjunct Moon (Vish Yoga)
    moon = _planet_by_name(planets, "Moon")
    if moon and saturn["sign_num"] == moon["sign_num"]:
        return [{
            "name": "Vish Yoga (Saturn-Moon)",
            "present": True,
            "severity": "moderate",
            "description": f"Saturn conjunct Moon in {saturn['sign']}. Can bring emotional heaviness and delays.",
            "effects": "Mental stress, delayed success, karmic lessons through emotional experiences.",
            "remedies": [
                "Chant Shani mantra on Saturdays",
                "Donate black sesame and mustard oil on Saturdays",
                "Wear a blue sapphire only after proper consultation",
                "Serve elderly people and workers",
            ],
        }]

    return []
