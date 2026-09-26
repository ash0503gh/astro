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
from datetime import date, datetime, timezone
from typing import Optional, List, Dict, Any

from ai_reader import without_thinking

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


def _from_today(date_str: str, today: date) -> str:
    """Describe a YYYY-MM-DD date relative to today: "10 months ago", "in 6 months".

    Spelled out because the model (thinking off) can't compare dates: knowing today
    is Sep 2026, it still called a period that began in Nov 2025 "upcoming".
    """
    try:
        days = (date.fromisoformat(date_str) - today).days
    except (TypeError, ValueError):
        return "unknown"
    months = round(abs(days) / 30.44)
    if months == 0:
        span = "under a month"
    elif months < 24:
        span = f"{months} month{'s' if months > 1 else ''}"
    else:
        span = f"{round(months / 12)} years"
    return f"in {span}" if days > 0 else f"{span} ago"


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
    today = datetime.now(timezone.utc).date()
    now_str = today.isoformat()

    def period(start, end):
        return (f"({start} to {end}; started {_from_today(start, today)}, "
                f"ends {_from_today(end, today)})")

    dasha_summary = (
        f"Current Mahadasha: {curr_dasha.get('mahadasha', 'N/A')} "
        f"{period(curr_dasha.get('mahadasha_start'), curr_dasha.get('mahadasha_end'))}\n"
        f"Current Antardasha: {curr_dasha.get('antardasha', 'N/A')} "
        f"{period(curr_dasha.get('antardasha_start'), curr_dasha.get('antardasha_end'))}"
    )

    # Find upcoming Antardashas (not yet started; the current one is listed above)
    upcoming_antardashas = []
    for md in dashas:
        for ad in md.get("antardashas", []):
            if ad.get("start", "") > now_str:
                upcoming_antardashas.append(
                    f"{md.get('lord', '')}-{ad.get('lord', '')} Antardasha: "
                    f"from {ad.get('start', '')} to {ad.get('end', '')} "
                    f"(starts {_from_today(ad.get('start', ''), today)})"
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

    return f"""ASTROLOGICAL DOSSIER FOR {name} (today is {now_str}):

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
        system_prompt = f"""आप एक अनुभवी एवं स्पष्टवादी वैदिक ज्योतिषी (दैवज्ञ) हैं।
जातक आपसे अपने जीवन के संबंध में एक विशिष्ट प्रश्न पूछ रहे हैं।
जातक की कुण्डली, सक्रिय विंशोत्तरी दशा तिथियां एवं आज के तात्कालिक गोचर नीचे दिए गए हैं।

उत्तर देने के अनिवार्य नियम:
1. नाम से सम्बोधन वर्जित: उत्तर की शुरुआत में जातक का नाम या कोई अभिवादन कभी न लिखें (जैसे "{name},", "प्रिय {name},", "नमस्ते" आदि कदापि न लिखें)। प्रथम शब्द से ही सीधे मुख्य उत्तर प्रारम्भ करें।
2. संक्षिप्त एवं बिंदुवार (अधिकतम 80–120 शब्द): उत्तर अत्यंत संक्षिप्त, स्पष्ट एवं प्रभावी रखें। सामान्य जातक के समझने योग्य सरल भाषा का प्रयोग करें। अनावश्यक विस्तार या भारी-भरकम व्याख्या न करें।
3. सीधा निष्कर्ष पहले: पहली ही पंक्ति में स्पष्ट निर्णय दें (जैसे: "अभी नया मकान या फ्लैट खरीदने से बचें।", "अक्टूबर से दिसंबर 2026 के मध्य नौकरी परिवर्तन के प्रबल योग हैं।")।
4. सरल एवं जनसामान्य की भाषा: ज्योतिषीय कारणों को आम बोलचाल की सरल, गरिमामयी हिन्दी में समझाएं ताकि साधारण व्यक्ति भी आसानी से समझ सके।
5. अनुकूल समय एवं सरल उपाय: सर्वोत्तम समय-सीमा (महीना/वर्ष) एक पंक्ति में बताएं और साथ में 1 सरल, व्यावहारिक उपाय सुझाएं।
6. पूर्णता: प्रत्येक वाक्य को पूर्ण एवं व्याकरण सम्मत विराम दें और सभी कोष्ठकों () को बंद रखें।

{context_text}"""
    else:
        system_prompt = f"""You are an expert Vedic Astrologer (Jyotishi) giving direct, personal advice.
The native is consulting you with a specific question.
Their chart, active Dasha dates, and current Gochar transits are provided below.

Respond following these strict guidelines:
1. NO GREETINGS OR NAMES: NEVER start your answer with the user's name or any greeting (do NOT write "{name},", "Hello", "Dear {name}", etc.). Jump directly into the answer on the very first word.
2. SHORT & ON-POINT (80–120 words max): Be punchy, clear, and direct. Busy users want quick clarity, not long essays.
3. CLEAR VERDICT FIRST: State the bottom line in the very first sentence (e.g. "Hold off on buying a home right now.", "A strong career change window opens between October and December 2026.").
4. SIMPLE, EVERYDAY EXPLANATION: Translate astrological factors into plain, practical terms that a normal person can easily understand. Mention the key planetary influence (e.g. active dasha or Saturn's transit) simply, without overwhelming them with dense technical jargon.
5. BEST WINDOW & REMEDY: Provide the best timing window in one sentence, followed by 1 simple practical remedy (e.g. mantra or lifestyle advice).
6. COMPLETION: Always complete every sentence cleanly with proper punctuation and closed parentheses.

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
            "temperature": 0.4,
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
                    json=without_thinking(payload, model),
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

                # Post-process: Guarantee removal of any leading greetings or user names
                if name:
                    name_clean = name.strip()
                    name_parts = [re.escape(p) for p in name_clean.split() if len(p) > 1]
                    names_to_match = "|".join([re.escape(name_clean)] + name_parts)
                    prefix_pattern = (
                        rf"^(?:\*{1,2}|_{1,2})?"
                        rf"(?:(?:dear|hello|hi|hey|namaste|greetings|प्रिय|श्रीमान|नमस्ते)\s+)?"
                        rf"(?:{names_to_match})"
                        rf"(?:\*{1,2}|_{1,2})?"
                        rf"[,:\s—\-]+"
                    )
                    cleaned_text = re.sub(prefix_pattern, "", cleaned_text, flags=re.IGNORECASE).strip()

                # Also strip standalone leading greetings if present
                cleaned_text = re.sub(
                    r"^(?:\*{1,2}|_{1,2})?(?:dear|hello|hi|hey|namaste|greetings|नमस्ते)(?:\*{1,2}|_{1,2})?[,:\s—\-]+",
                    "",
                    cleaned_text,
                    flags=re.IGNORECASE
                ).strip()

                if cleaned_text and cleaned_text[0].islower():
                    cleaned_text = cleaned_text[0].upper() + cleaned_text[1:]

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
