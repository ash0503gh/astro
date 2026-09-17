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
    # India - Metros & Major Tier-1/2/3 Cities
    "delhi": (28.6139, 77.2090, "Delhi"),
    "new delhi": (28.6139, 77.2090, "Delhi"),
    "mumbai": (19.0760, 72.8777, "Maharashtra"),
    "bombay": (19.0760, 72.8777, "Maharashtra"),
    "bengaluru": (12.9716, 77.5946, "Karnataka"),
    "bangalore": (12.9716, 77.5946, "Karnataka"),
    "hyderabad": (17.3850, 78.4867, "Telangana"),
    "secunderabad": (17.4399, 78.4983, "Telangana"),
    "chennai": (13.0827, 80.2707, "Tamil Nadu"),
    "madras": (13.0827, 80.2707, "Tamil Nadu"),
    "kolkata": (22.5726, 88.3639, "West Bengal"),
    "calcutta": (22.5726, 88.3639, "West Bengal"),
    "pune": (18.5204, 73.8567, "Maharashtra"),
    "ahmedabad": (23.0225, 72.5714, "Gujarat"),
    "jaipur": (26.9124, 75.7873, "Rajasthan"),
    "surat": (21.1702, 72.8311, "Gujarat"),
    "lucknow": (26.8467, 80.9462, "Uttar Pradesh"),
    "kanpur": (26.4499, 80.3319, "Uttar Pradesh"),
    "nagpur": (21.1458, 79.0882, "Maharashtra"),
    "indore": (22.7196, 75.8577, "Madhya Pradesh"),
    "thane": (19.2183, 72.9781, "Maharashtra"),
    "bhopal": (23.2599, 77.4126, "Madhya Pradesh"),
    "visakhapatnam": (17.6868, 83.2185, "Andhra Pradesh"),
    "vizag": (17.6868, 83.2185, "Andhra Pradesh"),
    "patna": (25.5941, 85.1376, "Bihar"),
    "vadodara": (22.3072, 73.1812, "Gujarat"),
    "baroda": (22.3072, 73.1812, "Gujarat"),
    "ghaziabad": (28.6692, 77.4538, "Uttar Pradesh"),
    "ludhiana": (30.9010, 75.8573, "Punjab"),
    "agra": (27.1767, 78.0081, "Uttar Pradesh"),
    "nashik": (19.9975, 73.7898, "Maharashtra"),
    "faridabad": (28.4089, 77.3178, "Haryana"),
    "meerut": (28.9845, 77.7064, "Uttar Pradesh"),
    "rajkot": (22.3039, 70.8022, "Gujarat"),
    "varanasi": (25.3176, 82.9739, "Uttar Pradesh"),
    "banaras": (25.3176, 82.9739, "Uttar Pradesh"),
    "kashi": (25.3176, 82.9739, "Uttar Pradesh"),
    "srinagar": (34.0837, 74.7973, "Jammu & Kashmir"),
    "aurangabad": (19.8762, 75.3433, "Maharashtra"),
    "chhatrapati sambhajinagar": (19.8762, 75.3433, "Maharashtra"),
    "dhanbad": (23.7957, 86.4304, "Jharkhand"),
    "amritsar": (31.6340, 74.8723, "Punjab"),
    "navi mumbai": (19.0330, 73.0297, "Maharashtra"),
    "allahabad": (25.4358, 81.8463, "Uttar Pradesh"),
    "prayagraj": (25.4358, 81.8463, "Uttar Pradesh"),
    "ranchi": (23.3441, 85.3096, "Jharkhand"),
    "howrah": (22.5958, 88.2636, "West Bengal"),
    "coimbatore": (11.0168, 76.9558, "Tamil Nadu"),
    "jabalpur": (23.1815, 79.9864, "Madhya Pradesh"),
    "gwalior": (26.2183, 78.1828, "Madhya Pradesh"),
    "vijayawada": (16.5062, 80.6480, "Andhra Pradesh"),
    "jodhpur": (26.2389, 73.0243, "Rajasthan"),
    "madurai": (9.9252, 78.1198, "Tamil Nadu"),
    "raipur": (21.2514, 81.6296, "Chhattisgarh"),
    "kota": (25.2138, 75.8648, "Rajasthan"),
    "chandigarh": (30.7333, 76.7794, "Chandigarh"),
    "guwahati": (26.1445, 91.7362, "Assam"),
    "solapur": (17.6599, 75.9064, "Maharashtra"),
    "hubli": (15.3647, 75.1240, "Karnataka"),
    "hubballi": (15.3647, 75.1240, "Karnataka"),
    "mysore": (12.2958, 76.6394, "Karnataka"),
    "mysuru": (12.2958, 76.6394, "Karnataka"),
    "tiruchirappalli": (10.7905, 78.7047, "Tamil Nadu"),
    "trichy": (10.7905, 78.7047, "Tamil Nadu"),
    "bareilly": (28.3670, 79.4304, "Uttar Pradesh"),
    "aligarh": (27.8974, 78.0880, "Uttar Pradesh"),
    "tiruppur": (11.1085, 77.3411, "Tamil Nadu"),
    "gurgaon": (28.4595, 77.0266, "Haryana"),
    "gurugram": (28.4595, 77.0266, "Haryana"),
    "noida": (28.5355, 77.3910, "Uttar Pradesh"),
    "greater noida": (28.4744, 77.5040, "Uttar Pradesh"),
    "moradabad": (28.8356, 78.7747, "Uttar Pradesh"),
    "jalandhar": (31.3260, 75.5762, "Punjab"),
    "bhubaneswar": (20.2961, 85.8245, "Odisha"),
    "salem": (11.6643, 78.1460, "Tamil Nadu"),
    "warangal": (17.9689, 79.5941, "Telangana"),
    "jalgaon": (21.0077, 75.5626, "Maharashtra"),
    "kochi": (9.9312, 76.2673, "Kerala"),
    "cochin": (9.9312, 76.2673, "Kerala"),
    "thiruvananthapuram": (8.5241, 76.9366, "Kerala"),
    "trivandrum": (8.5241, 76.9366, "Kerala"),
    "dehradun": (30.3165, 78.0322, "Uttarakhand"),
    "jamnagar": (22.4707, 70.0577, "Gujarat"),
    "ujjain": (23.1765, 75.7885, "Madhya Pradesh"),
    "haridwar": (29.9457, 78.1642, "Uttarakhand"),
    "rishikesh": (30.0869, 78.2676, "Uttarakhand"),
    "mangalore": (12.9141, 74.8560, "Karnataka"),
    "mangaluru": (12.9141, 74.8560, "Karnataka"),
    "belgaum": (15.8497, 74.4977, "Karnataka"),
    "belagavi": (15.8497, 74.4977, "Karnataka"),
    "udaipur": (24.5854, 73.7125, "Rajasthan"),
    "ajmer": (26.4499, 74.6399, "Rajasthan"),
    "mathura": (27.4924, 77.6737, "Uttar Pradesh"),
    "ayodhya": (26.7922, 82.1998, "Uttar Pradesh"),
    "shimla": (31.1048, 77.1734, "Himachal Pradesh"),
    "jammu": (32.7266, 74.8570, "Jammu & Kashmir"),
    "panaji": (15.4909, 73.8278, "Goa"),
    "goa": (15.2993, 74.1240, "Goa"),
    "puducherry": (11.9416, 79.8083, "Puducherry"),
    "pondicherry": (11.9416, 79.8083, "Puducherry"),
    "calicut": (11.2588, 75.7804, "Kerala"),
    "kozhikode": (11.2588, 75.7804, "Kerala"),
    "thrissur": (10.5276, 76.2144, "Kerala"),
    "kollam": (8.8932, 76.6141, "Kerala"),
    "gaya": (24.7914, 85.0002, "Bihar"),
    "muzaffarpur": (26.1209, 85.3647, "Bihar"),
    "bhagalpur": (25.2425, 86.9842, "Bihar"),
    "tirupati": (13.6288, 79.4192, "Andhra Pradesh"),
    "kurnool": (15.8281, 78.0373, "Andhra Pradesh"),
    "nellore": (14.4426, 79.9865, "Andhra Pradesh"),
    "anantapur": (14.6819, 77.6006, "Andhra Pradesh"),
    "guntur": (16.3067, 80.4365, "Andhra Pradesh"),
    "rohtak": (28.8955, 76.6066, "Haryana"),
    "panipat": (29.3909, 76.9635, "Haryana"),
    "karnal": (29.6857, 76.9905, "Haryana"),
    "ambala": (30.3782, 76.7767, "Haryana"),
    "hisar": (29.1492, 75.7217, "Haryana"),
    "jhansi": (25.4484, 78.5685, "Uttar Pradesh"),
    "gorakhpur": (26.7606, 83.3732, "Uttar Pradesh"),
    "saharanpur": (29.9640, 77.5460, "Uttar Pradesh"),
    "firozabad": (27.1592, 78.3957, "Uttar Pradesh"),
    "muzaffarnagar": (29.4727, 77.7085, "Uttar Pradesh"),
    "bhilai": (21.2121, 81.3733, "Chhattisgarh"),
    "bilaspur": (22.0797, 82.1409, "Chhattisgarh"),
    "cuttack": (20.4625, 85.8830, "Odisha"),
    "puri": (19.8135, 85.8312, "Odisha"),
    "rourkela": (22.2604, 84.8536, "Odisha"),
    "siliguri": (26.7271, 88.3953, "West Bengal"),
    "asansol": (23.6739, 86.9524, "West Bengal"),
    "durgapur": (23.5204, 87.3119, "West Bengal"),
    "kolhapur": (16.7050, 74.2433, "Maharashtra"),
    "sangli": (16.8524, 74.5815, "Maharashtra"),
    "amravati": (20.9320, 77.7523, "Maharashtra"),
    "nanded": (19.1383, 77.3210, "Maharashtra"),
    "akola": (20.7002, 77.0082, "Maharashtra"),
    "latur": (18.4088, 76.5604, "Maharashtra"),
    "dhule": (20.9042, 74.7749, "Maharashtra"),
    "ahmednagar": (19.0952, 74.7496, "Maharashtra"),
    "bhavnagar": (21.7645, 72.1519, "Gujarat"),
    "gandhinagar": (23.2156, 72.6369, "Gujarat"),
    "anand": (22.5645, 72.9289, "Gujarat"),
    "junagadh": (21.5222, 70.4579, "Gujarat"),
    "bikaner": (28.0229, 73.3119, "Rajasthan"),
    "alwar": (27.5530, 76.6346, "Rajasthan"),
    "bhilwara": (25.3407, 74.6313, "Rajasthan"),
    "sikar": (27.6094, 75.1398, "Rajasthan"),
    "bharatpur": (27.2152, 77.5030, "Rajasthan"),
    "pali": (25.7711, 73.3234, "Rajasthan"),
    "sri ganganagar": (29.9038, 73.8772, "Rajasthan"),
    "jamshedpur": (22.8046, 86.2029, "Jharkhand"),
    "bokaro": (23.6693, 86.1511, "Jharkhand"),
    "deoghar": (24.4826, 86.6974, "Jharkhand"),
    "hazaribagh": (23.9937, 85.3556, "Jharkhand"),
    "shillong": (25.5788, 91.8933, "Meghalaya"),
    "imphal": (24.8170, 93.9368, "Manipur"),
    "aizawl": (23.7271, 92.7176, "Mizoram"),
    "agartala": (23.8315, 91.2868, "Tripura"),
    "kohima": (25.6751, 94.1086, "Nagaland"),
    "dimapur": (25.9094, 93.7266, "Nagaland"),
    "gangtok": (27.3389, 88.6065, "Sikkim"),
    "itanagar": (27.0844, 93.6053, "Arunachal Pradesh"),
    "port blair": (11.6234, 92.7265, "Andaman and Nicobar Islands"),
    "silchar": (24.8333, 92.7789, "Assam"),
    "dibrugarh": (27.4728, 94.9120, "Assam"),
    "jorhat": (26.7509, 94.2037, "Assam"),
    "tezpur": (26.6528, 92.7926, "Assam"),
    "bathinda": (30.2110, 74.9455, "Punjab"),
    "pathankot": (32.2684, 75.6530, "Punjab"),
    "hoshiarpur": (31.5273, 75.9149, "Punjab"),
    "patiala": (30.3398, 76.3869, "Punjab"),
    "dharamshala": (32.2190, 76.3234, "Himachal Pradesh"),
    "manali": (32.2432, 77.1892, "Himachal Pradesh"),
    "kullu": (31.9579, 77.1095, "Himachal Pradesh"),
    "mandi": (31.7087, 76.9320, "Himachal Pradesh"),
    "solan": (30.9045, 77.0967, "Himachal Pradesh"),
    "haldwani": (29.2183, 79.5130, "Uttarakhand"),
    "roorkee": (29.8543, 77.8880, "Uttarakhand"),
    "nainital": (29.3919, 79.4542, "Uttarakhand"),
    "almora": (29.5971, 79.6591, "Uttarakhand"),
}


def _geocode_city(city: str) -> tuple:
    """Convert Indian city name to (latitude, longitude) with robust multi-tier fallback.
    
    1. Fast offline local dictionary of Indian cities (0ms, zero network dependency)
    2. Open-Meteo Geocoding API (filtered strictly to India)
    3. Nominatim with 10s timeout and country_codes='in'
    """
    clean_name = city.strip().lower()

    # Tier 1: Local cache of Indian cities
    if clean_name in MAJOR_CITIES:
        data = MAJOR_CITIES[clean_name]
        return (data[0], data[1])

    # Check partial match (e.g. "jaipur, rajasthan" -> "jaipur")
    primary_token = clean_name.split(",")[0].strip()
    if primary_token in MAJOR_CITIES:
        data = MAJOR_CITIES[primary_token]
        return (data[0], data[1])

    # Tier 2: Open-Meteo Geocoding API (filtered strictly to India)
    try:
        resp = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": primary_token, "count": 15, "language": "en", "format": "json"},
            timeout=6.0,
        )
        if resp.status_code == 200:
            results = resp.json().get("results") or []
            for item in results:
                if item.get("country_code", "").upper() == "IN" or "india" in item.get("country", "").lower():
                    return float(item["latitude"]), float(item["longitude"])
    except Exception:
        pass

    # Tier 3: Nominatim restricted to India (country_codes="in")
    try:
        geolocator = Nominatim(user_agent="jyotish-vedic-chart-v2", timeout=10)
        location = geolocator.geocode(f"{primary_token}, India", country_codes="in")
        if location:
            return location.latitude, location.longitude
    except Exception:
        pass

    raise ValueError(
        f"Could not find coordinates for '{city}' in India. Please check the spelling or select from the dropdown."
    )


def search_cities(query: str, limit: int = 8) -> list:
    """Search Indian cities for autocomplete suggestions."""
    q = query.strip().lower()
    if not q:
        return []

    # Clean query in case user typed e.g. "Jaipur, Rajasthan"
    q_name = q.split(",")[0].strip()
    if not q_name:
        q_name = q

    results = []
    seen = set()

    # 1. Search local Indian dictionary first (prefix matches prioritized over contains)
    prefix_matches = []
    contains_matches = []

    for city_key, data in MAJOR_CITIES.items():
        lat, lon = data[0], data[1]
        state = data[2] if len(data) > 2 else ""
        key = (round(lat, 2), round(lon, 2))

        formatted_name = city_key.title()
        display_parts = [formatted_name]
        if state and state.lower() != city_key:
            display_parts.append(state)
        display_parts.append("India")
        display = ", ".join(display_parts)

        entry = {
            "name": formatted_name,
            "display": display,
            "latitude": lat,
            "longitude": lon,
        }

        if city_key.startswith(q_name):
            if key not in seen:
                seen.add(key)
                prefix_matches.append(entry)
        elif q_name in city_key:
            if key not in seen:
                seen.add(key)
                contains_matches.append(entry)

    for entry in prefix_matches + contains_matches:
        results.append(entry)
        if len(results) >= limit:
            return results

    # 2. If fewer than limit, query Open-Meteo strictly filtered to India (country_code == 'IN')
    if len(results) < limit:
        try:
            resp = httpx.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": q_name, "count": 25, "language": "en", "format": "json"},
                timeout=4.0,
            )
            if resp.status_code == 200:
                items = resp.json().get("results", [])
                for item in items:
                    c_code = item.get("country_code", "").upper()
                    c_country = item.get("country", "").lower()
                    if c_code != "IN" and "india" not in c_country:
                        continue

                    c_name = item.get("name", "")
                    admin1 = item.get("admin1", "")
                    parts = [c_name]
                    if admin1 and admin1.lower() != c_name.lower():
                        parts.append(admin1)
                    parts.append("India")
                    display = ", ".join(parts)
                    lat = float(item["latitude"])
                    lon = float(item["longitude"])
                    key = (round(lat, 2), round(lon, 2))
                    if key not in seen:
                        seen.add(key)
                        results.append({
                            "name": c_name,
                            "display": display,
                            "latitude": lat,
                            "longitude": lon,
                        })
                        if len(results) >= limit:
                            break
        except Exception:
            pass

    return results


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
            "vedic_name": p.get("vedic_name", p["name"]),
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
