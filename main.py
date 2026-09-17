"""
Jyotish — Vedic Birth Chart & AI Reading
FastAPI backend serving API + static frontend (single deployment)
"""

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional

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

BASE_DIR = Path(__file__).parent

app = FastAPI(title="Jyotish API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Models ──

class BirthInput(BaseModel):
    name: str
    birth_date: str
    birth_time: str
    birth_city: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    timezone_offset: Optional[float] = None


# ── API Endpoints ──

@app.post("/api/chart")
async def api_chart(data: BirthInput):
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
        basic_reading = generate_basic_reading(
            chart["planets"], chart["houses"], chart["ascendant"], yogas, doshas_list
        )
        chart_data = _prepare_chart_data(chart)

        return {
            "name": data.name,
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
async def api_ai_reading(data: BirthInput):
    """AI-powered deep chart reading via Google Gemini."""
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
        reading = await generate_ai_reading(
            name=data.name, chart=chart,
            dashas=dashas, yogas=yogas, doshas=doshas_list,
        )
        return {"reading": reading}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/geocode")
async def api_geocode(data: dict):
    city = data.get("city", "").strip()
    if not city:
        raise HTTPException(status_code=400, detail="City required")
    try:
        lat, lon = _geocode_city(city)
        return {"city": city, "latitude": lat, "longitude": lon, "display_name": city}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/cities")
async def api_cities(q: str = ""):
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
async def serve_index():
    return FileResponse(BASE_DIR / "index.html")


# Mount static files LAST so API routes take priority
app.mount("/", StaticFiles(directory=BASE_DIR), name="static")


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
