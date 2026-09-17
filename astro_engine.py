"""
Core Vedic Astrology Engine
Uses Swiss Ephemeris (pyswisseph) for planetary calculations
with Lahiri Ayanamsa (sidereal zodiac).
"""

import swisseph as swe
from datetime import datetime
from typing import Optional
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
import httpx

# --- Constants ---

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

SIGN_LORDS = [
    "Mars", "Venus", "Mercury", "Moon",
    "Sun", "Mercury", "Venus", "Mars",
    "Jupiter", "Saturn", "Saturn", "Jupiter"
]

NAKSHATRAS = [
    ("Ashwini", "Ketu"), ("Bharani", "Venus"), ("Krittika", "Sun"),
    ("Rohini", "Moon"), ("Mrigashira", "Mars"), ("Ardra", "Rahu"),
    ("Punarvasu", "Jupiter"), ("Pushya", "Saturn"), ("Ashlesha", "Mercury"),
    ("Magha", "Ketu"), ("Purva Phalguni", "Venus"), ("Uttara Phalguni", "Sun"),
    ("Hasta", "Moon"), ("Chitra", "Mars"), ("Swati", "Rahu"),
    ("Vishakha", "Jupiter"), ("Anuradha", "Saturn"), ("Jyeshtha", "Mercury"),
    ("Moola", "Ketu"), ("Purva Ashadha", "Venus"), ("Uttara Ashadha", "Sun"),
    ("Shravana", "Moon"), ("Dhanishta", "Mars"), ("Shatabhisha", "Rahu"),
    ("Purva Bhadrapada", "Jupiter"), ("Uttara Bhadrapada", "Saturn"), ("Revati", "Mercury"),
]

NAKSHATRA_SPAN = 13.333333333  # 13°20' per nakshatra

PLANETS = [
    {"id": swe.SUN, "name": "Sun", "vedic": "Surya", "symbol": "Su"},
    {"id": swe.MOON, "name": "Moon", "vedic": "Chandra", "symbol": "Mo"},
    {"id": swe.MARS, "name": "Mars", "vedic": "Mangal", "symbol": "Ma"},
    {"id": swe.MERCURY, "name": "Mercury", "vedic": "Budha", "symbol": "Me"},
    {"id": swe.JUPITER, "name": "Jupiter", "vedic": "Guru", "symbol": "Ju"},
    {"id": swe.VENUS, "name": "Venus", "vedic": "Shukra", "symbol": "Ve"},
    {"id": swe.SATURN, "name": "Saturn", "vedic": "Shani", "symbol": "Sa"},
    {"id": swe.MEAN_NODE, "name": "Rahu", "vedic": "Rahu", "symbol": "Ra"},
]

# Planet dignities: {planet_name: {exalted_sign, debilitated_sign, own_signs}}
DIGNITIES = {
    "Sun":     {"exalted": 1, "debilitated": 7, "own": [5]},
    "Moon":    {"exalted": 2, "debilitated": 8, "own": [4]},
    "Mars":    {"exalted": 10, "debilitated": 4, "own": [1, 8]},
    "Mercury": {"exalted": 6, "debilitated": 12, "own": [3, 6]},
    "Jupiter": {"exalted": 4, "debilitated": 10, "own": [9, 12]},
    "Venus":   {"exalted": 12, "debilitated": 6, "own": [2, 7]},
    "Saturn":  {"exalted": 7, "debilitated": 1, "own": [10, 11]},
    "Rahu":    {"exalted": 3, "debilitated": 9, "own": [11]},
    "Ketu":    {"exalted": 9, "debilitated": 3, "own": [8]},
}


MAJOR_CITIES = {
    # India - Metros & Major Cities
    "delhi": (28.6139, 77.2090),
    "new delhi": (28.6139, 77.2090),
    "mumbai": (19.0760, 72.8777),
    "bombay": (19.0760, 72.8777),
    "bengaluru": (12.9716, 77.5946),
    "bangalore": (12.9716, 77.5946),
    "hyderabad": (17.3850, 78.4867),
    "chennai": (13.0827, 80.2707),
    "madras": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "calcutta": (22.5726, 88.3639),
    "pune": (18.5204, 73.8567),
    "ahmedabad": (23.0225, 72.5714),
    "jaipur": (26.9124, 75.7873),
    "surat": (21.1702, 72.8311),
    "lucknow": (26.8467, 80.9462),
    "kanpur": (26.4499, 80.3319),
    "nagpur": (21.1458, 79.0882),
    "indore": (22.7196, 75.8577),
    "thane": (19.2183, 72.9781),
    "bhopal": (23.2599, 77.4126),
    "visakhapatnam": (17.6868, 83.2185),
    "vizag": (17.6868, 83.2185),
    "patna": (25.5941, 85.1376),
    "vadodara": (22.3072, 73.1812),
    "baroda": (22.3072, 73.1812),
    "ghaziabad": (28.6692, 77.4538),
    "ludhiana": (30.9010, 75.8573),
    "agra": (27.1767, 78.0081),
    "nashik": (19.9975, 73.7898),
    "faridabad": (28.4089, 77.3178),
    "meerut": (28.9845, 77.7064),
    "rajkot": (22.3039, 70.8022),
    "varanasi": (25.3176, 82.9739),
    "banaras": (25.3176, 82.9739),
    "kashi": (25.3176, 82.9739),
    "srinagar": (34.0837, 74.7973),
    "aurangabad": (19.8762, 75.3433),
    "chhatrapati sambhajinagar": (19.8762, 75.3433),
    "dhanbad": (23.7957, 86.4304),
    "amritsar": (31.6340, 74.8723),
    "navi mumbai": (19.0330, 73.0297),
    "allahabad": (25.4358, 81.8463),
    "prayagraj": (25.4358, 81.8463),
    "ranchi": (23.3441, 85.3096),
    "howrah": (22.5958, 88.2636),
    "coimbatore": (11.0168, 76.9558),
    "jabalpur": (23.1815, 79.9864),
    "gwalior": (26.2183, 78.1828),
    "vijayawada": (16.5062, 80.6480),
    "jodhpur": (26.2389, 73.0243),
    "madurai": (9.9252, 78.1198),
    "raipur": (21.2514, 81.6296),
    "kota": (25.2138, 75.8648),
    "chandigarh": (30.7333, 76.7794),
    "guwahati": (26.1445, 91.7362),
    "solapur": (17.6599, 75.9064),
    "hubli": (15.3647, 75.1240),
    "mysore": (12.2958, 76.6394),
    "mysuru": (12.2958, 76.6394),
    "tiruchirappalli": (10.7905, 78.7047),
    "trichy": (10.7905, 78.7047),
    "bareilly": (28.3670, 79.4304),
    "aligarh": (27.8974, 78.0880),
    "tiruppur": (11.1085, 77.3411),
    "gurgaon": (28.4595, 77.0266),
    "gurugram": (28.4595, 77.0266),
    "noida": (28.5355, 77.3910),
    "greater noida": (28.4744, 77.5040),
    "moradabad": (28.8356, 78.7747),
    "jalandhar": (31.3260, 75.5762),
    "bhubaneswar": (20.2961, 85.8245),
    "salem": (11.6643, 78.1460),
    "warangal": (17.9689, 79.5941),
    "jalgaon": (21.0077, 75.5626),
    "kochi": (9.9312, 76.2673),
    "cochin": (9.9312, 76.2673),
    "dehradun": (30.3165, 78.0322),
    "jamnagar": (22.4707, 70.0577),
    "ujjain": (23.1765, 75.7885),
    "haridwar": (29.9457, 78.1642),
    "rishikesh": (30.0869, 78.2676),
    "mangalore": (12.9141, 74.8560),
    "mangaluru": (12.9141, 74.8560),
    "belgaum": (15.8497, 74.4977),
    "udaipur": (24.5854, 73.7125),
    "ajmer": (26.4499, 74.6399),
    "mathura": (27.4924, 77.6737),
    "ayodhya": (26.7922, 82.1998),
    "shimla": (31.1048, 77.1734),
    "jammu": (32.7266, 74.8570),
    "panaji": (15.4909, 73.8278),
    "goa": (15.2993, 74.1240),
    "puducherry": (11.9416, 79.8083),
    "pondicherry": (11.9416, 79.8083),
    "calicut": (11.2588, 75.7804),
    "kozhikode": (11.2588, 75.7804),
    "thrissur": (10.5276, 76.2144),
    "gaya": (24.7914, 85.0002),
    "tirupati": (13.6288, 79.4192),
    "kurnool": (15.8281, 78.0373),
    "nellore": (14.4426, 79.9865),
    "anantapur": (14.6819, 77.6006),
    "rohtak": (28.8955, 76.6066),
    "panipat": (29.3909, 76.9635),
    "karnal": (29.6857, 76.9905),
    "jhansi": (25.4484, 78.5685),
    "gorakhpur": (26.7606, 83.3732),
    "saharanpur": (29.9640, 77.5460),
    "bhilai": (21.2121, 81.3733),
    "cuttack": (20.4625, 85.8830),
    "puri": (19.8135, 85.8312),
    "siliguri": (26.7271, 88.3953),
    "asansol": (23.6739, 86.9524),
    "durgapur": (23.5204, 87.3119),
    "kolhapur": (16.7050, 74.2433),
    "bhavnagar": (21.7645, 72.1519),
    "gandhinagar": (23.2156, 72.6369),
    "bikaner": (28.0229, 73.3119),
    "alwar": (27.5530, 76.6346),
    "jamshedpur": (22.8046, 86.2029),

    # Global Hubs
    "new york": (40.7128, -74.0060),
    "nyc": (40.7128, -74.0060),
    "london": (51.5074, -0.1278),
    "toronto": (43.6532, -79.3832),
    "vancouver": (49.2827, -123.1207),
    "dubai": (25.2048, 55.2708),
    "abu dhabi": (24.4539, 54.3773),
    "singapore": (1.3521, 103.8198),
    "sydney": (-33.8688, 151.2093),
    "melbourne": (-37.8136, 144.9631),
    "san francisco": (37.7749, -122.4194),
    "los angeles": (34.0522, -118.2437),
    "chicago": (41.8781, -87.6298),
    "seattle": (47.6062, -122.3321),
    "dallas": (32.7767, -96.7970),
    "houston": (29.7604, -95.3698),
    "tokyo": (35.6762, 139.6503),
    "paris": (48.8566, 2.3522),
    "berlin": (52.5200, 13.4050),
}


def _geocode_city(city: str) -> tuple:
    """Convert city name to (latitude, longitude) with robust multi-tier fallback.
    
    1. Fast offline local dictionary (0ms, zero network dependency)
    2. Open-Meteo Geocoding API (fast, reliable, free)
    3. Nominatim with 10s timeout and unique User-Agent
    """
    clean_name = city.strip().lower()

    # Tier 1: Local cache of major cities
    if clean_name in MAJOR_CITIES:
        return MAJOR_CITIES[clean_name]

    # Check partial match (e.g. "jaipur, rajasthan" -> "jaipur")
    primary_token = clean_name.split(",")[0].strip()
    if primary_token in MAJOR_CITIES:
        return MAJOR_CITIES[primary_token]

    # Tier 2: Open-Meteo Geocoding API
    try:
        resp = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=6.0,
        )
        if resp.status_code == 200:
            results = resp.json().get("results")
            if results and len(results) > 0:
                return float(results[0]["latitude"]), float(results[0]["longitude"])
    except Exception:
        pass

    # Tier 3: Nominatim with 10s timeout and unique user-agent
    try:
        geolocator = Nominatim(user_agent="jyotish-vedic-chart-v2", timeout=10)
        location = geolocator.geocode(city)
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass

    raise ValueError(
        f"Could not find coordinates for '{city}'. Please check the spelling or enter a nearby major city."
    )


def _get_timezone(lat: float, lon: float, dt: datetime) -> tuple:
    """Get timezone name and UTC offset for a location at a given datetime."""
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon)
    if not tz_name:
        tz_name = "UTC"
    tz = pytz.timezone(tz_name)
    try:
        local_dt = tz.localize(dt)
    except Exception:
        try:
            local_dt = tz.localize(dt, is_dst=False)
        except Exception:
            local_dt = dt.replace(tzinfo=pytz.UTC)
    utc_offset = local_dt.utcoffset().total_seconds() / 3600
    return tz_name, utc_offset


def _to_julian_day(dt_utc: datetime) -> float:
    """Convert UTC datetime to Julian Day."""
    return swe.julday(
        dt_utc.year, dt_utc.month, dt_utc.day,
        dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    )


def _get_nakshatra(longitude: float) -> dict:
    """Get nakshatra details from absolute sidereal longitude."""
    nak_index = int(longitude / NAKSHATRA_SPAN)
    nak_index = min(nak_index, 26)
    nak_name, nak_lord = NAKSHATRAS[nak_index]
    pada = int((longitude % NAKSHATRA_SPAN) / (NAKSHATRA_SPAN / 4)) + 1
    pada = min(pada, 4)
    degree_in_nak = longitude % NAKSHATRA_SPAN
    return {
        "name": nak_name,
        "lord": nak_lord,
        "pada": pada,
        "degree": round(degree_in_nak, 2),
        "index": nak_index,
    }


def _get_sign(longitude: float) -> dict:
    """Get rashi (sign) from sidereal longitude."""
    sign_index = int(longitude / 30)
    sign_index = min(sign_index, 11)
    degree_in_sign = longitude % 30
    return {
        "sign_num": sign_index + 1,  # 1-12
        "sign": SIGNS[sign_index],
        "sign_english": SIGN_ENGLISH[sign_index],
        "lord": SIGN_LORDS[sign_index],
        "degree_in_sign": round(degree_in_sign, 2),
    }


def _get_navamsa_sign(longitude: float) -> dict:
    """Calculate Navamsa (D9) sign from sidereal longitude.
    Each navamsa = 3°20'. 9 navamsas per sign.
    Navamsa cycle: starts from the sign itself for movable,
    9th sign for fixed, 5th sign for dual signs.
    """
    sign_index = int(longitude / 30)
    degree_in_sign = longitude % 30
    navamsa_num = int(degree_in_sign / (30 / 9))  # 0-8

    # Starting sign for navamsa based on sign type
    if sign_index % 3 == 0:  # Movable (Aries, Cancer, Libra, Capricorn)
        start = sign_index
    elif sign_index % 3 == 1:  # Fixed (Taurus, Leo, Scorpio, Aquarius)
        start = sign_index + 8  # 9th from sign (0-indexed +8)
    else:  # Dual (Gemini, Virgo, Sagittarius, Pisces)
        start = sign_index + 4  # 5th from sign (0-indexed +4)

    navamsa_sign_index = (start + navamsa_num) % 12
    return {
        "sign_num": navamsa_sign_index + 1,
        "sign": SIGNS[navamsa_sign_index],
        "sign_english": SIGN_ENGLISH[navamsa_sign_index],
        "lord": SIGN_LORDS[navamsa_sign_index],
    }


def _get_dignity(planet_name: str, sign_num: int) -> str:
    """Determine planet's dignity in a sign."""
    if planet_name not in DIGNITIES:
        return "neutral"
    d = DIGNITIES[planet_name]
    if sign_num == d["exalted"]:
        return "exalted"
    if sign_num == d["debilitated"]:
        return "debilitated"
    if sign_num in d["own"]:
        return "own_sign"
    # Friendly / enemy / neutral — simplified
    return "neutral"


def compute_chart(
    birth_date: str,
    birth_time: str,
    birth_city: str,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    tz_offset: Optional[float] = None,
) -> dict:
    """Compute full Vedic birth chart.

    Returns dict with planets, houses, ascendant, nakshatras, navamsa.
    """
    # --- Resolve location ---
    if latitude is None or longitude is None:
        latitude, longitude = _geocode_city(birth_city)

    # --- Parse datetime ---
    dt_parts = birth_date.split("-")
    tm_parts = birth_time.split(":")
    local_dt = datetime(
        int(dt_parts[0]), int(dt_parts[1]), int(dt_parts[2]),
        int(tm_parts[0]), int(tm_parts[1])
    )

    # --- Timezone ---
    if tz_offset is None:
        tz_name, tz_offset = _get_timezone(latitude, longitude, local_dt)
    else:
        tz_name = f"UTC{'+' if tz_offset >= 0 else ''}{tz_offset}"

    # Convert local time to UTC
    utc_hour = local_dt.hour + local_dt.minute / 60.0 - tz_offset
    dt_utc = datetime(
        local_dt.year, local_dt.month, local_dt.day,
        0, 0
    )
    # Handle day rollover
    from datetime import timedelta
    dt_utc = local_dt - timedelta(hours=tz_offset)

    jd = _to_julian_day(dt_utc)

    # --- Set sidereal mode (Lahiri Ayanamsa) ---
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayanamsa = swe.get_ayanamsa(jd)

    # --- Calculate Ascendant (Lagna) ---
    # Using Placidus houses but extracting only ascendant for whole-sign system
    cusps, ascmc = swe.houses(jd, latitude, longitude, b'P')
    asc_tropical = ascmc[0]
    asc_sidereal = (asc_tropical - ayanamsa) % 360

    asc_sign_info = _get_sign(asc_sidereal)
    asc_nakshatra = _get_nakshatra(asc_sidereal)

    ascendant = {
        **asc_sign_info,
        "longitude": round(asc_sidereal, 4),
        "nakshatra": asc_nakshatra,
    }

    # --- Calculate planet positions ---
    planets_data = []
    moon_longitude = 0.0
    nakshatras_info = {}

    for p in PLANETS:
        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
        result = swe.calc_ut(jd, p["id"], flags)
        lon = result[0][0] % 360
        speed = result[0][3]
        is_retrograde = speed < 0

        sign_info = _get_sign(lon)
        nak_info = _get_nakshatra(lon)
        navamsa = _get_navamsa_sign(lon)

        # Determine house using whole-sign system
        house = ((sign_info["sign_num"] - asc_sign_info["sign_num"]) % 12) + 1

        planet_name = p["name"]
        dignity = _get_dignity(planet_name, sign_info["sign_num"])

        planet_data = {
            "name": planet_name,
            "vedic_name": p["vedic"],
            "symbol": p["symbol"],
            "longitude": round(lon, 4),
            **sign_info,
            "house": house,
            "nakshatra": nak_info,
            "navamsa": navamsa,
            "retrograde": is_retrograde,
            "speed": round(speed, 4),
            "dignity": dignity,
        }
        planets_data.append(planet_data)
        nakshatras_info[planet_name] = nak_info

        if planet_name == "Moon":
            moon_longitude = lon

    # --- Add Ketu (opposite of Rahu) ---
    rahu_data = next(p for p in planets_data if p["name"] == "Rahu")
    ketu_lon = (rahu_data["longitude"] + 180) % 360
    ketu_sign = _get_sign(ketu_lon)
    ketu_nak = _get_nakshatra(ketu_lon)
    ketu_navamsa = _get_navamsa_sign(ketu_lon)
    ketu_house = ((ketu_sign["sign_num"] - asc_sign_info["sign_num"]) % 12) + 1
    ketu_dignity = _get_dignity("Ketu", ketu_sign["sign_num"])

    planets_data.append({
        "name": "Ketu",
        "vedic_name": "Ketu",
        "symbol": "Ke",
        "longitude": round(ketu_lon, 4),
        **ketu_sign,
        "house": ketu_house,
        "nakshatra": ketu_nak,
        "navamsa": ketu_navamsa,
        "retrograde": True,  # Ketu is always retrograde
        "speed": round(-rahu_data["speed"], 4),
        "dignity": ketu_dignity,
    })
    nakshatras_info["Ketu"] = ketu_nak

    # --- Build houses data ---
    houses_data = []
    for i in range(1, 13):
        sign_num = ((asc_sign_info["sign_num"] - 1 + i - 1) % 12) + 1
        sign_idx = sign_num - 1
        houses_data.append({
            "house": i,
            "sign_num": sign_num,
            "sign": SIGNS[sign_idx],
            "sign_english": SIGN_ENGLISH[sign_idx],
            "lord": SIGN_LORDS[sign_idx],
            "planets": [p["symbol"] for p in planets_data if p["house"] == i],
        })

    # --- Navamsa chart data ---
    navamsa_data = []
    for p in planets_data:
        navamsa_data.append({
            "name": p["name"],
            "symbol": p["symbol"],
            "navamsa_sign": p["navamsa"]["sign"],
            "navamsa_sign_num": p["navamsa"]["sign_num"],
        })

    return {
        "planets": planets_data,
        "houses": houses_data,
        "ascendant": ascendant,
        "nakshatras": nakshatras_info,
        "navamsa": navamsa_data,
        "moon_longitude": moon_longitude,
        "ayanamsa": round(ayanamsa, 4),
        "julian_day": jd,
        "latitude": latitude,
        "longitude": longitude,
        "timezone": tz_name,
    }
