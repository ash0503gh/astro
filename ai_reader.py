"""
AI-Powered Deep Chart Reading using Google Gemini API.
Generates personalized, insightful interpretations of the birth chart.
"""

import json
import os
import re
import httpx
from typing import AsyncIterator, Optional

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
FALLBACK_MODELS = [DEFAULT_MODEL, "gemini-2.0-flash", "gemini-1.5-flash"]
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"


def without_thinking(payload: dict, model: str) -> dict:
    """Turn off Gemini 2.5 Flash "thinking" (billed at the output-token rate).

    Only 2.5 Flash models accept a zero thinking budget; older models don't think.
    """
    if not model.startswith("gemini-2.5-flash"):
        return payload
    config = {**payload["generationConfig"], "thinkingConfig": {"thinkingBudget": 0}}
    return {**payload, "generationConfig": config}


def _format_chart_for_prompt(
    name: str,
    chart: dict,
    dashas: list,
    yogas: list,
    doshas: list,
) -> str:
    """Format chart data into a structured prompt for Claude."""

    planets_text = "\n".join(
        f"  - {p['name']} ({p['vedic_name']}): {p['sign']} ({p['sign_english']}) "
        f"House {p['house']}, {p['degree_in_sign']}°, "
        f"Nakshatra: {p['nakshatra']['name']} Pada {p['nakshatra']['pada']}, "
        f"Dignity: {p['dignity']}"
        f"{' [R]' if p.get('retrograde') and p['name'] not in ('Rahu', 'Ketu') else ''}"
        for p in chart["planets"]
    )

    houses_text = "\n".join(
        f"  - House {h['house']}: {h['sign']} ({h['sign_english']}), "
        f"Lord: {h['lord']}, Planets: {', '.join(h['planets']) if h['planets'] else 'Empty'}"
        for h in chart["houses"]
    )

    yogas_text = "\n".join(
        f"  - {y['name']}: {y['description']}"
        for y in yogas
    ) if yogas else "  No major yogas detected."

    doshas_text = "\n".join(
        f"  - {d['name']}: {'Present' if d.get('present') else 'Absent'}"
        f"{' — ' + d.get('description', '') if d.get('present') else ''}"
        for d in doshas
    )

    # Current and next Mahadasha
    from dasha import get_current_dasha
    current_dasha = get_current_dasha(dashas)

    dasha_text = (
        f"  Current Mahadasha: {current_dasha.get('mahadasha', 'N/A')} "
        f"({current_dasha.get('mahadasha_start', '')} to {current_dasha.get('mahadasha_end', '')})\n"
        f"  Current Antardasha: {current_dasha.get('antardasha', 'N/A')} "
        f"({current_dasha.get('antardasha_start', '')} to {current_dasha.get('antardasha_end', '')})"
    )

    asc = chart["ascendant"]
    navamsa_text = "\n".join(
        f"  - {n['name']}: {n['navamsa_sign']}"
        for n in chart["navamsa"]
    )

    return f"""VEDIC BIRTH CHART ANALYSIS for {name}

ASCENDANT (Lagna):
  {asc['sign']} ({asc.get('sign_english', '')}) at {asc.get('degree_in_sign', '')}°
  Nakshatra: {asc['nakshatra']['name']} Pada {asc['nakshatra']['pada']}
  Lagna Lord: {asc['lord']}

PLANETARY POSITIONS (Sidereal / Lahiri Ayanamsa):
{planets_text}

HOUSE CHART:
{houses_text}

NAVAMSA (D9) POSITIONS:
{navamsa_text}

YOGAS DETECTED:
{yogas_text}

DOSHAS DETECTED:
{doshas_text}

VIMSHOTTARI DASHA:
{dasha_text}
"""


async def stream_ai_reading(
    name: str,
    chart: dict,
    dashas: list,
    yogas: list,
    doshas: list,
    language: str = "en",
) -> AsyncIterator[dict]:
    """Stream a deep AI reading of the birth chart from Google Gemini.

    Yields {"section": key} when a section header arrives, {"text": str} as content
    is written, and finally {"done": reading}: the parsed reading
    ({"full_text", "sections", "model_used"}) or {"error", "sections"}.
    """

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        yield {"done": {
            "error": "AI reading unavailable — GEMINI_API_KEY not configured on backend.",
            "sections": {},
        }}
        return

    chart_text = _format_chart_for_prompt(name, chart, dashas, yogas, doshas)

    if language == "hi":
        system_prompt = """आप एक प्रकांड वैदिक ज्योतिषी (दैवज्ञ) हैं, जिन्हें प्राचीन शास्त्रीय ग्रंथों (बृहत्पाराशर होराशास्त्र, फलदीपिका, जातक पारिजात, मानसागरी) का गूढ़ ज्ञान है।

प्रदान की गई जन्म कुण्डली का गहन, प्रामाणिक और विस्तृत विश्लेषण शुद्ध, सुरुचिपूर्ण एवं गरिमामयी हिन्दी भाषा (देवनागरी लिपि) में प्रस्तुत करें। आपका फलादेश जातक और उनके परिवार के लिए अत्यंत अंतर्दृष्टिपूर्ण, सटीक, संतुलित और व्यावहारिक होना चाहिए।

अपने विश्लेषण को अनिवार्य रूप से ठीक इन्हीं शीर्षकों (Exact Markdown Headers) के अंतर्गत प्रस्तुत करें:

## Personality & Core Nature
लग्न, लग्नेश, और चन्द्र राशि का शास्त्रीय विश्लेषण करते हुए जातक के व्यक्तित्व, स्वभाव, गुण-दोष और मूल प्रकृति का विस्तृत वर्णन करें।

## Mind & Emotions
चन्द्रमा की भाव स्थिति, नक्षत्र, और उस पर पड़ने वाले शुभ-अशुभ ग्रहों के दृष्टि प्रभाव के आधार पर जातक की मानसिक स्थिति, संवेदनशीलता और आंतरिक सोच का विश्लेषण करें।

## Career & Profession
दशम भाव (कर्म भाव), दशमेश, दशम भावस्थ ग्रहों तथा आजीविका से संबंधित योगों का विश्लेषण कर उपयुक्त कार्यक्षेत्र एवं करियर मार्गदर्शन प्रदान करें।

## Wealth & Finances
द्वितीय भाव (धन भाव), एकादश भाव (लाभ भाव), धन योगों तथा देवगुरु बृहस्पति की स्थिति के आधार पर धन संचय, पैतृक संपत्ति और आर्थिक संभावनाओं का विश्लेषण करें।

## Relationships & Marriage
सप्तम भाव (विवाह व साझेदारी भाव), सप्तमेश, शुक्र (एवं स्त्रियों की कुण्डली में गुरु) के आधार पर वैवाहिक जीवन, जीवनसाथी के स्वभाव और संबंधों का विश्लेषण करें।

## Health & Vitality
लग्न भाव, षष्ठ भाव (रोग भाव), लग्नेश और पीड़ित ग्रहों के आधार पर स्वास्थ्य, जीवन ऊर्जा और आवश्यक स्वास्थ्य सावधानियों का विश्लेषण करें।

## Spiritual Path
नवम भाव (भाग्य व धर्म भाव), द्वादश भाव (मोक्ष भाव), केतु की स्थिति और आध्यात्मिक योगों के आधार पर जातक की आध्यात्मिक यात्रा और ईश्वर भक्ति का विश्लेषण करें।

## Current Period Analysis
वर्तमान में चल रही विंशोत्तरी महादशा एवं अंतर्दशा का प्रभाव और आगामी समय के लिए स्पष्ट फलकथन करें।

## Key Recommendations
कुण्डली के दोषों के निवारण तथा शुभ ग्रहों के बल संवर्धन हेतु स्पष्ट और व्यावहारिक वैदिक उपाय प्रस्तुत करें।
उपायों को स्पष्ट रूप से संरचित करें: प्रत्येक मुख्य विषय के लिए संख्याबद्ध क्रम (जैसे 1. विष योग के निवारण हेतु उपाय) का प्रयोग करें, और प्रत्येक विशिष्ट उपाय को अलग पंक्ति में बुलेट बिंदु (*) से शुरू करें। कभी भी एक ही पंक्ति पर कई बुलेट बिंदु न जोड़ें।

प्रामाणिक वैदिक ज्योतिषीय शब्दावली (जैसे लग्न, राशि, नक्षत्र, महादशा, गोचर, उपाय, मंत्र, दान) का प्रयोग करें। प्रत्येक अनुभाग के लिए 1–2 सटीक, सारगर्भित और केंद्रित परिच्छेद लिखें ताकि सभी 9 शीर्षकों का विश्लेषण अनिवार्य रूप से पूर्ण हो सके। सामान्य या अस्पष्ट बातों से बचें — प्रत्येक अंतर्दृष्टि कुण्डली के किसी विशिष्ट ग्रह योग पर आधारित होनी चाहिए।"""
    else:
        system_prompt = """You are an expert Vedic astrologer (Jyotishi) with deep knowledge of
classical texts (Brihat Parashara Hora Shastra, Phaladeepika, Jataka Parijata).

Analyze the birth chart provided and give a comprehensive reading. Be insightful,
specific to the chart combinations, and balanced — highlight both strengths and
areas requiring attention.

Structure your response with these exact markdown headers:

## Personality & Core Nature
Analyze the Ascendant, its lord, and the Moon sign to describe the native's personality.

## Mind & Emotions
Focus on the Moon's placement, nakshatra, and aspects to describe the mental/emotional landscape.

## Career & Profession
Analyze the 10th house, its lord, planets influencing career, and relevant yogas.

## Wealth & Finances
Look at the 2nd and 11th houses, Dhana yogas, and Jupiter's placement.

## Relationships & Marriage
Analyze the 7th house, Venus, and Jupiter (for females) / Venus (for males).

## Health & Vitality
Check the Ascendant, 6th house, and afflicted planets for health indicators.

## Spiritual Path
Analyze the 9th and 12th houses, Ketu's placement, and spiritual yogas.

## Current Period Analysis
Interpret the current Mahadasha-Antardasha and what to expect.

## Key Recommendations
Provide specific, actionable remedies and suggestions.
Format recommendations clearly: use numbered items for each main area (e.g. 1. Remedies for Vish Yoga), and put each individual remedy on its own separate line starting with a bullet point (*). Never combine multiple bullet points onto the same line.

Use both Sanskrit terms and English explanations. Provide 1–2 focused, substantive paragraphs per section so all 9 sections are thoroughly completed. Avoid generic statements — every insight should be traceable
to a specific chart combination."""

    payload = {
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": chart_text}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 8192
        }
    }

    # Try configured model with fallback support
    models_to_try = []
    for m in FALLBACK_MODELS:
        if m and m not in models_to_try:
            models_to_try.append(m)

    last_error = ""

    async with httpx.AsyncClient(timeout=90.0) as client:
        for model in models_to_try:
            url = f"{GEMINI_BASE_URL}/{model}:streamGenerateContent?alt=sse"
            chunks = []
            block_reason = None
            try:
                async with client.stream(
                    "POST",
                    url,
                    headers={
                        "Content-Type": "application/json",
                        "x-goog-api-key": api_key,
                    },
                    json=without_thinking(payload, model),
                ) as response:
                    if response.status_code == 404:
                        # Model not available in this tier/region, try next fallback
                        last_error = f"Model '{model}' not found (404)."
                        continue

                    if response.status_code != 200:
                        err_body = (await response.aread()).decode("utf-8", "replace")
                        try:
                            err_body = json.loads(err_body).get("error", {}).get("message", err_body)
                        except Exception:
                            pass
                        yield {"done": {
                            "error": f"Gemini API error ({response.status_code}): {err_body}",
                            "sections": {},
                        }}
                        return

                    splitter = _SectionSplitter()
                    async for line in response.aiter_lines():
                        if not line.startswith("data:"):
                            continue
                        data = json.loads(line[5:])
                        block_reason = block_reason or data.get("promptFeedback", {}).get("blockReason")
                        for candidate in data.get("candidates", [])[:1]:
                            for part in candidate.get("content", {}).get("parts", []):
                                if part.get("text"):
                                    chunks.append(part["text"])
                                    for event in splitter.feed(part["text"]):
                                        yield event
                    for event in splitter.flush():
                        yield event

            except httpx.TimeoutException:
                yield {"done": {
                    "error": "Gemini API request timed out (60s). Please try again.",
                    "sections": {},
                }}
                return
            except Exception as e:
                if chunks:  # text already reached the user; don't restart on another model
                    yield {"done": {"error": f"AI reading was interrupted: {e}", "sections": {}}}
                    return
                last_error = str(e)
                continue

            text = "".join(chunks)
            if not text.strip():
                error = (f"AI generation blocked by safety filters: {block_reason}"
                         if block_reason else "Gemini generated no text content.")
                yield {"done": {"error": error, "sections": {}}}
                return

            yield {"done": {
                "full_text": text,
                "sections": _parse_sections(text),
                "model_used": model,
            }}
            return

    yield {"done": {
        "error": f"AI reading failed: {last_error or 'Unable to contact Gemini API'}",
        "sections": {},
    }}


# Multilingual mapping of header keywords to canonical keys
HEADER_KEY_MAP = [
    (("personality", "core nature", "व्यक्तित्व", "स्वभाव"), "personality_and_core_nature"),
    (("mind", "emotion", "मन", "भावना"), "mind_and_emotions"),
    (("career", "profession", "कर्म", "आजीविका", "करियर", "व्यवसाय"), "career_and_profession"),
    (("wealth", "finance", "धन", "वित्त", "आर्थिक"), "wealth_and_finances"),
    (("relationship", "marriage", "संबंध", "विवाह", "वैवाहिक", "दांपत्य"), "relationships_and_marriage"),
    (("health", "vitality", "स्वास्थ्य", "रोग", "आयु"), "health_and_vitality"),
    (("spiritual", "path", "आध्यात्म", "धर्म", "मोक्ष"), "spiritual_path"),
    (("current period", "dasha", "दशा", "महादशा", "वर्तमान"), "current_period_analysis"),
    (("recommendation", "remed", "उपाय", "सुझाव", "समाधान"), "key_recommendations"),
]


def _section_key(line: str) -> Optional[str]:
    """Canonical section key if `line` is a markdown section header, else None."""
    match = re.match(r"^#{1,3}\s+(?:[0-9]+[\.\)]\s*)?(.+)", line)
    if not match:
        return None
    header_raw = match.group(1).strip(" :*#")
    if len(header_raw) <= 2:
        return None

    # Match against canonical mapping
    hl = header_raw.lower()
    for keywords, canonical in HEADER_KEY_MAP:
        if any(kw in hl for kw in keywords):
            return canonical

    normalized_key = (
        header_raw.lower()
        .replace("&", "and")
        .replace("/", "_")
        .replace("-", "_")
    )
    normalized_key = re.sub(r"[^\w\s]", "", normalized_key)
    return re.sub(r"\s+", "_", normalized_key).strip("_")


class _SectionSplitter:
    """Turn streamed markdown into {"section": key} / {"text": str} events.

    Text passes through as soon as it arrives; only a line starting with "#" is
    held back until complete, to tell whether it is a section header.
    """

    def __init__(self):
        self.buf = ""     # received but not yet emitted
        self.mode = None  # None at a line start, then "header" or "text"

    def feed(self, delta: str) -> list:
        self.buf += delta
        events = []
        while self.buf:
            if self.mode is None:
                head = self.buf.lstrip(" ")
                if not head:
                    break
                self.mode = "header" if head.startswith("#") else "text"
            newline = self.buf.find("\n")
            if newline < 0:
                if self.mode == "text":
                    events.append({"text": self.buf})
                    self.buf = ""
                break
            line, self.buf = self.buf[:newline], self.buf[newline + 1:]
            events.append(self._line_event(line, "\n"))
            self.mode = None
        return events

    def flush(self) -> list:
        events = [self._line_event(self.buf, "")] if self.buf else []
        self.buf, self.mode = "", None
        return events

    def _line_event(self, line: str, ending: str) -> dict:
        key = _section_key(line) if self.mode == "header" else None
        return {"section": key} if key is not None else {"text": line + ending}


def _parse_sections(text: str) -> dict:
    """Parse the AI response into sections based on markdown headers."""
    sections = {}
    current_section = "introduction"
    current_content = []

    for line in text.split("\n"):
        key = _section_key(line)
        if key is not None:
            if current_content:
                block = "\n".join(current_content).strip()
                block = re.sub(r"\s+[\*\-•]\s+", "\n* ", block)
                sections[current_section] = block
            current_section = key
            current_content = []
            continue
        current_content.append(line)

    if current_content:
        block = "\n".join(current_content).strip()
        block = re.sub(r"\s+[\*\-•]\s+", "\n* ", block)
        sections[current_section] = block

    # Drop introduction if empty
    if "introduction" in sections and not sections["introduction"]:
        del sections["introduction"]

    return sections
