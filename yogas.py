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

    for y in unique:
        y_name = y["name"]
        if "Ruchaka" in y_name:
            y["name_hi"] = "रुचक योग (पंच महापुरुष)"
            y["type_hi"] = "साहस एवं नेतृत्व"
            y["description_hi"] = "मंगल केंद्र भाव में स्वराशि अथवा उच्च होकर रुचक महापुरुष योग बनाता है। यह अदम्य पराक्रम, साहस और उच्च नेतृत्व शक्ति प्रदान करता है।"
            y["strength_hi"] = "प्रबल"
        elif "Bhadra" in y_name:
            y["name_hi"] = "भद्र योग (पंच महापुरुष)"
            y["type_hi"] = "बुद्धि एवं मेधा"
            y["description_hi"] = "बुध केंद्र भाव में स्वराशि अथवा उच्च होकर भद्र महापुरुष योग बनाता है। यह कुशाग्र मेधा, वाणी का प्रभाव और व्यापार में सफलता प्रदान करता है।"
            y["strength_hi"] = "प्रबल"
        elif "Hamsa" in y_name:
            y["name_hi"] = "हंस योग (पंच महापुरुष)"
            y["type_hi"] = "ज्ञान एवं अध्यात्म"
            y["description_hi"] = "गुरु केंद्र भाव में स्वराशि अथवा उच्च होकर हंस महापुरुष योग बनाता है। यह उच्च ज्ञान, सदाचार और समाज में पूज्यता प्रदान करता है।"
            y["strength_hi"] = "प्रबल"
        elif "Malavya" in y_name:
            y["name_hi"] = "मालव्य योग (पंच महापुरुष)"
            y["type_hi"] = "ऐश्वर्य एवं कला"
            y["description_hi"] = "शुक्र केंद्र भाव में स्वराशि अथवा उच्च होकर मालव्य महापुरुष योग बनाता है। यह सौंदर्य, कलात्मक प्रतिभा, उत्तम वाहन और भौतिक सुख-सुविधाएं प्रदान करता है।"
            y["strength_hi"] = "प्रबल"
        elif "Shasha" in y_name:
            y["name_hi"] = "शश योग (पंच महापुरुष)"
            y["type_hi"] = "सत्ता एवं संगठन"
            y["description_hi"] = "शनि केंद्र भाव में स्वराशि अथवा उच्च होकर शश महापुरुष योग बनाता है। यह न्यायप्रियता, जन-समर्थन और स्थायी सत्ता प्रदान करता है।"
            y["strength_hi"] = "प्रबल"
        elif "Gajakesari" in y_name:
            y["name_hi"] = "गजकेसरी योग"
            y["type_hi"] = "धन एवं ज्ञान"
            y["description_hi"] = "चंद्रमा से केंद्र में गुरु स्थित होने से परम शुभ गजकेसरी योग का निर्माण होता है। यह ज्ञान, समृद्धि, अखंड यश और मान-सम्मान प्रदान करता है।"
            y["strength_hi"] = "प्रबल"
        elif "Budhaditya" in y_name:
            y["name_hi"] = "बुधादित्य योग"
            y["type_hi"] = "बुद्धि एवं विद्या"
            y["description_hi"] = "सूर्य और बुध की शुभ युति से बुधादित्य योग बनता है। यह कुशाग्र बौद्धिक क्षमता, प्रशासनिक योग्यता और उत्कृष्ट संचार कौशल प्रदान करता है।"
            y["strength_hi"] = "मध्यम"
        elif "Chandra-Mangal" in y_name:
            y["name_hi"] = "चन्द्र-मंगल योग"
            y["type_hi"] = "धन एवं समृद्धि"
            y["description_hi"] = "चंद्रमा और मंगल की युति से लक्ष्मी योग का सृजन होता है। यह जातक को उद्यमशील बनाता है और व्यापार व पुरुषार्थ द्वारा प्रचुर धनार्जन कराता है।"
            y["strength_hi"] = "मध्यम"
        elif "Dhana" in y_name:
            y["name_hi"] = "धन योग"
            y["type_hi"] = "धन एवं संपत्ति"
            y["description_hi"] = "धन भाव अथवा लाभ भाव के स्वामी की शुभ भाव में स्थिति धन संचय, वित्तीय स्थिरता और पैतृक संपत्ति का उत्तम लाभ प्रदान करती है।"
            y["strength_hi"] = "मध्यम"
        elif "Viparita" in y_name:
            y["name_hi"] = "विपरीत राजयोग"
            y["type_hi"] = "विपत्ति से विजय"
            y["description_hi"] = "त्रिक भावों (6, 8, 12) के स्वामियों की त्रिक भावों में ही स्थिति से विपरीत राजयोग बनता है। यह संकटों को अवसर में बदलकर अप्रत्याशित सफलता दिलाता है।"
            y["strength_hi"] = "मध्यम"
        elif "Neechabhanga" in y_name:
            y["name_hi"] = "नीचभंग राजयोग"
            y["type_hi"] = "दोष परिहार व राजयोग"
            y["description_hi"] = "नीच राशि में स्थित ग्रह के नीचत्व का भंग होकर अत्यंत शुभ राजयोग बनता है। यह प्रारंभिक संघर्षों के बाद असाधारण सफलता दिलाता है।"
            y["strength_hi"] = "प्रबल"
        elif "Adhi" in y_name:
            y["name_hi"] = "अधि योग"
            y["type_hi"] = "नेतृत्व एवं प्रभाव"
            y["description_hi"] = "चंद्रमा से 6, 7 और 8वें भावों में शुभ ग्रहों की स्थिति से अधि योग का निर्माण होता है। यह उत्कृष्ट नेतृत्व क्षमता और उच्च सामाजिक प्रतिष्ठा प्रदान करता है।"
            y["strength_hi"] = "प्रबल"
        elif "Saraswati" in y_name:
            y["name_hi"] = "सरस्वती योग"
            y["type_hi"] = "विद्या एवं ललित कला"
            y["description_hi"] = "बृहस्पति, शुक्र और बुध की शुभ स्थिति से सरस्वती योग बनता है। यह विद्या, संगीत, काव्य, लेखन और वाकपटुता में असाधारण सिद्धि प्रदान करता है।"
            y["strength_hi"] = "प्रबल"
        elif "Raj" in y_name:
            y["name_hi"] = "राजयोग"
            y["type_hi"] = "सत्ता एवं प्रतिष्ठा"
            y["description_hi"] = "केंद्र और त्रिकोण भावों के स्वामियों के शुभ संबंध से शक्तिशाली राजयोग बनता है। यह उच्च पद, सत्ता, अधिकार और मान-सम्मान दिलाता है।"
            y["strength_hi"] = "प्रबल"

    return unique
