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

    for d in doshas:
        d_name = d["name"]
        if "Mangal" in d_name:
            d["name_hi"] = "मांगलिक दोष (मंगल दोष)"
            d["description_hi"] = (
                f"लग्न से भाव {d.get('house', '')} में मंगल स्थित है। " +
                ("यह प्रबल मांगलिक दोष है।" if d.get("severity") == "high" else "यह आंशिक मांगलिक दोष है।")
                if d.get("present") else f"मंगल भाव {d.get('house', '')} में स्थित है। कुण्डली में मांगलिक दोष उपस्थित नहीं है।"
            )
            d["effects_hi"] = "विवाह में विलंब अथवा वैवाहिक जीवन में मतभेद की संभावना। ऊर्जा को सकारात्मक दिशा में लगाना आवश्यक है।"
            d["remedies_hi"] = [
                "मंगलवार को मंगल शांति पूजा अथवा रुद्राभिषेक कराएं",
                "नित्य अथवा मंगलवार को श्री हनुमान चालीसा का पाठ करें",
                "ज्योतिषीय परामर्श के उपरांत शुद्ध मूंगा रत्न धारण करें",
                "मांगलिक जातक से विवाह करने पर दोष का स्वतः परिहार हो जाता है",
            ]
            if d.get("cancellation"):
                d["cancellation_hi"] = "शुभ ग्रहों के प्रभाव व शुभ दृष्टि से मांगलिक दोष का परिहार होता है"
        elif "Kaal Sarp" in d_name:
            d["name_hi"] = "कालसर्प दोष"
            d["description_hi"] = (
                "समस्त ग्रह राहु और केतु की धुरी के एक तरफ स्थित हैं। यह कालसर्प दोष है।"
                if d.get("present") else "समस्त ग्रह राहु-केतु अक्ष से मुक्त हैं। कुण्डली में कालसर्प दोष उपस्थित नहीं है।"
            )
            d["effects_hi"] = "जीवन में अप्रत्याशित उतार-चढ़ाव, कार्यों में विलंब और संघर्ष की स्थिति। 33-36 वर्ष की आयु के उपरांत प्रभाव में भारी कमी आती है।"
            d["remedies_hi"] = [
                "त्र्यंबकेश्वर अथवा महाकालेश्वर में कालसर्प दोष निवारण पूजा कराएं",
                "प्रति शनिवार 'ॐ रां राहवे नमः' मंत्र का जाप करें",
                "नाग पंचमी पर नाग-नागिन के चांदी के जोड़े की पूजा कर जल प्रवाहित करें",
                "घर में चांदी का नाग स्थापित कर नित्य दर्शन करें",
            ]
        elif "Pitra" in d_name:
            d["name_hi"] = "पितृ दोष"
            d["description_hi"] = (
                "कुण्डली में पितृ ऋण एवं पूर्वजों के कर्मों से संबंधित प्रभाव उपस्थित हैं।"
                if d.get("present") else "कुण्डली में कोई गंभीर पितृ दोष उपस्थित नहीं है।"
            )
            d["effects_hi"] = "पूर्वजों के ऋण या पितरों की अप्रसन्नता से वंश वृद्धि, पिता के स्वास्थ्य अथवा करियर में रुकावटें आ सकती हैं।"
            d["remedies_hi"] = [
                "पितृ पक्ष में पितरों के निमित्त तर्पण एवं पिंडदान करें",
                "प्रत्येक अमावस्या को ब्राह्मणों या जरूरतमंदों को भोजन व वस्त्र दान करें",
                "प्रतिदिन प्रातः तांबे के लोटे से सूर्य देव को अर्घ्य दें और सूर्य गायत्री का जाप करें",
                "पीपल का वृक्ष लगाकर उसकी नियमित सेवा व जलार्पण करें",
            ]
        elif "Grahan" in d_name:
            is_surya = "Surya" in d_name
            d["name_hi"] = "सूर्य ग्रहण दोष" if is_surya else "चन्द्र ग्रहण दोष"
            d["description_hi"] = (
                "सूर्य राहु/केतु से पीड़ित होकर ग्रहण दोष का निर्माण कर रहा है।"
                if is_surya else "चंद्रमा राहु/केतु से पीड़ित होकर ग्रहण दोष का निर्माण कर रहा है।"
            )
            d["effects_hi"] = (
                "आत्मविश्वास में कमी, पिता से मतभेद अथवा स्वास्थ्य समस्याएं।"
                if is_surya else "मानसिक अशांति, अत्यधिक भावुकता अथवा अनिद्रा की स्थिति।"
            )
            d["remedies_hi"] = [
                "नित्य आदित्य हृदय स्तोत्र का पाठ करें व सूर्य को अर्घ्य दें" if is_surya else "प्रति सोमवार शिवलिंग पर कच्चा दूध व जल अर्पित करें",
                "रविवार को गेहूं या तांबे का दान करें" if is_surya else "सोमवार को चावल या दूध का दान करें",
            ]
        elif "Kemdrum" in d_name:
            d["name_hi"] = "केमद्रुम दोष"
            d["description_hi"] = (
                "चंद्रमा के दोनों ओर (द्वितीय व द्वादश भाव में) कोई ग्रह न होने से केमद्रुम योग बनता है।"
                if d.get("present") else "चंद्रमा के समीप शुभ ग्रह उपस्थित हैं, केमद्रुम दोष नहीं है।"
            )
            d["effects_hi"] = "मानसिक एकाकीपन, आर्थिक उतार-चढ़ाव और जीवन में भावनात्मक अस्थिरता की स्थिति।"
            d["remedies_hi"] = [
                "भगवान शिव और माता पार्वती की संयुक्त आराधना करें",
                "पूर्णिमा का व्रत रखें और चंद्रमा को अर्घ्य दें",
                "चांदी का चौकोर टुकड़ा अपने पास रखें",
            ]
            if d.get("cancellation"):
                d["cancellation_hi"] = "चंद्रमा के केंद्र में होने अथवा शुभ ग्रह की युति से दोष निष्फल हो गया है"
        elif "Vish Yoga" in d_name:
            d["name_hi"] = "विष योग (शनि-चन्द्र)"
            d["description_hi"] = "शनि और चंद्रमा की युति से विष योग बनता है।"
            d["effects_hi"] = "मानसिक तनाव, कार्यों में विलंब और भावनात्मक संवेदनशीलता।"
            d["remedies_hi"] = [
                "प्रति शनिवार शनि मंदिर में सरसों के तेल का दीपक जलाएं",
                "हनुमान चालीसा का नियमित पाठ करें",
                "सोमवार और शनिवार को भगवान शिव का जलाभिषेक करें",
            ]

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

    # Jupiter aspects Mars (Mars in the 5th, 7th or 9th house counted from Jupiter)
    jupiter = _planet_by_name(planets, "Jupiter")
    if jupiter:
        dist = ((mars["house"] - jupiter["house"]) % 12) + 1
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
