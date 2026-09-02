# ☉ Jyotish — Vedic Birth Chart & AI Reading

Full-stack Vedic astrology web app. FastAPI serves the API and static frontend from a single deployment on Render.

## Features

- North Indian Kundali chart (diamond SVG) + Navamsa (D9)
- Accurate sidereal planetary positions (Swiss Ephemeris, Lahiri Ayanamsa, Whole Sign Houses)
- Vimshottari Dasha timeline with Antardasha expansion
- Yoga detection (Panch Mahapurusha, Gajakesari, Budhaditya, Raj, Dhana, and more)
- Dosha analysis with cancellation checks and remedies
- Rule-based reading for every placement
- AI deep reading powered by Claude

## Local Development

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # optional, for AI readings
uvicorn main:app --reload
```

Open `http://localhost:8000`.

## Deploy to Render

1. Push all files to a GitHub repo (flat, no subfolders needed)
2. Create a **Web Service** on Render → connect the repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `ANTHROPIC_API_KEY`

## Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app — API endpoints + static file serving |
| `astro_engine.py` | Swiss Ephemeris calculations — sidereal positions, nakshatras, navamsa |
| `dasha.py` | Vimshottari Mahadasha + Antardasha |
| `yogas.py` | Yoga detection (10 types) |
| `doshas.py` | Dosha detection (6 types with cancellations) |
| `interpretations.py` | Rule-based chart readings |
| `ai_reader.py` | Claude API integration for deep readings |
| `index.html` | Frontend page |
| `style.css` | Premium dark theme |
| `app.js` | Frontend logic (vanilla JS) |
| `favicon.svg` | App icon |
| `requirements.txt` | Python dependencies |
| `render.yaml` | Render deployment config |

## Tech

- **Ayanamsa**: Lahiri (Chitrapaksha)
- **Houses**: Whole Sign
- **Ephemeris**: Moshier (built-in, no external data files)
- **Geocoding**: Nominatim (OpenStreetMap)
- **Timezone**: Auto via timezonefinder + pytz
