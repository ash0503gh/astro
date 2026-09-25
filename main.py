"""
Jyotish — Vedic Birth Chart & AI Reading
FastAPI backend serving API + static frontend (single deployment)
"""

from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from astro_engine import compute_chart, _geocode_city, search_cities
from dasha import compute_vimshottari_dasha
from yogas import detect_yogas
from doshas import detect_doshas
from interpretations import generate_basic_reading
from ai_reader import generate_ai_reading
from qa_engine import ask_jyotishi

BASE_DIR = Path(__file__).parent

app = FastAPI(title="Jyotish API", version="1.0.0")

# The frontend is served from this same origin; no other site needs browser access.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://astro-mze8.onrender.com"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# ── AI Abuse Guard (every AI request is a paid Gemini call) ──

MAX_QUESTION_CHARS = 500
MAX_HISTORY_CHARS = 2000  # per chat message; the frontend sends at most the last 6
AI_DAILY_LIMITS = {"reading": 10, "question": 50}  # per client IP, reset at 00:00 UTC
AI_LIMIT_MESSAGES = {
    ("reading", "en"): "Daily limit reached for AI readings ({limit} per day). Please try again tomorrow.",
    ("reading", "hi"): "आज की एआई फलादेश सीमा ({limit} प्रति दिन) पूरी हो गई है। कृपया कल पुनः प्रयास करें।",
    ("question", "en"): "Daily limit reached for questions ({limit} per day). Please try again tomorrow.",
    ("question", "hi"): "आज के प्रश्नों की सीमा ({limit} प्रति दिन) पूरी हो गई है। कृपया कल पुनः प्रयास करें।",
}
_ai_usage: Dict[tuple, int] = defaultdict(int)
_ai_usage_day = ""


def _client_ip(request: Request) -> str:
    # Render sits behind Cloudflare, which sets CF-Connecting-IP / True-Client-IP and
    # overwrites client-sent values. The first X-Forwarded-For entry can be spoofed.
    return (
        request.headers.get("cf-connecting-ip")
        or request.headers.get("true-client-ip")
        or (request.client.host if request.client else "unknown")
    )


def _check_ai_quota(request: Request, kind: str, language: Optional[str]) -> None:
    """Count one Gemini call for this client; raise 429 once today's limit is used up."""
    global _ai_usage_day
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if today != _ai_usage_day:
        _ai_usage.clear()
        _ai_usage_day = today
    key = (_client_ip(request), kind)
    limit = AI_DAILY_LIMITS[kind]
    if _ai_usage[key] >= limit:
        lang = "hi" if language == "hi" else "en"
        raise HTTPException(status_code=429, detail=AI_LIMIT_MESSAGES[(kind, lang)].format(limit=limit))
    _ai_usage[key] += 1


# ── Models ──

class BirthInput(BaseModel):
    name: str = Field(max_length=100)
    birth_date: str
    birth_time: str
    birth_city: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone_offset: Optional[float] = None
    language: Optional[str] = "en"


class ChatMessage(BaseModel):
    role: str
    content: str


class AskJyotishiInput(BaseModel):
    name: str = Field(max_length=100)
    birth_date: str
    birth_time: str
    birth_city: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone_offset: Optional[float] = None
    question: str = Field(max_length=MAX_QUESTION_CHARS)
    history: Optional[List[ChatMessage]] = None
    language: Optional[str] = "en"


# ── API Endpoints ──
# Endpoints doing blocking work (geocoding HTTP calls, chart math) are plain `def`
# so FastAPI runs them in its threadpool instead of freezing the event loop.

@app.post("/api/chart")
def api_chart(data: BirthInput):
    """Full Vedic birth chart with all calculations."""
    try:
        chart = compute_chart(
            birth_date=data.birth_date,
            birth_time=data.birth_time,
            birth_city=data.birth_city,
            latitude=data.latitude,
            longitude=data.longitude,
            tz_offset=data.timezone_offset,
        )
        dashas = compute_vimshottari_dasha(chart["moon_longitude"], data.birth_date)
        yogas = detect_yogas(chart["planets"], chart["houses"], chart["ascendant"])
        doshas_list = detect_doshas(chart["planets"], chart["houses"])
        lang = data.language or "en"
        basic_reading = generate_basic_reading(
            chart["planets"], chart["houses"], chart["ascendant"], yogas, doshas_list,
            language=lang,
        )
        chart_data = _prepare_chart_data(chart)

        return {
            "name": data.name,
            "language": lang,
            "birth_info": {
                "date": data.birth_date,
                "time": data.birth_time,
                "city": data.birth_city,
                "latitude": chart["latitude"],
                "longitude": chart["longitude"],
                "timezone": chart["timezone"],
            },
            "planets": chart["planets"],
            "houses": chart["houses"],
            "ascendant": chart["ascendant"],
            "nakshatras": chart["nakshatras"],
            "navamsa": chart["navamsa"],
            "dashas": dashas,
            "yogas": yogas,
            "doshas": doshas_list,
            "basic_reading": basic_reading,
            "chart_data": chart_data,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ai-reading")
async def api_ai_reading(data: BirthInput, request: Request):
    """AI-powered deep chart reading via Google Gemini."""
    try:
        chart = await run_in_threadpool(
            compute_chart,
            birth_date=data.birth_date,
            birth_time=data.birth_time,
            birth_city=data.birth_city,
            latitude=data.latitude,
            longitude=data.longitude,
            tz_offset=data.timezone_offset,
        )
        dashas = compute_vimshottari_dasha(chart["moon_longitude"], data.birth_date)
        yogas = detect_yogas(chart["planets"], chart["houses"], chart["ascendant"])
        doshas_list = detect_doshas(chart["planets"], chart["houses"])
        _check_ai_quota(request, "reading", data.language)
        reading = await generate_ai_reading(
            name=data.name, chart=chart,
            dashas=dashas, yogas=yogas, doshas=doshas_list,
            language=data.language or "en",
        )
        return {"reading": reading}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ask-jyotishi")
async def api_ask_jyotishi(data: AskJyotishiInput, request: Request):
    """Interactive Astrological Q&A powered by Gemini 2.5 Flash."""
    try:
        # Always rebuild the chart here: client-sent chart data never reaches the prompt.
        chart = await run_in_threadpool(
            compute_chart,
            birth_date=data.birth_date,
            birth_time=data.birth_time,
            birth_city=data.birth_city,
            latitude=data.latitude,
            longitude=data.longitude,
            tz_offset=data.timezone_offset,
        )
        dashas = compute_vimshottari_dasha(chart["moon_longitude"], data.birth_date)
        yogas = detect_yogas(chart["planets"], chart["houses"], chart["ascendant"])
        doshas_list = detect_doshas(chart["planets"], chart["houses"])

        history_list = [
            {"role": msg.role, "content": msg.content[:MAX_HISTORY_CHARS]}
            for msg in (data.history or [])[-6:]
        ]

        _check_ai_quota(request, "question", data.language)

        result = await ask_jyotishi(
            name=data.name,
            chart=chart,
            dashas=dashas,
            yogas=yogas,
            doshas=doshas_list,
            question=data.question,
            history=history_list,
            language=data.language or "en",
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/geocode")
def api_geocode(data: dict):
    city = data.get("city", "").strip()
    if not city:
        raise HTTPException(status_code=400, detail="City required")
    try:
        lat, lon = _geocode_city(city)
        return {"city": city, "latitude": lat, "longitude": lon, "display_name": city}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/cities")
def api_cities(q: str = ""):
    """City autocomplete endpoint with 1-hour browser cache."""
    if not q or len(q.strip()) < 2:
        return JSONResponse(
            content={"cities": []},
            headers={"Cache-Control": "public, max-age=3600"}
        )
    return JSONResponse(
        content={"cities": search_cities(q.strip())},
        headers={"Cache-Control": "public, max-age=3600"}
    )


@app.get("/health")
async def health():
    return {"status": "ok"}


# ── Static Frontend ──

@app.get("/")
@app.get("/index.html")
async def serve_index():
    return FileResponse(
        BASE_DIR / "index.html",
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
        }
    )

@app.get("/app.js")
async def serve_app_js():
    return FileResponse(
        BASE_DIR / "app.js",
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
        }
    )

@app.get("/style.css")
async def serve_style_css():
    return FileResponse(
        BASE_DIR / "style.css",
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
        }
    )

@app.get("/favicon.svg")
async def serve_favicon():
    return FileResponse(BASE_DIR / "favicon.svg")


# Only the files above are public. Never mount BASE_DIR as static: it would serve
# source code, .env and .git/ from the project folder.


# ── Helpers ──

def _prepare_chart_data(chart: dict) -> dict:
    house_planets = {i: [] for i in range(1, 13)}
    for planet in chart["planets"]:
        house_planets[planet["house"]].append({
            "name": planet["name"],
            "symbol": planet["symbol"],
            "degree": planet["degree_in_sign"],
            "retro": planet.get("retrograde", False),
        })
    asc_sign = chart["ascendant"]["sign_num"]
    house_signs = {}
    for i in range(1, 13):
        house_signs[i] = ((asc_sign - 1 + i - 1) % 12) + 1
    return {
        "house_planets": house_planets,
        "house_signs": house_signs,
        "ascendant_sign": asc_sign,
    }
