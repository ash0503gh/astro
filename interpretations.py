"""
Rule-Based Interpretations for Vedic Birth Charts
Provides basic readings for planet placements, house lordships, etc.
"""

ASC_READINGS = {
    "Mesha": "Bold, pioneering, and action-oriented. Natural leader with strong willpower and physical vitality. Can be impulsive but always ready to forge ahead.",
    "Vrishabha": "Stable, artistic, and wealth-conscious. Values comfort and security. Patient approach with a love for beauty, food, and material pleasures.",
    "Mithuna": "Curious, communicative, and versatile. Quick-witted with a love for learning and socializing. Adaptable but can be restless.",
    "Karka": "Nurturing, intuitive, and emotionally deep. Strong attachment to home and family. Protective nature with powerful intuition.",
    "Simha": "Regal, confident, and charismatic. Natural authority figure who seeks recognition. Generous and creative with a dramatic flair.",
    "Kanya": "Analytical, service-oriented, and detail-focused. Practical approach to life with strong organizational skills. Health-conscious.",
    "Tula": "Diplomatic, relationship-focused, and aesthetically inclined. Seeks balance and harmony. Strong sense of justice and partnership.",
    "Vrishchika": "Intense, transformative, and deeply perceptive. Strong willpower with an interest in hidden knowledge. Resilient through life's challenges.",
    "Dhanu": "Philosophical, optimistic, and dharma-oriented. Loves travel, higher learning, and spiritual pursuits. Naturally fortunate.",
    "Makara": "Ambitious, disciplined, and structured. Builds steadily toward long-term goals. Practical wisdom with a serious approach.",
    "Kumbha": "Innovative, humanitarian, and independent. Original thinker who values freedom and social causes. Unconventional approach.",
    "Meena": "Spiritual, compassionate, and imaginative. Deep connection to the unseen world. Artistic and empathetic with intuitive wisdom.",
}

PLANET_IN_HOUSE = {
    "Sun": {
        1: "Strong personality and leadership. Self-confident with natural authority. Good vitality.",
        2: "Wealth through government or authority. Family pride. Powerful speech.",
        3: "Courageous and bold. Good relationship with siblings. Success through effort.",
        4: "Status through property or vehicles. Connection to the homeland. Father figure at home.",
        5: "Creative intelligence. Love for drama and speculation. Blessed with wise children.",
        6: "Victory over enemies. Good health recovery. Service-oriented career may suit.",
        7: "Partnerships with powerful people. Spouse may be authoritative. Public life.",
        8: "Interest in occult and transformation. Challenges with authority. Hidden power.",
        9: "Fortunate father. Connection to dharma and higher learning. Government support.",
        10: "Excellent for career and public recognition. Leadership positions. Government roles.",
        11: "Large social circle. Gains through government or authority. Fulfilled desires.",
        12: "Spiritual inclinations. Living abroad possible. Father may be distant.",
    },
    "Moon": {
        1: "Emotional and caring personality. Popular and attractive. Changeable moods.",
        2: "Wealth fluctuations. Love for food and family. Persuasive speech.",
        3: "Mentally active and communicative. Imaginative. Emotional bond with siblings.",
        4: "Very strong position. Emotional comfort, good vehicles, property. Loving mother.",
        5: "Romantic and creative. Intelligent with artistic talents. Emotional about children.",
        6: "Emotional stress from enemies/debts. Healing through nurturing. Service to others.",
        7: "Emotional partnerships. Attractive and social spouse. Many public interactions.",
        8: "Emotional transformation. Interest in mysteries. Inheritance possible.",
        9: "Spiritual and philosophical mind. Travel over water. Fortunate mother.",
        10: "Public fame and popularity. Career may involve public dealing. Variable career path.",
        11: "Many friends and social connections. Gains through women. Fulfilled emotional desires.",
        12: "Spiritual and introspective. Sleep issues possible. Expenditure on comforts.",
    },
    "Mars": {
        1: "Energetic, athletic, and courageous. Aggressive drive. Scars or marks on body possible.",
        2: "Harsh speech but earning through effort. Family conflicts. Good for engineering/technical fields.",
        3: "Very strong placement. Brave, adventurous. Good with hands. Success in competition.",
        4: "Property through effort. Challenges with domestic peace. Strong vehicles/machinery.",
        5: "Sharp intelligence. Competitive in sports. Children may be strong-willed.",
        6: "Excellent position. Victory over enemies. Medical/military career. Good health.",
        7: "Passionate partnerships. Conflicts in marriage possible. Strong business drive.",
        8: "Transformative experiences. Interest in surgery/occult. Sudden events. Longevity issues to watch.",
        9: "Dharmic warrior. Father may be in military/police. Pilgrimage and righteous action.",
        10: "Excellent for career. Engineering, military, surgery, sports. Action-oriented leadership.",
        11: "Gains through courage and enterprise. Influential friends. Fulfilled ambitions.",
        12: "Foreign connections. Expenditure on property. Hidden anger. Hospital/institutional work.",
    },
}

# Simplified entries for remaining planets
for planet_name in ["Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
    if planet_name not in PLANET_IN_HOUSE:
        PLANET_IN_HOUSE[planet_name] = {}

PLANET_IN_HOUSE["Jupiter"].update({
    1: "Wise, optimistic, and naturally fortunate. Good health and longevity. Respected personality.",
    4: "Blessed with property, vehicles, and domestic happiness. Good education. Strong mother.",
    5: "Exceptional intelligence and creativity. Blessed with good children. Spiritual inclination.",
    7: "Excellent spouse. Happy marriage. Business partnerships thrive. Social respect.",
    9: "Most auspicious placement. Deeply spiritual and fortunate. Guru-blessed. Father is fortunate.",
    10: "High career success. Respected leader. Government favor. Ethical profession.",
})

PLANET_IN_HOUSE["Venus"].update({
    1: "Attractive, charming, and artistic. Love for luxury. Romantic personality.",
    2: "Wealth and family harmony. Sweet speech. Love for good food and luxury items.",
    4: "Beautiful home and vehicles. Domestic happiness. Love for comforts.",
    5: "Romantic and creative. Artistic talents. Love affairs. Blessed with daughters.",
    7: "Excellent for marriage. Beautiful and loving spouse. Happy partnerships.",
    12: "Luxurious lifestyle. Foreign pleasures. Spiritual love. High expenditure on comforts.",
})

PLANET_IN_HOUSE["Saturn"].update({
    1: "Disciplined and hardworking. Slow start but lasting results. Health needs attention.",
    3: "Courageous through persistence. Good for writing and communication. Steady siblings.",
    6: "Victory over enemies through patience. Good for service. Overcoming debts.",
    7: "Delayed marriage but lasting partnership. Older or mature spouse. Serious commitments.",
    10: "Career through hard work and discipline. Government/corporate success after struggles.",
    11: "Steady gains over time. Loyal friends. Fulfilled ambitions through persistence.",
})

PLANET_IN_HOUSE["Rahu"].update({
    1: "Unconventional personality. Foreign influences. Ambitious but restless.",
    3: "Excellent for media, communication, and technology. Bold ventures. Success through innovation.",
    6: "Victory over enemies through cunning. Good for competitive exams. Overcoming obstacles.",
    10: "Career in technology, foreign companies, or unconventional fields. Sudden rise possible.",
    11: "Large gains through unconventional means. Influential network. Foreign connections bring wealth.",
})

PLANET_IN_HOUSE["Ketu"].update({
    1: "Spiritual and detached personality. Interest in mysticism. Past-life karmic influences.",
    5: "Spiritual intelligence. Interest in past lives. Children may be spiritually inclined.",
    8: "Strong intuition and occult knowledge. Mystical experiences. Research ability.",
    9: "Deeply spiritual. Past-life dharmic connections. Pilgrimage. Detachment from religion.",
    12: "Excellent for moksha. Spiritual liberation. Interest in meditation and isolation.",
})

DIGNITY_READINGS = {
    "exalted": "is exalted — operating at peak strength. Its positive qualities shine brightly.",
    "debilitated": "is debilitated — facing challenges expressing its energy. Growth comes through overcoming these obstacles.",
    "own_sign": "is in its own sign — comfortable, confident, and functioning well in its natural domain.",
    "neutral": "is in a neutral position — performing adequately with moderate strength.",
}

RETROGRADE_READING = (
    "Being retrograde, {planet}'s energy is internalized and intensified. "
    "Past-life karmic themes related to {planet}'s significations are highlighted. "
    "Results may be delayed but ultimately deeper and more transformative."
)


def generate_basic_reading(
    planets: list,
    houses: list,
    ascendant: dict,
    yogas: list,
    doshas: list,
) -> dict:
    """Generate a comprehensive rule-based reading."""

    reading = {
        "ascendant": "",
        "personality": "",
        "planets": [],
        "key_strengths": [],
        "key_challenges": [],
        "career": "",
        "relationships": "",
        "summary": "",
    }

    # --- Ascendant Reading ---
    asc_sign = ascendant["sign"]
    reading["ascendant"] = ASC_READINGS.get(asc_sign, f"Ascendant in {asc_sign}.")
    reading["personality"] = (
        f"With {asc_sign} ({ascendant.get('sign_english', '')}) rising, "
        f"the Ascendant lord is {ascendant.get('lord', '')}. "
        f"{ASC_READINGS.get(asc_sign, '')}"
    )

    # --- Planet-by-planet readings ---
    strengths = []
    challenges = []

    for p in planets:
        pname = p["name"]
        house = p["house"]
        planet_reading = {
            "name": pname,
            "vedic_name": p.get("vedic_name", pname),
            "placement": f"{pname} in {p['sign']} ({p.get('sign_english', '')}) in House {house}",
            "reading": "",
        }

        # House placement reading
        house_text = PLANET_IN_HOUSE.get(pname, {}).get(house, "")
        if house_text:
            planet_reading["reading"] = house_text

        # Dignity reading
        dignity = p.get("dignity", "neutral")
        dignity_text = DIGNITY_READINGS.get(dignity, "")
        if dignity_text:
            planet_reading["reading"] += f" {pname} {dignity_text}"

        # Retrograde
        if p.get("retrograde") and pname not in ("Rahu", "Ketu"):
            planet_reading["reading"] += " " + RETROGRADE_READING.format(planet=pname)

        # Track strengths and challenges
        if dignity == "exalted":
            strengths.append(f"{pname} exalted in {p['sign']} (House {house})")
        elif dignity == "own_sign":
            strengths.append(f"{pname} strong in own sign {p['sign']}")
        elif dignity == "debilitated":
            challenges.append(f"{pname} debilitated in {p['sign']} — needs remedial attention")

        if house in [6, 8, 12] and pname not in ("Rahu", "Ketu"):
            challenges.append(f"{pname} in dusthana House {house}")

        reading["planets"].append(planet_reading)

    # Add yoga-based strengths
    for yoga in yogas:
        if yoga.get("category") == "benefic":
            strengths.append(f"{yoga['name']} — {yoga['description'][:80]}")

    # Add dosha-based challenges
    for dosha in doshas:
        if dosha.get("present") and dosha.get("severity") not in ("none", "cancelled"):
            challenges.append(f"{dosha['name']} ({dosha['severity']})")

    reading["key_strengths"] = strengths[:8]
    reading["key_challenges"] = challenges[:8]

    # --- Career indicators ---
    house_10_planets = [p for p in planets if p["house"] == 10]
    house_10_data = next((h for h in houses if h["house"] == 10), None)
    career_text = ""
    if house_10_planets:
        names = [p["name"] for p in house_10_planets]
        career_text = f"Career house (10th) has {', '.join(names)}, suggesting "
        if "Sun" in names:
            career_text += "government, leadership, or authority roles. "
        if "Mars" in names:
            career_text += "engineering, military, surgery, or sports. "
        if "Mercury" in names:
            career_text += "communication, IT, writing, or commerce. "
        if "Jupiter" in names:
            career_text += "teaching, law, finance, or advisory roles. "
        if "Venus" in names:
            career_text += "arts, entertainment, luxury goods, or hospitality. "
        if "Saturn" in names:
            career_text += "corporate, government service, manufacturing, or mining. "
        if "Rahu" in names:
            career_text += "technology, foreign companies, or unconventional fields. "
    elif house_10_data:
        career_text = (
            f"10th house lord is {house_10_data['lord']}. "
            f"Career direction influenced by {house_10_data['lord']}'s placement and dignity."
        )
    reading["career"] = career_text

    # --- Relationship indicators ---
    house_7_planets = [p for p in planets if p["house"] == 7]
    venus = next((p for p in planets if p["name"] == "Venus"), None)
    rel_text = ""
    if house_7_planets:
        names = [p["name"] for p in house_7_planets]
        rel_text = f"Partnership house (7th) has {', '.join(names)}. "
    if venus:
        rel_text += (
            f"Venus is in {venus['sign']} (House {venus['house']}). "
            f"{'Venus is strong — good for relationships and harmony.' if venus.get('dignity') in ('exalted', 'own_sign') else 'Relationships benefit from patience and understanding.'}"
        )
    reading["relationships"] = rel_text

    # --- Summary ---
    reading["summary"] = (
        f"This chart has {len(yogas)} yoga(s) and "
        f"{len([d for d in doshas if d.get('present')])} active dosha(s). "
        f"Overall, {'a well-supported chart with strong planetary placements' if len(strengths) > len(challenges) else 'a chart with growth opportunities through overcoming challenges'}."
    )

    return reading
