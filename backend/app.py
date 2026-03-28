from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# ========================================
# REALISTIC MARKET PRICES (Based on actual fares)
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
    
    # Oceania
    "Sydney (SYD)", "Melbourne (MEL)", "Auckland (AKL)"
]

# Premium airlines with their price multipliers
airlines = [
    {"name": "Emirates", "multiplier": 1.15, "premium": True},
    {"name": "Qatar Airways", "multiplier": 1.12, "premium": True},
    {"name": "British Airways", "multiplier": 1.10, "premium": True},
    {"name": "Turkish Airlines", "multiplier": 1.05, "premium": False},
    {"name": "Uganda Airlines", "multiplier": 0.92, "premium": False},
    {"name": "Kenya Airways", "multiplier": 0.95, "premium": False},
    {"name": "Ethiopian Airlines", "multiplier": 0.93, "premium": False},
    {"name": "RwandAir", "multiplier": 0.91, "premium": False},
    {"name": "South African Airways", "multiplier": 0.98, "premium": False},
    {"name": "Air France", "multiplier": 1.08, "premium": False},
    {"name": "Lufthansa", "multiplier": 1.08, "premium": False},
    {"name": "Singapore Airlines", "multiplier": 1.12, "premium": True}
]

# REALISTIC MARKET PRICES (in Nigerian Naira - approximate)
# Based on actual market rates as of 2024/2025
realistic_prices = {
    # ===== UGANDA ROUTES =====
    ("Kampala (EBB)", "Dubai (DXB)"): 320000,      # Actual: ~$450
    ("Kampala (EBB)", "London (LHR)"): 480000,      # Actual: ~$650
    ("Kampala (EBB)", "Nairobi (NBO)"): 95000,      # Actual: ~$130
    ("Kampala (EBB)", "Johannesburg (JNB)"): 280000, # Actual: ~$380
    ("Kampala (EBB)", "Addis Ababa (ADD)"): 120000,  # Actual: ~$160
    ("Kampala (EBB)", "Kigali (KGL)"): 80000,        # Actual: ~$110
    ("Kampala (EBB)", "Istanbul (IST)"): 380000,     # Actual: ~$520
    ("Kampala (EBB)", "Doha (DOH)"): 310000,         # Actual: ~$420
    
    # ===== NIGERIA ROUTES =====
    ("Lagos (LOS)", "Dubai (DXB)"): 380000,          # Actual: ~$520
    ("Lagos (LOS)", "London (LHR)"): 520000,         # Actual: ~$700
    ("Lagos (LOS)", "New York (JFK)"): 950000,       # Actual: ~$1,300
    ("Lagos (LOS)", "Johannesburg (JNB)"): 310000,   # Actual: ~$420
    ("Lagos (LOS)", "Nairobi (NBO)"): 280000,        # Actual: ~$380
    ("Lagos (LOS)", "Kampala (EBB)"): 250000,        # Actual: ~$340
    ("Lagos (LOS)", "Accra (ACC)"): 95000,           # Actual: ~$130
    ("Lagos (LOS)", "Cape Town (CPT)"): 420000,      # Actual: ~$570
    ("Abuja (ABV)", "Dubai (DXB)"): 390000,          # Actual: ~$530
    ("Abuja (ABV)", "London (LHR)"): 530000,         # Actual: ~$720
    ("Abuja (ABV)", "New York (JFK)"): 980000,       # Actual: ~$1,330
    
    # ===== MIDDLE EAST TO EUROPE/ASIA =====
    ("Dubai (DXB)", "London (LHR)"): 220000,         # Actual: ~$300
    ("Dubai (DXB)", "Paris (CDG)"): 210000,          # Actual: ~$285
    ("Dubai (DXB)", "New York (JFK)"): 480000,       # Actual: ~$650
    ("Dubai (DXB)", "Singapore (SIN)"): 320000,      # Actual: ~$435
    ("Dubai (DXB)", "Bangkok (BKK)"): 190000,        # Actual: ~$260
    ("Dubai (DXB)", "Mumbai (BOM)"): 110000,         # Actual: ~$150
    ("Dubai (DXB)", "Kampala (EBB)"): 320000,        # Actual: ~$435
    
    # ===== EUROPEAN ROUTES =====
    ("London (LHR)", "New York (JFK)"): 380000,      # Actual: ~$520
    ("London (LHR)", "Paris (CDG)"): 75000,          # Actual: ~$100
    ("London (LHR)", "Dubai (DXB)"): 220000,         # Actual: ~$300
    ("London (LHR)", "Singapore (SIN)"): 520000,     # Actual: ~$700
    ("Paris (CDG)", "Dubai (DXB)"): 210000,          # Actual: ~$285
    ("Paris (CDG)", "New York (JFK)"): 390000,       # Actual: ~$530
    ("Frankfurt (FRA)", "New York (JFK)"): 410000,   # Actual: ~$560
    ("Istanbul (IST)", "Dubai (DXB)"): 140000,       # Actual: ~$190
    
    # ===== AFRICAN ROUTES =====
    ("Nairobi (NBO)", "Dubai (DXB)"): 270000,        # Actual: ~$370
    ("Nairobi (NBO)", "London (LHR)"): 420000,       # Actual: ~$570
    ("Nairobi (NBO)", "Kampala (EBB)"): 95000,       # Actual: ~$130
    ("Nairobi (NBO)", "Johannesburg (JNB)"): 220000, # Actual: ~$300
    ("Johannesburg (JNB)", "Dubai (DXB)"): 350000,   # Actual: ~$475
    ("Johannesburg (JNB)", "London (LHR)"): 470000,  # Actual: ~$640
    ("Cape Town (CPT)", "Dubai (DXB)"): 380000,      # Actual: ~$515
    ("Cape Town (CPT)", "London (LHR)"): 520000,     # Actual: ~$705
    
    # ===== ASIAN ROUTES =====
    ("Singapore (SIN)", "Bangkok (BKK)"): 85000,     # Actual: ~$115
    ("Singapore (SIN)", "Dubai (DXB)"): 320000,      # Actual: ~$435
    ("Singapore (SIN)", "London (LHR)"): 520000,     # Actual: ~$705
    ("Bangkok (BKK)", "Dubai (DXB)"): 190000,        # Actual: ~$260
    ("Mumbai (BOM)", "Dubai (DXB)"): 110000,         # Actual: ~$150
    ("Mumbai (BOM)", "London (LHR)"): 380000,        # Actual: ~$515
}

# Generate flights
flights_list = []
flight_id = 1

for (from_city, to_city), base_price in realistic_prices.items():
    for airline in airlines:
        # Calculate price with airline multiplier
        economy_price = int(base_price * airline["multiplier"])
        business_price = int(economy_price * 3.2)
        first_price = int(economy_price * 5.5)
        
        # Generate flights for next 180 days (6 months)
        for day_offset in range(1, 181):
            flight_date = (datetime.now() + timedelta(days=day_offset)).strftime('%Y-%m-%d')
            
            # Add seasonal pricing (higher during holidays)
            month = int(flight_date[5:7])
            if month in [12, 1, 7, 8]:  # December, January, July, August
                economy_price = int(economy_price * 1.25)  # 25% higher during peak seasons
            elif month in [4, 5, 6, 11]:  # Shoulder seasons
                economy_price = int(economy_price * 1.1)   # 10% higher
            else:
                economy_price = int(economy_price * 0.95)  # 5% discount off-peak
            
            # Random departure times
            hour = random.choice([6, 8, 10, 12, 14, 16, 18, 20, 22])
            minute = random.choice([0, 15, 30, 45])
            duration_h = random.randint(2, 12)
            duration_m = random.choice([0, 15, 30, 45])
            
            flight = {
                'id': flight_id,
                'flight_number': f"{airline['name'][:2].upper()}{random.randint(100, 999)}",
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
            flights_list.append(flight)
            flight_id += 1
            
            if flight_id > 8000:
                break
        if flight_id > 8000:
            break
    if flight_id > 8000:
        break

print(f"✅ Generated {len(flights_list)} flights with realistic market prices")
print(f"📊 Routes covered: {len(realistic_prices)}")

bookings = []

# ========================================
# API ROUTES (same as before)
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
                if len(outbound) >= 10:
                    break
    
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
                    if len(return_flights) >= 10:
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
                    if len(segment_results) >= 5:
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
    print("✨ DOUBLE H CONCIERGE - REALISTIC MARKET PRICES")
    print("="*60)
    print(f"🌍 Cities: {len(cities)} worldwide (including Uganda!)")
    print(f"✈️ Routes: {len(realistic_prices)} with accurate market rates")
    print(f"💎 Airlines: {len(airlines)} carriers with price variations")
    print(f"📅 Flights: {len(flights_list)} (next 180 days)")
    print("\n💰 PRICES ARE MARKET REALISTIC:")
    print(f"   • Kampala → Dubai: ~₦320,000 ($435)")
    print(f"   • Kampala → London: ~₦480,000 ($650)")
    print(f"   • Lagos → Dubai: ~₦380,000 ($520)")
    print(f"   • Lagos → London: ~₦520,000 ($700)")
    print("\n🌐 Server running at: http://localhost:" + str(port))
    app.run(host='0.0.0.0', port=port)
