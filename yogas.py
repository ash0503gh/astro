"""
Vedic Astrology Yoga Detection
Identifies important planetary combinations (yogas) in the birth chart.
"""

KENDRA_HOUSES = [1, 4, 7, 10]
TRIKONA_HOUSES = [1, 5, 9]
DUSTHANA_HOUSES = [6, 8, 12]
UPACHAYA_HOUSES = [3, 6, 10, 11]

# Panch Mahapurusha planets and their names
MAHAPURUSHA = {
    "Mars": "Ruchaka",
    "Mercury": "Bhadra",
    "Jupiter": "Hamsa",
    "Venus": "Malavya",
    "Saturn": "Shasha",
}


def _planet_by_name(planets: list, name: str) -> dict:
    """Get planet data by name."""
    return next((p for p in planets if p["name"] == name), None)


def _planets_in_house(planets: list, house: int) -> list:
    """Get all planets in a specific house."""
    return [p for p in planets if p["house"] == house]


def _is_conjunct(p1: dict, p2: dict) -> bool:
    """Check if two planets are in the same sign (conjunct)."""
    return p1["sign_num"] == p2["sign_num"]


def _houses_apart(house1: int, house2: int) -> int:
    """Calculate house distance (1-12)."""
    return ((house2 - house1) % 12) or 12


def detect_yogas(planets: list, houses: list, ascendant: dict) -> list:
    """Detect all significant yogas in the chart.

    Returns list of yoga dicts with name, description, strength, involved planets.
    """
    yogas = []

    # --- Panch Mahapurusha Yogas ---
    for planet_name, yoga_name in MAHAPURUSHA.items():
        p = _planet_by_name(planets, planet_name)
        if p and p["house"] in KENDRA_HOUSES:
            if p["dignity"] in ("own_sign", "exalted"):
                yogas.append({
                    "name": f"{yoga_name} Yoga",
                    "type": "Panch Mahapurusha",
                    "planets": [planet_name],
                    "description": f"{planet_name} in own/exalted sign in Kendra (House {p['house']}). "
                                   f"Grants strength, authority, and the qualities of {planet_name}.",
                    "strength": "strong",
                    "category": "benefic",
                })

    # --- Gajakesari Yoga ---
    moon = _planet_by_name(planets, "Moon")
    jupiter = _planet_by_name(planets, "Jupiter")
    if moon and jupiter:
        dist = _houses_apart(moon["house"], jupiter["house"])
        if dist in [1, 4, 7, 10]:
            yogas.append({
                "name": "Gajakesari Yoga",
                "type": "Wealth & Wisdom",
                "planets": ["Moon", "Jupiter"],
                "description": "Jupiter in Kendra from Moon. Grants wisdom, wealth, "
                               "fame, and a good reputation. One of the most auspicious yogas.",
                "strength": "strong",
                "category": "benefic",
            })

    # --- Budhaditya Yoga ---
    sun = _planet_by_name(planets, "Sun")
    mercury = _planet_by_name(planets, "Mercury")
    if sun and mercury and _is_conjunct(sun, mercury):
        if mercury.get("dignity") != "debilitated":
            yogas.append({
                "name": "Budhaditya Yoga",
                "type": "Intelligence",
                "planets": ["Sun", "Mercury"],
                "description": "Sun-Mercury conjunction. Grants sharp intellect, "
                               "communication skills, and academic excellence.",
                "strength": "moderate",
                "category": "benefic",
            })

    # --- Chandra-Mangal Yoga ---
    mars = _planet_by_name(planets, "Mars")
    if moon and mars and _is_conjunct(moon, mars):
        yogas.append({
            "name": "Chandra-Mangal Yoga",
            "type": "Wealth",
            "planets": ["Moon", "Mars"],
            "description": "Moon-Mars conjunction. Brings wealth through enterprise, "
                           "courage, and bold ventures.",
            "strength": "moderate",
            "category": "benefic",
        })

    # --- Dhana Yoga (Wealth) ---
    # Lord of 2nd or 11th in Kendra or Trikona
    for h in houses:
        if h["house"] in [2, 11]:
            lord_name = h["lord"]
            lord_planet = _planet_by_name(planets, lord_name)
            if lord_planet and lord_planet["house"] in (KENDRA_HOUSES + TRIKONA_HOUSES):
                yogas.append({
                    "name": "Dhana Yoga",
                    "type": "Wealth",
                    "planets": [lord_name],
                    "description": f"Lord of House {h['house']} ({lord_name}) placed in "
                                   f"House {lord_planet['house']}. Indicates wealth accumulation.",
                    "strength": "moderate",
                    "category": "benefic",
                })

    # --- Raj Yoga ---
    # Conjunction or mutual aspect of Kendra and Trikona lords
    kendra_lords = set()
    trikona_lords = set()
    for h in houses:
        if h["house"] in KENDRA_HOUSES:
            kendra_lords.add(h["lord"])
        if h["house"] in TRIKONA_HOUSES:
            trikona_lords.add(h["lord"])

    raj_pairs = kendra_lords & trikona_lords  # Lords ruling both
    for lord_name in raj_pairs:
        lord_planet = _planet_by_name(planets, lord_name)
        if lord_planet:
            yogas.append({
                "name": "Raj Yoga",
                "type": "Power & Status",
                "planets": [lord_name],
                "description": f"{lord_name} rules both Kendra and Trikona houses. "
                               f"Grants power, authority, leadership, and social status.",
                "strength": "strong",
                "category": "benefic",
            })

    # Check for conjunction of separate Kendra and Trikona lords
    for k_lord in kendra_lords - trikona_lords:
        k_planet = _planet_by_name(planets, k_lord)
        if not k_planet:
            continue
        for t_lord in trikona_lords - kendra_lords:
            t_planet = _planet_by_name(planets, t_lord)
            if not t_planet:
                continue
            if k_planet and t_planet and _is_conjunct(k_planet, t_planet):
                yogas.append({
                    "name": "Raj Yoga",
                    "type": "Power & Status",
                    "planets": [k_lord, t_lord],
                    "description": f"Kendra lord ({k_lord}) conjunct Trikona lord ({t_lord}). "
                                   f"Powerful combination for success and recognition.",
                    "strength": "strong",
                    "category": "benefic",
                })

    # --- Viparita Raj Yoga ---
    # Lords of 6, 8, 12 placed in other dusthana houses
    dusthana_lords_in_dusthana = []
    for h in houses:
        if h["house"] in DUSTHANA_HOUSES:
            lord_planet = _planet_by_name(planets, h["lord"])
            if lord_planet and lord_planet["house"] in DUSTHANA_HOUSES:
                dusthana_lords_in_dusthana.append(h)

    if len(dusthana_lords_in_dusthana) >= 2:
        yogas.append({
            "name": "Viparita Raj Yoga",
            "type": "Overcoming Adversity",
            "planets": [h["lord"] for h in dusthana_lords_in_dusthana],
            "description": "Dusthana lords placed in dusthana houses. "
                           "Adversity transforms into advantage. Success through unconventional paths.",
            "strength": "moderate",
            "category": "benefic",
        })

    # --- Neechabhanga Raj Yoga ---
    # Debilitated planet gets cancellation
    for p in planets:
        if p["dignity"] == "debilitated":
            sign_lord = p.get("lord", "")
            sign_lord_planet = _planet_by_name(planets, sign_lord)
            if sign_lord_planet and sign_lord_planet["house"] in KENDRA_HOUSES:
                yogas.append({
                    "name": "Neechabhanga Raj Yoga",
                    "type": "Cancellation of Debilitation",
                    "planets": [p["name"], sign_lord],
                    "description": f"{p['name']}'s debilitation is cancelled because "
                                   f"sign lord {sign_lord} is in Kendra. "
                                   f"Turns weakness into exceptional strength.",
                    "strength": "strong",
                    "category": "benefic",
                })

    # --- Adhi Yoga ---
    # Benefics (Jupiter, Venus, Mercury) in 6, 7, 8 from Moon
    if moon:
        benefic_names = ["Jupiter", "Venus", "Mercury"]
        benefics_in_678 = []
        for bn in benefic_names:
            bp = _planet_by_name(planets, bn)
            if bp:
                dist = _houses_apart(moon["house"], bp["house"])
                if dist in [6, 7, 8]:
                    benefics_in_678.append(bn)
        if len(benefics_in_678) >= 2:
            yogas.append({
                "name": "Adhi Yoga",
                "type": "Leadership",
                "planets": benefics_in_678,
                "description": f"Benefics ({', '.join(benefics_in_678)}) in 6/7/8 from Moon. "
                               f"Grants leadership ability, polite conduct, and high status.",
                "strength": "strong",
                "category": "benefic",
            })

    # --- Saraswati Yoga ---
    # Jupiter, Venus, Mercury in Kendra/Trikona/2nd house
    good_houses = KENDRA_HOUSES + TRIKONA_HOUSES + [2]
    saraswati_planets = []
    for name in ["Jupiter", "Venus", "Mercury"]:
        p = _planet_by_name(planets, name)
        if p and p["house"] in good_houses:
            saraswati_planets.append(name)
    if len(saraswati_planets) == 3:
        yogas.append({
            "name": "Saraswati Yoga",
            "type": "Learning & Arts",
            "planets": saraswati_planets,
            "description": "Jupiter, Venus, and Mercury all in Kendra/Trikona/2nd house. "
                           "Exceptional talent in arts, learning, music, and speech.",
            "strength": "strong",
            "category": "benefic",
        })

    # Deduplicate
    seen = set()
    unique = []
    for y in yogas:
        key = (y["name"], tuple(sorted(y["planets"])))
        if key not in seen:
            seen.add(key)
            unique.append(y)

    return unique
