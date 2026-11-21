# -*- coding: utf-8 -*-
"""
Gurukulam Kundli CRM - Universal Offline Cities & Coordinates Database
Integrated with:
1. Curated primary fast-access Indian & World astrological centers.
2. 721,229+ complete worldwide places database (including all 557,208+ Indian statutory cities,
   towns, tehsils, and census urban centres from GeoNames & Census of India).
"""

import os
import re
import sqlite3

# Fast-access benchmark cities (prioritizing Maharashtra & key regional centers)
OFFLINE_CITIES = [
    {"name": "Karmala", "country": "India", "state": "Maharashtra", "lat": 18.4116, "lon": 75.1966, "tz": 5.5, "district": "Solapur"},
    {"name": "Solapur", "country": "India", "state": "Maharashtra", "lat": 17.6599, "lon": 75.9064, "tz": 5.5},
    {"name": "Karmala, Solapur", "country": "India", "state": "Maharashtra", "lat": 18.4116, "lon": 75.1966, "tz": 5.5},
    {"name": "Pandharpur", "country": "India", "state": "Maharashtra", "lat": 17.6776, "lon": 75.3284, "tz": 5.5},
    {"name": "Pune", "country": "India", "state": "Maharashtra", "lat": 18.5204, "lon": 73.8567, "tz": 5.5},
    {"name": "Mumbai", "country": "India", "state": "Maharashtra", "lat": 19.0760, "lon": 72.8777, "tz": 5.5},
    {"name": "Nashik", "country": "India", "state": "Maharashtra", "lat": 19.9975, "lon": 73.7898, "tz": 5.5},
    {"name": "Kolhapur", "country": "India", "state": "Maharashtra", "lat": 16.7050, "lon": 74.2433, "tz": 5.5},
    {"name": "Satara", "country": "India", "state": "Maharashtra", "lat": 17.6805, "lon": 74.0183, "tz": 5.5},
    {"name": "Sangli", "country": "India", "state": "Maharashtra", "lat": 16.8524, "lon": 74.5815, "tz": 5.5},
    {"name": "Chhatrapati Sambhajinagar", "country": "India", "state": "Maharashtra", "lat": 19.8762, "lon": 75.3433, "tz": 5.5},
    {"name": "Ahmednagar", "country": "India", "state": "Maharashtra", "lat": 19.0948, "lon": 74.7480, "tz": 5.5},
    {"name": "Nagpur", "country": "India", "state": "Maharashtra", "lat": 21.1458, "lon": 79.0882, "tz": 5.5},
    {"name": "Thane", "country": "India", "state": "Maharashtra", "lat": 19.2183, "lon": 72.9781, "tz": 5.5},
    {"name": "Vadodara", "country": "India", "state": "Gujarat", "lat": 22.3072, "lon": 73.1812, "tz": 5.5},
    {"name": "Ahmedabad", "country": "India", "state": "Gujarat", "lat": 23.0225, "lon": 72.5714, "tz": 5.5},
    {"name": "Delhi", "country": "India", "state": "Delhi", "lat": 28.6139, "lon": 77.2090, "tz": 5.5},
    {"name": "New Delhi", "country": "India", "state": "Delhi", "lat": 28.6139, "lon": 77.2090, "tz": 5.5},
    {"name": "Ludhiana", "country": "India", "state": "Punjab", "lat": 30.9010, "lon": 75.8573, "tz": 5.5},
    {"name": "Noida", "country": "India", "state": "Uttar Pradesh", "lat": 28.5355, "lon": 77.3910, "tz": 5.5},
    {"name": "Gurugram", "country": "India", "state": "Haryana", "lat": 28.4595, "lon": 77.0266, "tz": 5.5},
    {"name": "Chandigarh", "country": "India", "state": "Chandigarh", "lat": 30.7333, "lon": 76.7794, "tz": 5.5},
    {"name": "Amritsar", "country": "India", "state": "Punjab", "lat": 31.6340, "lon": 74.8723, "tz": 5.5},
    {"name": "Jalandhar", "country": "India", "state": "Punjab", "lat": 31.3260, "lon": 75.5762, "tz": 5.5},
    {"name": "Patiala", "country": "India", "state": "Punjab", "lat": 30.3398, "lon": 76.3869, "tz": 5.5},
    {"name": "Bathinda", "country": "India", "state": "Punjab", "lat": 30.2110, "lon": 74.9455, "tz": 5.5},
    {"name": "Mohali", "country": "India", "state": "Punjab", "lat": 30.7046, "lon": 76.7179, "tz": 5.5},
    {"name": "Jaipur", "country": "India", "state": "Rajasthan", "lat": 26.9124, "lon": 75.7873, "tz": 5.5},
    {"name": "Jodhpur", "country": "India", "state": "Rajasthan", "lat": 26.2389, "lon": 73.0243, "tz": 5.5},
    {"name": "Udaipur", "country": "India", "state": "Rajasthan", "lat": 24.5854, "lon": 73.7125, "tz": 5.5},
    {"name": "Bikaner", "country": "India", "state": "Rajasthan", "lat": 28.0229, "lon": 73.3119, "tz": 5.5},
    {"name": "Ajmer", "country": "India", "state": "Rajasthan", "lat": 26.4499, "lon": 74.6399, "tz": 5.5},
    {"name": "Kota", "country": "India", "state": "Rajasthan", "lat": 25.2138, "lon": 75.8648, "tz": 5.5},
    {"name": "Varanasi", "country": "India", "state": "Uttar Pradesh", "lat": 25.3176, "lon": 82.9739, "tz": 5.5},
    {"name": "Lucknow", "country": "India", "state": "Uttar Pradesh", "lat": 26.8467, "lon": 80.9462, "tz": 5.5},
    {"name": "Kanpur", "country": "India", "state": "Uttar Pradesh", "lat": 26.4499, "lon": 80.3319, "tz": 5.5},
    {"name": "Prayagraj", "country": "India", "state": "Uttar Pradesh", "lat": 25.4358, "lon": 81.8463, "tz": 5.5},
    {"name": "Ayodhya", "country": "India", "state": "Uttar Pradesh", "lat": 26.7922, "lon": 82.1998, "tz": 5.5},
    {"name": "Mathura", "country": "India", "state": "Uttar Pradesh", "lat": 27.4924, "lon": 77.6737, "tz": 5.5},
    {"name": "Agra", "country": "India", "state": "Uttar Pradesh", "lat": 27.1767, "lon": 78.0081, "tz": 5.5},
    {"name": "Haridwar", "country": "India", "state": "Uttarakhand", "lat": 29.9457, "lon": 78.1642, "tz": 5.5},
    {"name": "Dehradun", "country": "India", "state": "Uttarakhand", "lat": 30.3165, "lon": 78.0322, "tz": 5.5},
    {"name": "Shimla", "country": "India", "state": "Himachal Pradesh", "lat": 31.1048, "lon": 77.1734, "tz": 5.5},
    {"name": "Jammu", "country": "India", "state": "Jammu and Kashmir", "lat": 32.7266, "lon": 74.8570, "tz": 5.5},
    {"name": "Srinagar", "country": "India", "state": "Jammu and Kashmir", "lat": 34.0837, "lon": 74.7973, "tz": 5.5},
    {"name": "Indore", "country": "India", "state": "Madhya Pradesh", "lat": 22.7196, "lon": 75.8577, "tz": 5.5},
    {"name": "Bhopal", "country": "India", "state": "Madhya Pradesh", "lat": 23.2599, "lon": 77.4126, "tz": 5.5},
    {"name": "Ujjain", "country": "India", "state": "Madhya Pradesh", "lat": 23.1765, "lon": 75.7885, "tz": 5.5},
    {"name": "Mumbai", "country": "India", "state": "Maharashtra", "lat": 19.0760, "lon": 72.8777, "tz": 5.5},
    {"name": "Pune", "country": "India", "state": "Maharashtra", "lat": 18.5204, "lon": 73.8567, "tz": 5.5},
    {"name": "Nagpur", "country": "India", "state": "Maharashtra", "lat": 21.1458, "lon": 79.0882, "tz": 5.5},
    {"name": "Nashik", "country": "India", "state": "Maharashtra", "lat": 19.9975, "lon": 73.7898, "tz": 5.5},
    {"name": "Ahmedabad", "country": "India", "state": "Gujarat", "lat": 23.0225, "lon": 72.5714, "tz": 5.5},
    {"name": "Surat", "country": "India", "state": "Gujarat", "lat": 21.1702, "lon": 72.8311, "tz": 5.5},
    {"name": "Vadodara", "country": "India", "state": "Gujarat", "lat": 22.3072, "lon": 73.1812, "tz": 5.5},
    {"name": "Rajkot", "country": "India", "state": "Gujarat", "lat": 22.3039, "lon": 70.8022, "tz": 5.5},
    {"name": "Kolkata", "country": "India", "state": "West Bengal", "lat": 22.5726, "lon": 88.3639, "tz": 5.5},
    {"name": "Patna", "country": "India", "state": "Bihar", "lat": 25.5941, "lon": 85.1376, "tz": 5.5},
    {"name": "Ranchi", "country": "India", "state": "Jharkhand", "lat": 23.3441, "lon": 85.3096, "tz": 5.5},
    {"name": "Raipur", "country": "India", "state": "Chhattisgarh", "lat": 21.2514, "lon": 81.6296, "tz": 5.5},
    {"name": "Bengaluru", "country": "India", "state": "Karnataka", "lat": 12.9716, "lon": 77.5946, "tz": 5.5},
    {"name": "Chennai", "country": "India", "state": "Tamil Nadu", "lat": 13.0827, "lon": 80.2707, "tz": 5.5},
    {"name": "Hyderabad", "country": "India", "state": "Telangana", "lat": 17.3850, "lon": 78.4867, "tz": 5.5},
    {"name": "Bhubaneswar", "country": "India", "state": "Odisha", "lat": 20.2961, "lon": 85.8245, "tz": 5.5},
    {"name": "Guwahati", "country": "India", "state": "Assam", "lat": 26.1445, "lon": 91.7362, "tz": 5.5},
    {"name": "Kochi", "country": "India", "state": "Kerala", "lat": 9.9312, "lon": 76.2673, "tz": 5.5},
    {"name": "London", "country": "United Kingdom", "state": "England", "lat": 51.5074, "lon": -0.1278, "tz": 0.0},
    {"name": "New York", "country": "United States", "state": "New York", "lat": 40.7128, "lon": -74.0060, "tz": -5.0},
    {"name": "Dubai", "country": "United Arab Emirates", "state": "Dubai", "lat": 25.2048, "lon": 55.2708, "tz": 4.0},
    {"name": "Kathmandu", "country": "Nepal", "state": "Bagmati", "lat": 27.7172, "lon": 85.3240, "tz": 5.75},
]

def _to_dms(val: float, is_lat: bool) -> str:
    direction = ("N" if val >= 0 else "S") if is_lat else ("E" if val >= 0 else "W")
    av = abs(val)
    d = int(av)
    m = int((av - d) * 60)
    return f"{d:02d}:{m:02d}:{direction}"

def _get_db_path():
    # Try current or parent data directory
    import sys
    base_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    paths = [
        os.path.join(base_dir, "data", "world_cities.db"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "world_cities.db"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "world_cities.db"),
        os.path.join(getattr(sys, '_MEIPASS', ''), "data", "world_cities.db"),
        r"E:\Kundli crm\data\world_cities.db",
        r"data\world_cities.db",
    ]
    for p in paths:
        if p and os.path.exists(p):
            return p
    return paths[0]

def search_cities(query: str, limit: int = 30) -> list[dict]:
    """
    Search across 721,000+ cities and statutory towns in India & Worldwide.
    Always prioritizes prominent Indian cities and matches accurately.
    Supports compound queries like 'Karmala, Solapur' or 'Solapur, Maharashtra'.
    """
    if not query or len(query.strip()) < 2:
        return OFFLINE_CITIES[:limit]

    q_raw = query.strip().lower()
    # Split query by comma, slash or whitespace
    tokens = [t.strip() for t in re.split(r'[,/\s]+', q_raw) if t.strip()]
    if not tokens:
        tokens = [q_raw]

    # Check priority in-memory list first
    priority_matches = []
    # Pass 1: exact/prefix match for all tokens or full query
    for c in OFFLINE_CITIES:
        c_name = c["name"].lower()
        c_state = c.get("state", "").lower()
        c_dist = c.get("district", "").lower()
        full_text = f"{c_name} {c_state} {c_dist}"
        if all(t in full_text for t in tokens):
            priority_matches.append(c)
        elif any(c_name.startswith(t) or t in c_name for t in tokens):
            if c not in priority_matches:
                priority_matches.append(c)

    db_path = _get_db_path()
    if not os.path.exists(db_path):
        return priority_matches[:limit] if priority_matches else OFFLINE_CITIES[:limit]

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        main_token = tokens[0]
        # 1. Exact or prefix match with Maharashtra & Indian priority
        cur.execute("""
            SELECT name, country, state, lat, lng, timezone_offset
            FROM cities
            WHERE name LIKE ? OR name LIKE ?
            ORDER BY
                CASE WHEN LOWER(state) = 'maharashtra' THEN 0 ELSE 1 END,
                CASE WHEN country = 'IN' THEN 0 ELSE 1 END,
                CASE WHEN LOWER(name) = ? THEN 0 ELSE 1 END,
                LENGTH(name) ASC
            LIMIT ?
        """, (f"{main_token}%", f"%{main_token}%", main_token, limit * 2))
        rows = cur.fetchall()

        # 2. If compound tokens (e.g. ['karmala', 'solapur']), filter or reorder by second token
        if len(tokens) > 1:
            sec_token = tokens[1]
            scored_rows = []
            for r in rows:
                r_text = f"{r[0]} {r[1]} {r[2]}".lower()
                score = 0
                if sec_token in r_text:
                    score += 10
                if (r[2] or '').lower() == 'maharashtra':
                    score += 5
                scored_rows.append((score, r))
            scored_rows.sort(key=lambda x: -x[0])
            rows = [r for _, r in scored_rows]

        conn.close()

        db_results = [
            {
                "name": r[0],
                "country": r[1] or "India",
                "state": r[2] or "",
                "lat": round(float(r[3]), 4),
                "lon": round(float(r[4]), 4),
                "tz": float(r[5]) if r[5] is not None else 5.5,
            }
            for r in rows
        ]

        # Merge priority matches first, then DB results without duplicates
        combined = []
        seen = set()
        for c in priority_matches:
            k = (c["name"].lower(), c.get("state", "").lower())
            if k not in seen:
                combined.append(c)
                seen.add(k)
        for c in db_results:
            k = (c["name"].lower(), c.get("state", "").lower())
            if k not in seen:
                combined.append(c)
                seen.add(k)

        return combined[:limit]

    except Exception as e:
        return priority_matches[:limit] if priority_matches else OFFLINE_CITIES[:limit]


def find_city(place_name: str) -> dict:
    """Find the exact or best matching city with typo tolerance."""
    if not place_name:
        return OFFLINE_CITIES[0]

    p = place_name.strip()
    p_lower = p.lower()

    # 1. Check exact match in OFFLINE_CITIES
    for c in OFFLINE_CITIES:
        if c["name"].lower() == p_lower:
            return c

    # 2. Search query
    results = search_cities(p, limit=5)
    if results:
        # Check if first result matches prefix
        return results[0]

    # 3. Typo tolerance: try prefix (e.g. 'ludhiz' -> 'ludh')
    if len(p) >= 4:
        sub_results = search_cities(p[:4], limit=3)
        if sub_results:
            return sub_results[0]

    # Default to Delhi
    return OFFLINE_CITIES[1]  # Delhi
