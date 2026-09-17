"""
AI-Powered Deep Chart Reading using Google Gemini API.
Generates personalized, insightful interpretations of the birth chart.
"""

import os
import re
import httpx
from typing import Optional

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
FALLBACK_MODELS = [DEFAULT_MODEL, "gemini-2.0-flash", "gemini-1.5-flash"]
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"


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


async def generate_ai_reading(
    name: str,
    chart: dict,
    dashas: list,
    yogas: list,
    doshas: list,
) -> dict:
    """Generate a deep AI reading of the birth chart using Google Gemini."""

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        return {
            "error": "AI reading unavailable — GEMINI_API_KEY not configured on backend.",
            "sections": {},
        }

    chart_text = _format_chart_for_prompt(name, chart, dashas, yogas, doshas)

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

Use both Sanskrit terms and English explanations. Be authentic to the Jyotish tradition
while being accessible. Avoid generic statements — every insight should be traceable
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
                    # Model not available in this tier/region, try next fallback
                    last_error = f"Model '{model}' not found (404)."
                    continue

                if response.status_code != 200:
                    err_body = response.text
                    try:
                        err_json = response.json()
                        err_body = err_json.get("error", {}).get("message", err_body)
                    except Exception:
                        pass
                    return {
                        "error": f"Gemini API error ({response.status_code}): {err_body}",
                        "sections": {},
                    }

                data = response.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    prompt_feedback = data.get("promptFeedback", {})
                    block_reason = prompt_feedback.get("blockReason")
                    if block_reason:
                        return {
                            "error": f"AI generation blocked by safety filters: {block_reason}",
                            "sections": {},
                        }
                    return {
                        "error": "Gemini returned an empty response.",
                        "sections": {},
                    }

                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                text = "\n".join(part.get("text", "") for part in parts if "text" in part)

                if not text.strip():
                    return {
                        "error": "Gemini generated no text content.",
                        "sections": {},
                    }

                # Parse sections
                sections = _parse_sections(text)

                return {
                    "full_text": text,
                    "sections": sections,
                    "model_used": model,
                }

            except httpx.TimeoutException:
                return {
                    "error": "Gemini API request timed out (60s). Please try again.",
                    "sections": {},
                }
            except Exception as e:
                last_error = str(e)
                continue

    return {
        "error": f"AI reading failed: {last_error or 'Unable to contact Gemini API'}",
        "sections": {},
    }


def _parse_sections(text: str) -> dict:
    """Parse the AI response into sections based on markdown headers."""
    sections = {}
    current_section = "introduction"
    current_content = []

    for line in text.split("\n"):
        match = re.match(r"^#{1,3}\s+(?:[0-9]+[\.\)]\s*)?(.+)", line)
        if match:
            header_raw = match.group(1).strip(" :*#")
            if len(header_raw) > 2:
                if current_content:
                    block = "\n".join(current_content).strip()
                    block = re.sub(r'([^\n])\s*[\*\-•]\s+(\*\*|[A-Za-z0-9])', r'\1\n* \2', block)
                    sections[current_section] = block
                normalized_key = (
                    header_raw.lower()
                    .replace("&", "and")
                    .replace("/", "_")
                    .replace("-", "_")
                )
                normalized_key = re.sub(r"[^\w\s]", "", normalized_key)
                normalized_key = re.sub(r"\s+", "_", normalized_key).strip("_")
                current_section = normalized_key
                current_content = []
                continue
        current_content.append(line)

    if current_content:
        block = "\n".join(current_content).strip()
        block = re.sub(r'([^\n])\s*[\*\-•]\s+(\*\*|[A-Za-z0-9])', r'\1\n* \2', block)
        sections[current_section] = block

    # Drop introduction if empty
    if "introduction" in sections and not sections["introduction"]:
        del sections["introduction"]

    return sections
