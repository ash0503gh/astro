"""
Astrological Q&A ("Ask Jyotishi") Engine powered by Google Gemini 2.5 Flash.
Provides direct, honest, and grounded astrological answers based on:
- Precise Natal Chart (Lagna, Houses, Planetary Placements, Dignities, Nakshatras)
- Vimshottari Dasha Timeline (Current & Upcoming Antardashas with exact dates)
- Real-Time Planetary Transits (Gochar of Saturn, Jupiter, Rahu, Ketu, etc.)
- Multi-turn conversation history (up to 6 recent messages)
"""

import os
import re
import httpx
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

try:
    import swisseph as swe
except ImportError:
    swe = None

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
DEFAULT_MODEL = os.getenv("GEMINI_QA_MODEL") or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
FALLBACK_MODELS = [DEFAULT_MODEL, "gemini-2.0-flash", "gemini-1.5-flash"]
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

SIGNS = [
    "Mesha", "Vrishabha", "Mithuna", "Karka",
    "Simha", "Kanya", "Tula", "Vrishchika",
    "Dhanu", "Makara", "Kumbha", "Meena"
]

SIGN_ENGLISH = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

SIGNS_HI_MAP = {
    "Mesha": "मेष", "Vrishabha": "वृषभ", "Mithuna": "मिथुन", "Karka": "कर्क",
    "Simha": "सिंह", "Kanya": "कन्या", "Tula": "तुला", "Vrishchika": "वृश्चिक",
    "Dhanu": "धनु", "Makara": "मकर", "Kumbha": "कुम्भ", "Meena": "मीन",
}

LORDS_HI_MAP = {
    "Mars": "मंगल", "Venus": "शुक्र", "Mercury": "बुध", "Moon": "चन्द्र",
    "Sun": "सूर्य", "Jupiter": "बृहस्पति (गुरु)", "Saturn": "शनि", "Rahu": "राहु", "Ketu": "केतु"
}


def compute_current_transits(natal_lagna_sign_num: int, natal_moon_sign_num: int) -> Dict[str, Any]:
    """Compute real-time planetary transits (Gochar) in sidereal Lahiri zodiac."""
    now = datetime.now(timezone.utc)
    transits = {
        "calculated_at": now.strftime("%Y-%m-%d %H:%M UTC"),
        "planets": [],
    }

    if swe is None:
        return transits

    jd_now = swe.julday(
        now.year, now.month, now.day,
        now.hour + now.minute / 60.0 + now.second / 3600.0
    )
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    planet_list = [
        (swe.SUN, "Sun", "Surya"),
        (swe.MOON, "Moon", "Chandra"),
        (swe.MARS, "Mars", "Mangal"),
        (swe.MERCURY, "Mercury", "Budha"),
        (swe.JUPITER, "Jupiter", "Guru"),
        (swe.VENUS, "Venus", "Shukra"),
        (swe.SATURN, "Saturn", "Shani"),
        (swe.MEAN_NODE, "Rahu", "Rahu"),
    ]

    for pid, pname, vedic_name in planet_list:
        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
        res = swe.calc_ut(jd_now, pid, flags)
        lon = res[0][0] % 360
        speed = res[0][3]
        sign_idx = int(lon / 30) % 12
        sign_num = sign_idx + 1
        deg_in_sign = round(lon % 30, 2)
        is_retro = speed < 0 and pname not in ("Rahu",)

        # House from Natal Lagna and Natal Moon
        house_from_lagna = ((sign_num - natal_lagna_sign_num) % 12) + 1
        house_from_moon = ((sign_num - natal_moon_sign_num) % 12) + 1

        transits["planets"].append({
            "name": pname,
            "vedic_name": vedic_name,
            "sign": SIGNS[sign_idx],
            "sign_english": SIGN_ENGLISH[sign_idx],
            "sign_num": sign_num,
            "degree": deg_in_sign,
            "retrograde": is_retro,
            "house_from_lagna": house_from_lagna,
            "house_from_moon": house_from_moon,
        })

    # Ketu is opposite Rahu
    rahu_data = next((p for p in transits["planets"] if p["name"] == "Rahu"), None)
    if rahu_data:
        ketu_sign_num = ((rahu_data["sign_num"] + 5) % 12) + 1
        ketu_sign_idx = ketu_sign_num - 1
        ketu_house_lagna = ((ketu_sign_num - natal_lagna_sign_num) % 12) + 1
        ketu_house_moon = ((ketu_sign_num - natal_moon_sign_num) % 12) + 1
        transits["planets"].append({
            "name": "Ketu",
            "vedic_name": "Ketu",
            "sign": SIGNS[ketu_sign_idx],
            "sign_english": SIGN_ENGLISH[ketu_sign_idx],
            "sign_num": ketu_sign_num,
            "degree": rahu_data["degree"],
            "retrograde": True,
            "house_from_lagna": ketu_house_lagna,
            "house_from_moon": ketu_house_moon,
        })

    return transits


def _format_context_for_jyotishi(
    name: str,
    chart: dict,
    dashas: list,
    yogas: list,
    doshas: list,
    transits: dict,
    language: str = "en",
) -> str:
    """Format full natal, dasha, and real-time transit context for Gemini."""

    planets_text = "\n".join(
        f"  - {p['name']} ({p.get('vedic_name', '')}): {p['sign']} ({p.get('sign_english', '')}) "
        f"House {p['house']}, {p.get('degree_in_sign', '')}°, "
        f"Nakshatra: {p.get('nakshatra', {}).get('name', '')} Pada {p.get('nakshatra', {}).get('pada', '')}, "
        f"Dignity: {p.get('dignity', 'neutral')}"
        f"{' [R]' if p.get('retrograde') and p['name'] not in ('Rahu', 'Ketu') else ''}"
        for p in chart.get("planets", [])
    )

    houses_text = "\n".join(
        f"  - House {h['house']}: {h['sign']} ({h.get('sign_english', '')}), "
        f"Lord: {h['lord']}, Occupants: {', '.join(h['planets']) if h.get('planets') else 'None'}"
        for h in chart.get("houses", [])
    )

    # Active & Upcoming Dashas
    from dasha import get_current_dasha
    curr_dasha = get_current_dasha(dashas)
    dasha_summary = (
        f"Current Mahadasha: {curr_dasha.get('mahadasha', 'N/A')} "
        f"({curr_dasha.get('mahadasha_start', '')} to {curr_dasha.get('mahadasha_end', '')})\n"
        f"Current Antardasha: {curr_dasha.get('antardasha', 'N/A')} "
        f"({curr_dasha.get('antardasha_start', '')} to {curr_dasha.get('antardasha_end', '')})"
    )

    # Find upcoming Antardashas
    upcoming_antardashas = []
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for md in dashas:
        for ad in md.get("antardashas", []):
            if ad.get("end", "") > now_str:
                upcoming_antardashas.append(
                    f"{md.get('lord', '')}-{ad.get('lord', '')} Antardasha: "
                    f"from {ad.get('start', '')} to {ad.get('end', '')}"
                )
            if len(upcoming_antardashas) >= 4:
                break
        if len(upcoming_antardashas) >= 4:
            break

    upcoming_dasha_text = "\n  - ".join(upcoming_antardashas) if upcoming_antardashas else "Not available"

    # Transits text
    transits_text = ""
    if transits.get("planets"):
        saturn_t = next((p for p in transits["planets"] if p["name"] == "Saturn"), None)
        jupiter_t = next((p for p in transits["planets"] if p["name"] == "Jupiter"), None)
        rahu_t = next((p for p in transits["planets"] if p["name"] == "Rahu"), None)
        ketu_t = next((p for p in transits["planets"] if p["name"] == "Ketu"), None)

        t_lines = []
        for p in transits["planets"]:
            retro_mark = " [R]" if p.get("retrograde") else ""
            t_lines.append(
                f"  - Transit {p['name']} in {p['sign']} ({p['sign_english']}) {p['degree']}°{retro_mark} "
                f"-> House {p['house_from_lagna']} from Natal Lagna, House {p['house_from_moon']} from Natal Moon"
            )
        transits_text = "\n".join(t_lines)

    asc = chart.get("ascendant", {})
    moon = next((p for p in chart.get("planets", []) if p["name"] == "Moon"), None)

    yogas_text = ", ".join(y.get("name", "") for y in yogas) if yogas else "None"
    doshas_text = ", ".join(d.get("name", "") for d in doshas if d.get("present")) if doshas else "None"

    return f"""ASTROLOGICAL DOSSIER FOR {name}:

NATAL LAGNA (Ascendant):
  Sign: {asc.get('sign', '')} ({asc.get('sign_english', '')}) at {asc.get('degree_in_sign', '')}°
  Lagna Lord: {asc.get('lord', '')}
  Nakshatra: {asc.get('nakshatra', {}).get('name', '')} Pada {asc.get('nakshatra', {}).get('pada', '')}

NATAL MOON:
  Sign: {moon.get('sign', '') if moon else 'N/A'} ({moon.get('sign_english', '') if moon else ''})
  House: {moon.get('house', '') if moon else ''}
  Nakshatra: {moon.get('nakshatra', {}).get('name', '') if moon else ''}

PLANETARY POSITIONS (Sidereal / Lahiri):
{planets_text}

HOUSES AND LORDS:
{houses_text}

YOGAS: {yogas_text}
DOSHAS: {doshas_text}

VIMSHOTTARI DASHA TIMELINE:
  {dasha_summary}
  Upcoming Periods:
  - {upcoming_dasha_text}

REAL-TIME PLANETARY TRANSITS (GOCHAR as of {transits.get('calculated_at', 'Today')}):
{transits_text}
"""


async def ask_jyotishi(
    name: str,
    chart: dict,
    dashas: list,
    yogas: list,
    doshas: list,
    question: str,
    history: Optional[List[Dict[str, str]]] = None,
    language: str = "en",
) -> Dict[str, Any]:
    """Answer an astrological question using Gemini 2.5 Flash with chart context & transits."""

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        return {
            "answer": "Astrological Q&A unavailable — GEMINI_API_KEY is not configured on the backend.",
            "error": "Missing GEMINI_API_KEY",
        }

    # Extract natal lagna and moon sign numbers for transit calculations
    asc_sign = chart.get("ascendant", {}).get("sign", "Mesha")
    lagna_sign_num = SIGNS.index(asc_sign) + 1 if asc_sign in SIGNS else 1

    moon = next((p for p in chart.get("planets", []) if p["name"] == "Moon"), None)
    moon_sign = moon.get("sign", "Mesha") if moon else "Mesha"
    moon_sign_num = SIGNS.index(moon_sign) + 1 if moon_sign in SIGNS else 1

    # Real-time planetary transits
    transits = compute_current_transits(lagna_sign_num, moon_sign_num)
    context_text = _format_context_for_jyotishi(name, chart, dashas, yogas, doshas, transits, language=language)

    if language == "hi":
        system_prompt = f"""आप एक परम विद्वान, स्पष्टवादी और प्रामाणिक वैदिक ज्योतिषी (दैवज्ञ) हैं।
जातक ({name}) आपसे अपने जीवन, करियर, धन, संबंध, स्वास्थ्य अथवा समय के संबंध में विशिष्ट प्रश्न पूछ रहे हैं।

जातक का जन्म कुण्डली विवरण, वर्तमान एवं आगामी विंशोत्तरी महादशा-अंतर्दशा और आज के वास्तविक ग्रह गोचर (Transits) नीचे दिए गए हैं।

जातक के प्रश्न का उत्तर इन अनिवार्य नियमों के अनुसार दें:
1. संक्षिप्त, सटीक, ईमानदार और सीधा उत्तर दें (Concise, punchy, direct and honest)। किसी भी बात को अनावश्‍यक घुमा-फिराकर या मीठा बनाकर न कहें। यदि कोई समय कठिन है अथवा कार्य में बाधा के योग हैं, तो स्पष्ट शब्दों में बताएं और उसका ज्योतिषीय कारण स्पष्ट करें।
2. उत्तर को 2 से 3 सारगर्भित, केंद्रित परिच्छेदों में प्रस्तुत करें।
3. अपने उत्तर में ज्योतिषीय आधार (सटीक भाव, भावेश, चल रही महादशा/अंतर्दशा की तिथियां और वर्तमान गोचर जैसे शनि/गुरु का प्रभाव) का स्पष्ट उल्लेख करें।
4. आगामी 6 से 12 महीनों के संबंध में समय-सीमा (Timeframe / Dates) स्पष्ट करें (जैसे अमुक माह से अमुक माह तक)।
5. यदि आवश्यक हो, तो 1-2 व्यावहारिक और सटीक वैदिक उपाय (मंत्र, दान, व्रत) सुझाएं।
6. शुद्ध, गरिमामयी देवनागरी हिन्दी भाषा का प्रयोग करें। किसी भी शब्द के लिए कच्चे मार्कडाउन तारों (raw asterisks) का अनुचित प्रयोग न करें।
7. अनिवार्य पूर्णता नियम: अपने उत्तर और प्रत्येक वाक्य को सदैव पूर्ण, सुस्पष्ट और व्याकरण सम्मत विराम दें। कभी भी वाक्य अथवा समय-सीमा को अधूरा न छोड़ें। सभी तिथियों (जैसे जुलाई 2026 – मई 2027) एवं कोष्ठकों () को सही ढंग से बंद करें।

{context_text}"""
    else:
        system_prompt = f"""You are an expert, highly perceptive, and candid Vedic Astrologer (Jyotishi).
The native ({name}) is consulting you with specific personal questions regarding their career, finances, relationships, health, or life timings.

The native's complete birth chart, active and upcoming Vimshottari Mahadasha/Antardasha dates, and real-time planetary transits (Gochar) are provided below.

Respond according to these strict principles:
1. Give a concise, punchy, direct, and completely honest answer. Do not sugarcoat difficult placements or over-promise. If a period poses setbacks or is unfavorable for a transition, state so plainly and explain the astrological reasons.
2. Structure your answer in 2 to 3 crisp, substantive paragraphs.
3. Ground every conclusion in exact astrological evidence: cite the involved house numbers (e.g. 10th lord in 11th), current and upcoming Dasha dates (e.g. Jupiter-Mercury period starting in Nov 2026), and active transits (e.g. Saturn in 8th from Moon or Jupiter aspecting 10th house).
4. Provide specific time windows or months where relevant (e.g. "Favorable window: October to December 2026").
5. Include 1–2 practical, traditional Vedic remedies (mantra, charity, or lifestyle adjustments) if challenges exist.
6. Avoid generic horoscopes. Keep your tone respectful, authoritative, and insightful. Never output messy raw asterisks or unformatted text.
7. CRITICAL COMPLETION RULE: Always bring your thoughts and sentences to a complete, grammatically finalized conclusion. Never stop mid-sentence or cut off dates or words. Keep all date ranges (e.g. July 2026 – May 2027) and parentheses properly closed.

{context_text}"""

    # Format multi-turn conversation contents (up to 6 recent messages)
    contents = []
    recent_history = (history or [])[-6:]
    for msg in recent_history:
        role = "user" if msg.get("role") == "user" else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg.get("content", "")}]
        })

    # Append current question
    contents.append({
        "role": "user",
        "parts": [{"text": question}]
    })

    payload = {
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.5,
            "maxOutputTokens": 4096,
        }
    }

    models_to_try = []
    for m in FALLBACK_MODELS:
        if m and m not in models_to_try:
            models_to_try.append(m)

    last_error = ""
    async with httpx.AsyncClient(timeout=60.0) as client:
        for model in models_to_try:
            url = f"{GEMINI_BASE_URL}/{model}:generateContent?key={api_key}"
            try:
                response = await client.post(
                    url,
                    headers={
                        "Content-Type": "application/json",
                        "x-goog-api-key": api_key,
                    },
                    json=payload,
                )

                if response.status_code == 404:
                    last_error = f"Model {model} not found (404)."
                    continue

                if response.status_code != 200:
                    err_msg = response.text
                    try:
                        err_msg = response.json().get("error", {}).get("message", err_msg)
                    except Exception:
                        pass
                    return {
                        "error": f"Gemini API error ({response.status_code}): {err_msg}",
                        "answer": "Unable to generate answer at this time.",
                    }

                data = response.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    return {
                        "error": "Gemini returned an empty response.",
                        "answer": "The Jyotishi was unable to interpret this configuration right now. Please try again.",
                    }

                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                raw_text = "".join(
                    part.get("text", "") for part in parts
                    if isinstance(part, dict) and "text" in part
                )
                
                # Clean up any stray markdown formatting artifacts
                cleaned_text = raw_text.strip()
                return {
                    "answer": cleaned_text,
                    "model": model,
                    "transits_used": bool(transits.get("planets")),
                }

            except Exception as e:
                last_error = str(e)
                continue

    return {
        "error": f"Failed across all models. Last error: {last_error}",
        "answer": "Connection error while reaching Gemini. Please try again in a moment.",
    }
