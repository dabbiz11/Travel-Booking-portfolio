from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from datetime import datetime, timedelta
import random
import string
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# ========================================
# FLIGHT DATA
# ========================================

cities = [
    "Lagos (LOS)", "Abuja (ABV)", "Dubai (DXB)", "London (LHR)", 
    "New York (JFK)", "Paris (CDG)", "Istanbul (IST)", "Cape Town (CPT)"
]

airlines = [
    {"name": "Emirates", "code": "EK"},
    {"name": "Qatar Airways", "code": "QR"},
    {"name": "British Airways", "code": "BA"},
    {"name": "Turkish Airlines", "code": "TK"}
]

# Base fares
route_fares = {
    ("Lagos (LOS)", "Dubai (DXB)"): 650000,
    ("Lagos (LOS)", "London (LHR)"): 850000,
    ("Lagos (LOS)", "New York (JFK)"): 1200000,
    ("Dubai (DXB)", "Lagos (LOS)"): 650000,
    ("London (LHR)", "Dubai (DXB)"): 280000,
}

cabin_multipliers = {"economy": 1.0, "business": 3.2, "first": 5.5}

# Generate flights
flights = []
flight_id = 1

for from_city, to_city in route_fares.keys():
    base = route_fares[(from_city, to_city)]
    for airline in airlines:
        economy = int(base * 1.1)
        business = int(economy * 3.2)
        first = int(economy * 5.5)
        
        for day in range(1, 31):
            date = (datetime.now() + timedelta(days=day)).strftime('%Y-%m-%d')
            flight = {
                'id': flight_id,
                'flight_number': f"{airline['code']}{random.randint(100, 999)}",
                'airline': airline['name'],
                'from_city': from_city,
                'to_city': to_city,
                'departure_time': f"{random.randint(6, 22)}:{random.choice(['00','15','30','45'])}",
                'arrival_time': f"{(random.randint(8, 24))}:{random.choice(['00','15','30','45'])}",
                'duration': f"{random.randint(2, 8)}h {random.randint(0, 59)}m",
                'date': date,
                'economy_price': economy,
                'business_price': business,
                'first_price': first,
                'price': economy
            }
            flights.append(flight)
            flight_id += 1

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
    
    results = []
    for f in flights:
        if f['from_city'] == from_city and f['to_city'] == to_city and f['date'] == date:
            copy = f.copy()
            if cabin == 'economy':
                copy['price'] = copy['economy_price']
            elif cabin == 'business':
                copy['price'] = copy['business_price']
            else:
                copy['price'] = copy['first_price']
            results.append(copy)
    
    return jsonify(results)

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.json
    ref = f"DH-{datetime.now().strftime('%Y%m')}-{random.randint(1000, 9999)}"
    
    booking = {
        'id': len(bookings) + 1,
        'booking_reference': ref,
        'flight': data.get('flight'),
        'passenger_name': data.get('passenger_name'),
        'email': data.get('email'),
        'phone': data.get('phone'),
        'total_amount': data.get('total_amount'),
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
    app.run(host='0.0.0.0', port=port)
