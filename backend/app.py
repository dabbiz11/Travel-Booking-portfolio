from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# ========================================
# COMPLETE CITIES LIST (50+ INCLUDING UGANDA)
# ========================================

cities = [
    # Africa (Including Uganda)
    "Lagos (LOS)", "Abuja (ABV)", "Kampala (EBB)", "Entebbe (EBB)", "Nairobi (NBO)", 
    "Cape Town (CPT)", "Johannesburg (JNB)", "Accra (ACC)", "Casablanca (CMN)", "Cairo (CAI)",
    "Addis Ababa (ADD)", "Dar es Salaam (DAR)", "Kigali (KGL)", "Mauritius (MRU)", "Marrakech (RAK)",
    
    # Middle East
    "Dubai (DXB)", "Abu Dhabi (AUH)", "Doha (DOH)", "Riyadh (RUH)", "Jeddah (JED)", 
    "Kuwait (KWI)", "Muscat (MCT)", "Bahrain (BAH)", "Amman (AMM)",
    
    # Europe
    "London (LHR)", "Paris (CDG)", "Frankfurt (FRA)", "Amsterdam (AMS)", "Rome (FCO)",
    "Milan (MXP)", "Barcelona (BCN)", "Madrid (MAD)", "Zurich (ZRH)", "Geneva (GVA)",
    "Vienna (VIE)", "Prague (PRG)", "Lisbon (LIS)", "Dublin (DUB)", "Manchester (MAN)",
    "Berlin (BER)", "Munich (MUC)", "Istanbul (IST)",
    
    # Asia
    "Singapore (SIN)", "Bangkok (BKK)", "Tokyo (HND)", "Seoul (ICN)", "Hong Kong (HKG)",
    "Kuala Lumpur (KUL)", "Jakarta (CGK)", "Mumbai (BOM)", "Delhi (DEL)", "Ho Chi Minh (SGN)",
    
    # North America
    "New York (JFK)", "Los Angeles (LAX)", "Chicago (ORD)", "Miami (MIA)", "Toronto (YYZ)",
    "Vancouver (YVR)", "San Francisco (SFO)", "Boston (BOS)", "Washington (IAD)",
    
    # South America
    "Sao Paulo (GRU)", "Rio de Janeiro (GIG)", "Buenos Aires (EZE)", "Bogota (BOG)", "Lima (LIM)",
    
    # Oceania
    "Sydney (SYD)", "Melbourne (MEL)", "Auckland (AKL)", "Brisbane (BNE)", "Perth (PER)"
]

# Premium Airlines
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
    {"name": "Lufthansa", "code": "LH"},
    {"name": "Singapore Airlines", "code": "SQ"}
]

# REALISTIC MARKET PRICES (in Naira)
route_prices = {
    # Uganda Routes
    ("Kampala (EBB)", "Dubai (DXB)"): 320000,
    ("Kampala (EBB)", "London (LHR)"): 480000,
    ("Kampala (EBB)", "Nairobi (NBO)"): 95000,
    ("Kampala (EBB)", "Johannesburg (JNB)"): 280000,
    ("Kampala (EBB)", "Addis Ababa (ADD)"): 120000,
    ("Kampala (EBB)", "Kigali (KGL)"): 80000,
    ("Kampala (EBB)", "Istanbul (IST)"): 380000,
    ("Kampala (EBB)", "Doha (DOH)"): 310000,
    ("Lagos (LOS)", "Kampala (EBB)"): 250000,
    ("Nairobi (NBO)", "Kampala (EBB)"): 95000,
    
    # Nigeria Routes
    ("Lagos (LOS)", "Dubai (DXB)"): 380000,
    ("Lagos (LOS)", "London (LHR)"): 520000,
    ("Lagos (LOS)", "New York (JFK)"): 950000,
    ("Lagos (LOS)", "Johannesburg (JNB)"): 310000,
    ("Lagos (LOS)", "Nairobi (NBO)"): 280000,
    ("Lagos (LOS)", "Accra (ACC)"): 95000,
    ("Lagos (LOS)", "Cape Town (CPT)"): 420000,
    ("Abuja (ABV)", "Dubai (DXB)"): 390000,
    ("Abuja (ABV)", "London (LHR)"): 530000,
    
    # Middle East to Europe/Asia
    ("Dubai (DXB)", "London (LHR)"): 220000,
    ("Dubai (DXB)", "Paris (CDG)"): 210000,
    ("Dubai (DXB)", "New York (JFK)"): 480000,
    ("Dubai (DXB)", "Singapore (SIN)"): 320000,
    ("Dubai (DXB)", "Bangkok (BKK)"): 190000,
    ("Dubai (DXB)", "Mumbai (BOM)"): 110000,
    ("Dubai (DXB)", "Kampala (EBB)"): 320000,
    
    # European Routes
    ("London (LHR)", "New York (JFK)"): 380000,
    ("London (LHR)", "Paris (CDG)"): 75000,
    ("London (LHR)", "Dubai (DXB)"): 220000,
    ("London (LHR)", "Singapore (SIN)"): 520000,
    ("Paris (CDG)", "Dubai (DXB)"): 210000,
    ("Paris (CDG)", "New York (JFK)"): 390000,
    ("Istanbul (IST)", "Dubai (DXB)"): 140000,
    
    # African Routes
    ("Nairobi (NBO)", "Dubai (DXB)"): 270000,
    ("Nairobi (NBO)", "London (LHR)"): 420000,
    ("Nairobi (NBO)", "Johannesburg (JNB)"): 220000,
    ("Johannesburg (JNB)", "Dubai (DXB)"): 350000,
    ("Johannesburg (JNB)", "London (LHR)"): 470000,
    ("Cape Town (CPT)", "Dubai (DXB)"): 380000,
    ("Cape Town (CPT)", "London (LHR)"): 520000,
    
    # Asian Routes
    ("Singapore (SIN)", "Bangkok (BKK)"): 85000,
    ("Singapore (SIN)", "Dubai (DXB)"): 320000,
    ("Singapore (SIN)", "London (LHR)"): 520000,
    ("Bangkok (BKK)", "Dubai (DXB)"): 190000,
    ("Mumbai (BOM)", "Dubai (DXB)"): 110000,
    ("Mumbai (BOM)", "London (LHR)"): 380000,
}

# Generate flights for ALL routes (180 days)
flights_list = []
flight_id = 1

print("✈️ Generating flights for 180 days...")

for (from_city, to_city), base_price in route_prices.items():
    for airline in airlines:
        # Calculate price with airline variation
        price_variation = random.uniform(0.92, 1.08)
        economy_price = int(base_price * price_variation)
        business_price = int(economy_price * 3.2)
        first_price = int(economy_price * 5.5)
        
        # Generate for next 180 days (6 months)
        for day_offset in range(1, 181):
            flight_date = (datetime.now() + timedelta(days=day_offset)).strftime('%Y-%m-%d')
            
            # Seasonal pricing adjustment
            month = int(flight_date[5:7])
            seasonal_multiplier = 1.0
            if month in [12, 1, 7, 8]:  # Peak seasons
                seasonal_multiplier = 1.25
            elif month in [4, 5, 6, 11]:  # Shoulder seasons
                seasonal_multiplier = 1.1
            else:
                seasonal_multiplier = 0.95
            
            final_economy = int(economy_price * seasonal_multiplier)
            final_business = int(business_price * seasonal_multiplier)
            final_first = int(first_price * seasonal_multiplier)
            
            # Random times
            hour = random.choice([6, 8, 10, 12, 14, 16, 18, 20, 22])
            minute = random.choice([0, 15, 30, 45])
            duration_h = random.randint(2, 12)
            duration_m = random.choice([0, 15, 30, 45])
            
            flight = {
                'id': flight_id,
                'flight_number': f"{airline['code']}{random.randint(100, 999)}",
                'airline': airline['name'],
                'from_city': from_city,
                'to_city': to_city,
                'departure_time': f"{hour:02d}:{minute:02d}",
                'arrival_time': f"{(hour + duration_h) % 24:02d}:{duration_m:02d}",
                'duration': f"{duration_h}h {duration_m}m",
                'date': flight_date,
                'economy_price': final_economy,
                'business_price': final_business,
                'first_price': final_first,
                'price': final_economy
            }
            flights_list.append(flight)
            flight_id += 1
            
            # Limit to 15,000 flights for performance
            if flight_id > 15000:
                break
        if flight_id > 15000:
            break
    if flight_id > 15000:
        break

print(f"✅ Generated {len(flights_list)} flights for {len(route_prices)} routes")

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
    
    # Search for outbound flights
    outbound = []
    for f in flights_list:
        if f['from_city'] == from_city and f['to_city'] == to_city and f['date'] == date:
            copy = f.copy()
            if cabin == 'economy':
                copy['price'] = copy['economy_price']
            elif cabin == 'business':
                copy['price'] = copy['business_price']
            else:
                copy['price'] = copy['first_price']
            outbound.append(copy)
    
    # If no flights on exact date, show nearby dates
    if not outbound:
        for f in flights_list:
            if f['from_city'] == from_city and f['to_city'] == to_city:
                copy = f.copy()
                if cabin == 'economy':
                    copy['price'] = copy['economy_price']
                elif cabin == 'business':
                    copy['price'] = copy['business_price']
                else:
                    copy['price'] = copy['first_price']
                outbound.append(copy)
                if len(outbound) >= 15:
                    break
    
    # Search for return flights
    return_flights = []
    if trip_type == 'round' and return_date:
        for f in flights_list:
            if f['to_city'] == from_city and f['from_city'] == to_city and f['date'] == return_date:
                copy = f.copy()
                if cabin == 'economy':
                    copy['price'] = copy['economy_price']
                elif cabin == 'business':
                    copy['price'] = copy['business_price']
                else:
                    copy['price'] = copy['first_price']
                return_flights.append(copy)
        
        if not return_flights:
            for f in flights_list:
                if f['to_city'] == from_city and f['from_city'] == to_city:
                    copy = f.copy()
                    if cabin == 'economy':
                        copy['price'] = copy['economy_price']
                    elif cabin == 'business':
                        copy['price'] = copy['business_price']
                    else:
                        copy['price'] = copy['first_price']
                    return_flights.append(copy)
                    if len(return_flights) >= 15:
                        break
    
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
        
        if not segment_results:
            for f in flights_list:
                if f['from_city'] == from_city and f['to_city'] == to_city:
                    copy = f.copy()
                    if cabin == 'economy':
                        copy['price'] = copy['economy_price']
                    elif cabin == 'business':
                        copy['price'] = copy['business_price']
                    else:
                        copy['price'] = copy['first_price']
                    segment_results.append(copy)
                    if len(segment_results) >= 8:
                        break
        
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
    print("✨ DOUBLE H CONCIERGE - LUXURY TRAVEL SYSTEM")
    print("="*60)
    print(f"🌍 Cities: {len(cities)} worldwide (including Uganda!)")
    print(f"✈️ Routes: {len(route_prices)} major routes")
    print(f"💎 Airlines: {len(airlines)} premium carriers")
    print(f"📅 Flights available: {len(flights_list)} (next 180 days)")
    print(f"\n🇺🇬 Uganda routes included:")
    print("   • Kampala → Dubai (₦320,000)")
    print("   • Kampala → London (₦480,000)")
    print("   • Kampala → Nairobi (₦95,000)")
    print("\n🌐 Server running on port " + str(port))
    app.run(host='0.0.0.0', port=port)
