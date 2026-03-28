from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from datetime import datetime, timedelta
import random
import string
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# ========================================
# 50+ COUNTRIES WORLDWIDE (Including Uganda)
# ========================================

cities = [
    # Africa (including Uganda)
    "Lagos (LOS)", "Abuja (ABV)", "Kampala (EBB)", "Entebbe (EBB)", "Nairobi (NBO)", 
    "Cape Town (CPT)", "Johannesburg (JNB)", "Accra (ACC)", "Casablanca (CMN)", "Cairo (CAI)",
    "Addis Ababa (ADD)", "Dar es Salaam (DAR)", "Kigali (KGL)", "Mauritius (MRU)", "Marrakech (RAK)",
    
    # Middle East
    "Dubai (DXB)", "Abu Dhabi (AUH)", "Doha (DOH)", "Riyadh (RUH)", "Jeddah (JED)", 
    "Kuwait (KWI)", "Muscat (MCT)", "Bahrain (BAH)", "Amman (AMM)",
    
    # Europe
    "London (LHR)", "Paris (CDG)", "Frankfurt (FRA)", "Amsterdam (AMS)", "Rome (FCO)",
    "Milan (MXP)", "Barcelona (BCN)", "Madrid (MAD)", "Zurich (ZRH)", "Geneva (GVA)",
    "Brussels (BRU)", "Vienna (VIE)", "Prague (PRG)", "Lisbon (LIS)", "Dublin (DUB)",
    "Manchester (MAN)", "Edinburgh (EDI)", "Berlin (BER)", "Munich (MUC)", "Istanbul (IST)",
    
    # Asia
    "Singapore (SIN)", "Bangkok (BKK)", "Tokyo (HND)", "Seoul (ICN)", "Hong Kong (HKG)",
    "Shanghai (PVG)", "Beijing (PEK)", "Kuala Lumpur (KUL)", "Jakarta (CGK)", "Mumbai (BOM)",
    "Delhi (DEL)", "Chennai (MAA)", "Bangalore (BLR)", "Ho Chi Minh (SGN)", "Manila (MNL)",
    
    # North America
    "New York (JFK)", "Los Angeles (LAX)", "Chicago (ORD)", "Miami (MIA)", "Toronto (YYZ)",
    "Vancouver (YVR)", "Montreal (YUL)", "Atlanta (ATL)", "San Francisco (SFO)", "Boston (BOS)",
    "Washington (IAD)", "Dallas (DFW)", "Houston (IAH)", "Seattle (SEA)", "Las Vegas (LAS)",
    
    # South America
    "Sao Paulo (GRU)", "Rio de Janeiro (GIG)", "Buenos Aires (EZE)", "Bogota (BOG)", "Lima (LIM)",
    "Santiago (SCL)", "Montevideo (MVD)", "Caracas (CCS)", "Quito (UIO)", "La Paz (LPB)",
    
    # Oceania
    "Sydney (SYD)", "Melbourne (MEL)", "Auckland (AKL)", "Brisbane (BNE)", "Perth (PER)",
    "Christchurch (CHC)", "Wellington (WLG)"
]

# Premium global airlines
airlines = [
    {"name": "Emirates", "code": "EK"},
    {"name": "Qatar Airways", "code": "QR"},
    {"name": "Etihad Airways", "code": "EY"},
    {"name": "British Airways", "code": "BA"},
    {"name": "Virgin Atlantic", "code": "VS"},
    {"name": "Air France", "code": "AF"},
    {"name": "Lufthansa", "code": "LH"},
    {"name": "Turkish Airlines", "code": "TK"},
    {"name": "Singapore Airlines", "code": "SQ"},
    {"name": "Cathay Pacific", "code": "CX"},
    {"name": "Kenya Airways", "code": "KQ"},
    {"name": "RwandAir", "code": "WB"},
    {"name": "Ethiopian Airlines", "code": "ET"},
    {"name": "South African Airways", "code": "SA"},
    {"name": "Uganda Airlines", "code": "UR"}
]

cabin_multipliers = {"economy": 1.0, "business": 3.2, "first": 5.5}

# Base fare calculator
def calculate_base_fare(from_city, to_city):
    from_code = from_city.split("(")[-1].replace(")", "").strip()
    to_code = to_city.split("(")[-1].replace(")", "").strip()
    
    fare_map = {
        # Uganda routes
        ("EBB", "NBO"): 180000, ("EBB", "DXB"): 650000, ("EBB", "LHR"): 850000,
        ("EBB", "JNB"): 520000, ("EBB", "ADD"): 250000, ("EBB", "KGL"): 150000,
        ("LOS", "EBB"): 320000, ("NBO", "EBB"): 180000, ("JNB", "EBB"): 520000,
        
        # Africa routes
        ("LOS", "JNB"): 450000, ("LOS", "CPT"): 500000, ("LOS", "NBO"): 380000,
        ("LOS", "DXB"): 650000, ("LOS", "LHR"): 850000, ("LOS", "JFK"): 1200000,
        
        # Middle East to Europe/Asia
        ("DXB", "LHR"): 280000, ("DXB", "JFK"): 850000, ("DXB", "SIN"): 280000,
        ("DXB", "BKK"): 250000, ("DXB", "NBO"): 220000, ("DXB", "EBB"): 650000,
        
        # European connections
        ("LHR", "JFK"): 450000, ("LHR", "DXB"): 280000, ("LHR", "CDG"): 120000,
        ("CDG", "DXB"): 320000, ("CDG", "JFK"): 480000,
        
        # Default
        "default": 400000
    }
    
    key = (from_code, to_code)
    if key in fare_map:
        return fare_map[key]
    return fare_map["default"]

# Generate flights for 180 days (6 months)
flights = {}
flight_id = 1

# Generate for popular routes including Uganda
popular_routes = [
    # Uganda connections
    ("Kampala (EBB)", "Dubai (DXB)"), ("Kampala (EBB)", "London (LHR)"),
    ("Kampala (EBB)", "Nairobi (NBO)"), ("Kampala (EBB)", "Johannesburg (JNB)"),
    ("Kampala (EBB)", "Addis Ababa (ADD)"), ("Kampala (EBB)", "Kigali (KGL)"),
    ("Lagos (LOS)", "Kampala (EBB)"), ("Nairobi (NBO)", "Kampala (EBB)"),
    
    # Major international routes
    ("Lagos (LOS)", "Dubai (DXB)"), ("Lagos (LOS)", "London (LHR)"),
    ("Lagos (LOS)", "New York (JFK)"), ("Lagos (LOS)", "Johannesburg (JNB)"),
    ("Dubai (DXB)", "London (LHR)"), ("Dubai (DXB)", "New York (JFK)"),
    ("Dubai (DXB)", "Singapore (SIN)"), ("Dubai (DXB)", "Bangkok (BKK)"),
    ("London (LHR)", "New York (JFK)"), ("London (LHR)", "Paris (CDG)"),
    ("Nairobi (NBO)", "Dubai (DXB)"), ("Nairobi (NBO)", "London (LHR)"),
    ("Johannesburg (JNB)", "Dubai (DXB)"), ("Johannesburg (JNB)", "London (LHR)"),
    ("Cape Town (CPT)", "Dubai (DXB)"), ("Cape Town (CPT)", "London (LHR)"),
    ("New York (JFK)", "London (LHR)"), ("New York (JFK)", "Dubai (DXB)"),
]

for from_city, to_city in popular_routes:
    base_fare = calculate_base_fare(from_city, to_city)
    
    for airline in airlines:
        economy_price = int(base_fare * random.uniform(0.9, 1.2))
        business_price = int(economy_price * cabin_multipliers["business"])
        first_price = int(economy_price * cabin_multipliers["first"])
        
        # Generate for 180 days (6 months)
        for day_offset in range(1, 181):
            flight_date = (datetime.now() + timedelta(days=day_offset)).strftime('%Y-%m-%d')
            hour = random.choice([0, 2, 6, 8, 10, 12, 14, 16, 18, 20, 22])
            minute = random.choice([0, 15, 30, 45])
            duration_h = random.randint(2, 14)
            duration_m = random.choice([0, 15, 30, 45])
            
            key = f"{from_city}_{to_city}_{airline['code']}_{flight_date}"
            flights[key] = {
                'id': flight_id,
                'flight_number': f"{airline['code']}{random.randint(100, 999)}",
                'airline': airline['name'],
                'from_city': from_city,
                'to_city': to_city,
                'departure_time': f"{hour:02d}:{minute:02d}",
                'arrival_time': f"{(hour + duration_h) % 24:02d}:{duration_m:02d}",
                'duration': f"{duration_h}h {duration_m}m",
                'date': flight_date,
                'economy_price': economy_price,
                'business_price': business_price,
                'first_price': first_price,
                'price': economy_price
            }
            flight_id += 1
            if flight_id > 8000:
                break
        if flight_id > 8000:
            break
    if flight_id > 8000:
        break

flights_list = list(flights.values())
bookings = []

# ========================================
# ROUTES
# ========================================

@app.route('/')
def home():
    return send_file('../frontend/index.html')

@app.route('/api/cities')
def get_cities():
    return jsonify(cities)

@app.route('/api/flights/search', methods=['POST'])
def search_flights():
    data = request.json
    from_city = data.get('from')
    to_city = data.get('to')
    date = data.get('date')
    cabin = data.get('cabin_class', 'economy')
    trip_type = data.get('trip_type', 'oneway')
    return_date = data.get('return_date')
    
    results = []
    for f in flights_list:
        if f['from_city'] == from_city and f['to_city'] == to_city and f['date'] == date:
            copy = f.copy()
            if cabin == 'economy':
                copy['price'] = copy['economy_price']
            elif cabin == 'business':
                copy['price'] = copy['business_price']
            else:
                copy['price'] = copy['first_price']
            results.append(copy)
    
    # If return trip, also search for return flights
    if trip_type == 'round' and return_date:
        return_results = []
        for f in flights_list:
            if f['to_city'] == from_city and f['from_city'] == to_city and f['date'] == return_date:
                copy = f.copy()
                if cabin == 'economy':
                    copy['price'] = copy['economy_price']
                elif cabin == 'business':
                    copy['price'] = copy['business_price']
                else:
                    copy['price'] = copy['first_price']
                return_results.append(copy)
        return jsonify({'outbound': results, 'return': return_results})
    
    return jsonify({'outbound': results, 'return': []})

@app.route('/api/flights/multi-city', methods=['POST'])
def multi_city_search():
    data = request.json
    segments = data.get('segments', [])
    cabin = data.get('cabin_class', 'economy')
    
    results = []
    for segment in segments:
        from_city = segment.get('from')
        to_city = segment.get('to')
        date = segment.get('date')
        
        segment_results = []
        for f in flights_list:
            if f['from_city'] == from_city and f['to_city'] == to_city and f['date'] == date:
                copy = f.copy()
                if cabin == 'economy':
                    copy['price'] = copy['economy_price']
                elif cabin == 'business':
                    copy['price'] = copy['business_price']
                else:
                    copy['price'] = copy['first_price']
                segment_results.append(copy)
        results.append(segment_results)
    
    return jsonify(results)

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.json
    ref = f"DH-{datetime.now().strftime('%Y%m')}-{random.randint(1000, 9999)}"
    
    booking = {
        'id': len(bookings) + 1,
        'booking_reference': ref,
        'flights': data.get('flights', []),
        'passenger_name': data.get('passenger_name'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'total_amount': data.get('total_amount'),
        'trip_type': data.get('trip_type', 'oneway'),
        'status': 'confirmed',
        'booking_date': datetime.now().isoformat()
    }
    bookings.append(booking)
    
    return jsonify({'message': 'Booking confirmed', 'booking_reference': ref})

@app.route('/api/bookings/my-bookings', methods=['GET'])
def get_bookings():
    return jsonify(bookings)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print("\n" + "="*60)
    print("✨ DOUBLE H CONCIERGE - GLOBAL LUXURY TRAVEL")
    print("="*60)
    print(f"🌍 Cities: {len(cities)} worldwide (including Uganda!)")
    print(f"✈️ Routes: {len(popular_routes)} major routes")
    print(f"💎 Airlines: {len(airlines)} premium carriers")
    print(f"📅 Flights available: {len(flights_list)} (next 180 days)")
    print(f"\n🇺🇬 Uganda included: Kampala (EBB), Entebbe (EBB)")
    print("\n🌐 Server running - Ready for search!")
    app.run(host='0.0.0.0', port=port)
