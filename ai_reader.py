"""
AI-Powered Deep Chart Reading using Anthropic Claude API.
Generates personalized, insightful interpretations of the birth chart.
"""

import os
import httpx
from typing import Optional

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = "claude-sonnet-5"
API_URL = "https://api.anthropic.com/v1/messages"


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
    """Generate a deep AI reading of the birth chart using Claude."""

    if not ANTHROPIC_API_KEY:
        return {
            "error": "AI reading unavailable — ANTHROPIC_API_KEY not configured.",
            "sections": {},
        }

    chart_text = _format_chart_for_prompt(name, chart, dashas, yogas, doshas)

    system_prompt = """You are an expert Vedic astrologer (Jyotishi) with deep knowledge of
classical texts (Brihat Parashara Hora Shastra, Phaladeepika, Jataka Parijata).

Analyze the birth chart provided and give a comprehensive reading. Be insightful,
specific to the chart combinations, and balanced — highlight both strengths and
areas requiring attention.

Structure your response in these sections:

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

Use both Sanskrit terms and English explanations. Be authentic to the Jyotish tradition
while being accessible. Avoid generic statements — every insight should be traceable
to a specific chart combination."""

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                API_URL,
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": MODEL,
                    "max_tokens": 4000,
                    "system": system_prompt,
                    "messages": [
                        {"role": "user", "content": chart_text}
                    ],
                },
            )

            if response.status_code != 200:
                err_body = response.text
                try:
                    err_json = response.json()
                    err_body = err_json.get("error", {}).get("message", err_body)
                except Exception:
                    pass
                return {
                    "error": f"AI API error ({response.status_code}): {err_body}",
                    "sections": {},
                }

            data = response.json()
            content = data.get("content", [])
            text = "\n".join(
                block.get("text", "") for block in content if block.get("type") == "text"
            )

            # Parse sections
            sections = _parse_sections(text)

            return {
                "full_text": text,
                "sections": sections,
            }

    except Exception as e:
        return {
            "error": f"AI reading failed: {str(e)}",
            "sections": {},
        }


def _parse_sections(text: str) -> dict:
    """Parse the AI response into sections based on ## headers."""
    sections = {}
    current_section = "introduction"
    current_content = []

    for line in text.split("\n"):
        if line.startswith("## "):
            if current_content:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = line[3:].strip().lower().replace(" ", "_").replace("&", "and")
            current_content = []
        else:
            current_content.append(line)

    if current_content:
        sections[current_section] = "\n".join(current_content).strip()

    return sections
