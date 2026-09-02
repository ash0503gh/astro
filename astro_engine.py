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


def _geocode_city(city: str) -> tuple:
    """Convert city name to (latitude, longitude)."""
    geolocator = Nominatim(user_agent="jyotish-app")
    location = geolocator.geocode(city)
    if not location:
        raise ValueError(f"Could not geocode city: {city}")
    return location.latitude, location.longitude


def _get_timezone(lat: float, lon: float, dt: datetime) -> tuple:
    """Get timezone name and UTC offset for a location at a given datetime."""
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon)
    if not tz_name:
        tz_name = "UTC"
    tz = pytz.timezone(tz_name)
    local_dt = tz.localize(dt)
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
