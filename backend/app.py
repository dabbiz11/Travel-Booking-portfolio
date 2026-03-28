from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# ========================================
# COMPLETE CITIES LIST
# ========================================

cities = [
    # Africa
    "Lagos (LOS)", "Abuja (ABV)", "Kampala (EBB)", "Entebbe (EBB)", "Nairobi (NBO)", 
    "Cape Town (CPT)", "Johannesburg (JNB)", "Accra (ACC)", "Casablanca (CMN)", "Cairo (CAI)",
    "Addis Ababa (ADD)", "Dar es Salaam (DAR)", "Kigali (KGL)", "Mauritius (MRU)",
    
    # Middle East
    "Dubai (DXB)", "Abu Dhabi (AUH)", "Doha (DOH)", "Riyadh (RUH)", "Jeddah (JED)", 
    "Kuwait (KWI)", "Muscat (MCT)", "Bahrain (BAH)", "Amman (AMM)",
    
    # Europe
    "London (LHR)", "Paris (CDG)", "Frankfurt (FRA)", "Amsterdam (AMS)", "Rome (FCO)",
    "Milan (MXP)", "Barcelona (BCN)", "Madrid (MAD)", "Zurich (ZRH)", "Vienna (VIE)",
    "Manchester (MAN)", "Berlin (BER)", "Munich (MUC)", "Istanbul (IST)",
    
    # Asia
    "Singapore (SIN)", "Bangkok (BKK)", "Tokyo (HND)", "Seoul (ICN)", "Hong Kong (HKG)",
    "Kuala Lumpur (KUL)", "Mumbai (BOM)", "Delhi (DEL)", "Ho Chi Minh (SGN)",
    
    # North America
    "New York (JFK)", "Los Angeles (LAX)", "Chicago (ORD)", "Miami (MIA)", "Toronto (YYZ)",
    "San Francisco (SFO)", "Boston (BOS)",
    
    # South America
    "Sao Paulo (GRU)", "Rio de Janeiro (GIG)", "Buenos Aires (EZE)", "Bogota (BOG)", "Lima (LIM)",
    
    # Oceania
    "Sydney (SYD)", "Melbourne (MEL)", "Auckland (AKL)", "Brisbane (BNE)", "Perth (PER)"
]

airlines = [
    {"name": "Emirates", "code": "EK"},
    {"name": "Qatar Airways", "code": "QR"},
    {"name": "British Airways", "code": "BA"},
    {"name": "Turkish Airlines", "code": "TK"},
    {"name": "Uganda Airlines", "code": "UR"},
    {"name": "Kenya Airways", "code": "KQ"},
    {"name": "Ethiopian Airlines", "code": "ET"},
    {"name": "RwandAir", "code": "WB"},
    {"name": "South African Airways", "code": "SA"},
    {"name": "Air France", "code": "AF"},
    {"name": "Lufthansa", "code": "LH"}
]

# ========================================
# PRICE DATABASE - ALL ROUTES
# ========================================

def get_route_price(from_city, to_city):
    """Get realistic price for any route"""
    
    # Extract city codes
    from_code = from_city.split("(")[-1].replace(")", "").strip() if "(" in from_city else from_city[:3]
    to_code = to_city.split("(")[-1].replace(")", "").strip() if "(" in to_city else to_city[:3]
    
    # Price matrix (in Naira)
    prices = {
        # Uganda Routes
        ("EBB", "DXB"): 320000, ("EBB", "LHR"): 480000, ("EBB", "NBO"): 95000,
        ("EBB", "JNB"): 280000, ("EBB", "ADD"): 120000, ("EBB", "KGL"): 80000,
        ("EBB", "IST"): 380000, ("EBB", "DOH"): 310000,
        
        # Nigeria Routes
        ("LOS", "DXB"): 380000, ("LOS", "LHR"): 520000, ("LOS", "JFK"): 950000,
        ("LOS", "JNB"): 310000, ("LOS", "NBO"): 280000, ("LOS", "ACC"): 95000,
        ("LOS", "CPT"): 420000, ("LOS", "EBB"): 250000,
        ("ABV", "DXB"): 390000, ("ABV", "LHR"): 530000,
        
        # Kenya Routes
        ("NBO", "DXB"): 270000, ("NBO", "LHR"): 420000, ("NBO", "JNB"): 220000,
        ("NBO", "EBB"): 95000, ("NBO", "KGL"): 85000,
        
        # South Africa Routes
        ("JNB", "DXB"): 350000, ("JNB", "LHR"): 470000, ("JNB", "CPT"): 150000,
        ("CPT", "DXB"): 380000, ("CPT", "LHR"): 520000,
        
        # Middle East Routes
        ("DXB", "LHR"): 220000, ("DXB", "CDG"): 210000, ("DXB", "JFK"): 480000,
        ("DXB", "SIN"): 320000, ("DXB", "BKK"): 190000, ("DXB", "BOM"): 110000,
        ("DXB", "EBB"): 320000, ("DXB", "NBO"): 270000,
        
        # European Routes
        ("LHR", "JFK"): 380000, ("LHR", "CDG"): 75000, ("LHR", "DXB"): 220000,
        ("LHR", "SIN"): 520000, ("CDG", "DXB"): 210000, ("CDG", "JFK"): 390000,
        ("IST", "DXB"): 140000,
        
        # Asian Routes
        ("SIN", "BKK"): 85000, ("SIN", "DXB"): 320000, ("SIN", "LHR"): 520000,
        ("BKK", "DXB"): 190000, ("BOM", "DXB"): 110000, ("BOM", "LHR"): 380000,
    }
    
    # Try exact match
    key = (from_code, to_code)
    if key in prices:
        return prices[key]
    
    # Try reverse
    rev_key = (to_code, from_code)
    if rev_key in prices:
        return prices[rev_key]
    
    # Default price based on distance approximation
    return 400000

# Generate flights dynamically
def generate_flights_for_route(from_city, to_city, date, cabin):
    """Generate flights on demand for any route"""
    
    base_price = get_route_price(from_city, to_city)
    
    # Apply cabin multiplier
    if cabin == 'economy':
        multiplier = 1.0
    elif cabin == 'business':
        multiplier = 3.2
    else:
        multiplier = 5.5
    
    price = int(base_price * multiplier)
    
    # Seasonal adjustment
    month = int(date[5:7]) if date else 1
    if month in [12, 1, 7, 8]:
        price = int(price * 1.25)
    elif month in [4, 5, 6, 11]:
        price = int(price * 1.1)
    else:
        price = int(price * 0.95)
    
    # Generate multiple flights per route
    flights = []
    airlines_list = ["Emirates", "Qatar Airways", "British Airways", "Turkish Airlines", 
                     "Uganda Airlines", "Kenya Airways", "Ethiopian Airlines"]
    
    for i, airline in enumerate(airlines_list[:4]):  # 4 flights per route
        hour = random.choice([6, 8, 10, 12, 14, 16, 18, 20])
        minute = random.choice([0, 15, 30, 45])
        duration_h = random.randint(2, 8)
        
        flights.append({
            'id': random.randint(10000, 99999),
            'flight_number': f"{airline[:2].upper()}{random.randint(100, 999)}",
            'airline': airline,
            'from_city': from_city,
            'to_city': to_city,
            'departure_time': f"{hour:02d}:{minute:02d}",
            'arrival_time': f"{(hour + duration_h) % 24:02d}:{minute:02d}",
            'duration': f"{duration_h}h {random.choice([0,15,30,45])}m",
            'date': date,
            'price': price + random.randint(-20000, 20000) * i
        })
    
    return flights

# Store bookings
bookings = []

# ========================================
# API ENDPOINTS
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
    
    print(f"🔍 Searching: {from_city} → {to_city} on {date}")
    
    # Generate outbound flights
    outbound = generate_flights_for_route(from_city, to_city, date, cabin)
    
    # Generate return flights if round trip
    return_flights = []
    if trip_type == 'round' and return_date:
        return_flights = generate_flights_for_route(to_city, from_city, return_date, cabin)
    
    return jsonify({'outbound': outbound, 'return': return_flights})

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
        
        flights = generate_flights_for_route(from_city, to_city, date, cabin)
        results.append(flights)
    
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
    print("✨ DOUBLE H CONCIERGE - LUXURY TRAVEL SYSTEM")
    print("="*60)
    print(f"🌍 Cities available: {len(cities)} worldwide")
    print(f"✈️ Dynamic flight generation enabled")
    print(f"🇺🇬 Uganda routes: Kampala (EBB), Entebbe (EBB)")
    print("\n✅ ANY route you search will return flights!")
    print("🌐 Server running on port " + str(port))
    app.run(host='0.0.0.0', port=port)
