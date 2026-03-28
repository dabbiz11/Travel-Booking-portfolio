from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import random
import string

app = Flask(__name__)
CORS(app)

# ========================================
# COMPLETE HTML CONTENT (same as before)
# ========================================

HTML_CONTENT = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Double H Concierge | Global Luxury Travel</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root {
            --navy: #0A1A2F;
            --navy-light: #0F2A3F;
            --gold: #C6A43B;
            --gold-dark: #9B7E2E;
            --cream: #F5F0E6;
            --white: #FFFFFF;
            --gray: #6B7280;
            --gray-light: #E5E7EB;
        }
        body {
            font-family: 'Inter', sans-serif;
            background: var(--navy);
            color: var(--cream);
            line-height: 1.5;
        }
        .navbar {
            background: rgba(10, 26, 47, 0.98);
            backdrop-filter: blur(10px);
            padding: 1.2rem 2rem;
            position: fixed;
            width: 100%;
            top: 0;
            z-index: 1000;
            border-bottom: 1px solid rgba(198, 164, 59, 0.2);
        }
        .nav-container {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo h1 {
            font-size: 1.5rem;
            font-weight: 600;
            letter-spacing: -0.5px;
        }
        .logo h1 span { color: var(--gold); font-weight: 700; }
        .logo p { font-size: 0.7rem; color: var(--gray); letter-spacing: 1px; }
        .nav-links { display: flex; gap: 2.5rem; }
        .nav-links a {
            color: var(--cream);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            transition: color 0.3s;
            cursor: pointer;
        }
        .nav-links a:hover { color: var(--gold); }
        .hero {
            min-height: 85vh;
            background: linear-gradient(135deg, rgba(10, 26, 47, 0.95), rgba(10, 26, 47, 0.85)), url('https://images.pexels.com/photos/2166711/pexels-photo-2166711.jpeg?auto=compress&cs=tinysrgb&w=1600');
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
            text-align: center;
            padding-top: 80px;
        }
        .hero-content { max-width: 800px; margin: 0 auto; padding: 4rem 2rem; }
        .hero-badge {
            display: inline-block;
            padding: 0.4rem 1.2rem;
            background: rgba(198, 164, 59, 0.15);
            border-radius: 50px;
            font-size: 0.75rem;
            font-weight: 500;
            color: var(--gold);
            margin-bottom: 1.5rem;
        }
        .hero h1 { font-size: 3.5rem; font-weight: 700; line-height: 1.2; margin-bottom: 1rem; }
        .hero h1 span { color: var(--gold); }
        .hero p { font-size: 1.1rem; color: var(--gray-light); margin-bottom: 2rem; }
        .search-card {
            max-width: 1200px;
            margin: -2rem auto 3rem;
            background: var(--white);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
            position: relative;
            z-index: 10;
        }
        .search-form {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.2rem;
        }
        .form-group { display: flex; flex-direction: column; }
        .form-group label {
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--gray);
            margin-bottom: 0.5rem;
        }
        .form-group input, .form-group select {
            padding: 0.9rem 1rem;
            border: 1px solid var(--gray-light);
            border-radius: 10px;
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            transition: all 0.3s;
            background: var(--white);
        }
        .form-group input:focus, .form-group select:focus {
            outline: none;
            border-color: var(--gold);
            box-shadow: 0 0 0 3px rgba(198, 164, 59, 0.1);
        }
        .search-btn {
            background: var(--gold);
            color: var(--navy);
            border: none;
            padding: 0.9rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 1.5rem;
            width: 100%;
        }
        .search-btn:hover { background: var(--gold-dark); transform: translateY(-1px); }
        .results-section {
            max-width: 1200px;
            margin: 3rem auto;
            display: none;
        }
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        .section-header h2 { font-size: 1.5rem; font-weight: 600; }
        .section-header h2 span { color: var(--gold); }
        .result-count { color: var(--gray); font-size: 0.85rem; }
        .flight-card {
            background: var(--navy-light);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.3s;
            cursor: pointer;
            border: 1px solid rgba(198, 164, 59, 0.2);
        }
        .flight-card:hover { border-color: var(--gold); transform: translateX(5px); }
        .flight-info h3 { font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem; }
        .flight-route { display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem; font-size: 0.9rem; }
        .flight-time { font-weight: 600; color: var(--gold); }
        .flight-duration { color: var(--gray); font-size: 0.8rem; }
        .flight-price { text-align: right; }
        .price-amount { font-size: 1.5rem; font-weight: 700; color: var(--gold); }
        .price-amount small { font-size: 0.75rem; font-weight: normal; color: var(--gray); }
        .book-btn {
            background: transparent;
            color: var(--gold);
            border: 1px solid var(--gold);
            padding: 0.5rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            font-size: 0.8rem;
            cursor: pointer;
            margin-top: 0.5rem;
            transition: all 0.3s;
        }
        .book-btn:hover { background: var(--gold); color: var(--navy); }
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            justify-content: center;
            align-items: center;
            z-index: 2000;
        }
        .modal-content {
            background: var(--white);
            border-radius: 16px;
            padding: 2rem;
            max-width: 500px;
            width: 90%;
            color: var(--navy);
        }
        .modal-content h3 { font-size: 1.3rem; margin-bottom: 1rem; color: var(--gold); }
        .modal-content input {
            width: 100%;
            padding: 0.9rem;
            margin-bottom: 1rem;
            border: 1px solid var(--gray-light);
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
        }
        .confirm-btn {
            background: var(--gold);
            color: var(--navy);
            border: none;
            padding: 0.9rem;
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
        }
        .bookings-list {
            background: var(--navy-light);
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
        }
        .booking-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 1rem;
            margin-bottom: 1rem;
            text-align: left;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .footer {
            background: var(--navy-light);
            text-align: center;
            padding: 2rem;
            margin-top: 4rem;
            border-top: 1px solid rgba(198, 164, 59, 0.2);
        }
        @media (max-width: 768px) {
            .hero h1 { font-size: 2rem; }
            .search-form { grid-template-columns: 1fr; }
            .flight-card { flex-direction: column; text-align: center; gap: 1rem; }
            .flight-price { text-align: center; }
            .nav-links { gap: 1rem; }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <div class="logo">
                <h1>DOUBLE H <span>CONCIERGE</span></h1>
                <p>Global Luxury Travel</p>
            </div>
            <div class="nav-links">
                <a onclick="showSearch()">Search Flights</a>
                <a onclick="showBookings()">My Bookings</a>
            </div>
        </div>
    </nav>

    <div class="hero">
        <div class="hero-content">
            <div class="hero-badge">GLOBAL NETWORK | 50+ DESTINATIONS</div>
            <h1>Your Journey,<br><span>Perfected</span></h1>
            <p>50+ countries • 180+ routes • Premium airlines • 6 months ahead</p>
        </div>
    </div>

    <div class="search-card" id="searchSection">
        <div class="search-form">
            <div class="form-group">
                <label>From</label>
                <select id="fromCity"></select>
            </div>
            <div class="form-group">
                <label>To</label>
                <select id="toCity"></select>
            </div>
            <div class="form-group">
                <label>Departure Date</label>
                <input type="date" id="departureDate">
            </div>
            <div class="form-group">
                <label>Cabin Class</label>
                <select id="cabinClass">
                    <option value="economy">Economy</option>
                    <option value="business">Business</option>
                    <option value="first">First Class</option>
                </select>
            </div>
            <div class="form-group">
                <label>Passengers</label>
                <select id="passengers">
                    <option value="1">1 Adult</option>
                    <option value="2">2 Adults</option>
                    <option value="3">3 Adults</option>
                    <option value="4">4 Adults</option>
                </select>
            </div>
        </div>
        <button class="search-btn" onclick="searchFlights()">Search Flights</button>
    </div>

    <div id="resultsSection" class="results-section">
        <div class="section-header">
            <h2>Available <span>Flights</span></h2>
            <div class="result-count" id="resultCount"></div>
        </div>
        <div id="flightList"></div>
    </div>

    <div id="bookingsSection" class="results-section">
        <div class="section-header">
            <h2>My <span>Bookings</span></h2>
        </div>
        <div id="bookingsList" class="bookings-list"></div>
    </div>

    <div id="bookingModal" class="modal">
        <div class="modal-content">
            <h3>Complete Your Booking</h3>
            <div id="modalDetails" style="margin-bottom: 1rem;"></div>
            <input type="text" id="passengerName" placeholder="Full Name">
            <input type="email" id="passengerEmail" placeholder="Email Address">
            <input type="tel" id="passengerPhone" placeholder="Phone Number">
            <button class="confirm-btn" onclick="confirmBooking()">Confirm Booking</button>
            <button onclick="closeModal()" style="margin-top: 0.5rem; width: 100%; padding: 0.5rem; background: none; border: 1px solid #ddd; border-radius: 8px;">Cancel</button>
        </div>
    </div>

    <footer class="footer">
        <p>&copy; 2024 Double H Concierge. Global luxury travel redefined.</p>
    </footer>

    <script>
        let selectedFlight = null;
        let allFlights = [];

        document.getElementById('departureDate').value = new Date().toISOString().split('T')[0];

        // Load cities from backend
        async function loadCities() {
            const response = await fetch('/api/cities');
            const cities = await response.json();
            const fromSelect = document.getElementById('fromCity');
            const toSelect = document.getElementById('toCity');
            
            cities.forEach(city => {
                fromSelect.innerHTML += `<option value="${city}">${city}</option>`;
                toSelect.innerHTML += `<option value="${city}">${city}</option>`;
            });
        }
        loadCities();

        async function searchFlights() {
            const from = document.getElementById('fromCity').value;
            const to = document.getElementById('toCity').value;
            const date = document.getElementById('departureDate').value;
            const cabin = document.getElementById('cabinClass').value;
            const passengers = document.getElementById('passengers').value;

            if (!from || !to) {
                alert('Please select departure and destination cities');
                return;
            }

            showLoading(true);
            
            try {
                const response = await fetch('/api/flights/search', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ from, to, date, cabin_class: cabin, passengers })
                });
                
                allFlights = await response.json();
                displayFlights(allFlights);
            } catch (error) {
                console.error('Error:', error);
                alert('Error searching flights. Please try again.');
            }
            
            showLoading(false);
        }

        function displayFlights(flights) {
            const flightList = document.getElementById('flightList');
            const resultCount = document.getElementById('resultCount');
            
            if (flights.length === 0) {
                flightList.innerHTML = '<div style="background: #0F2A3F; padding: 3rem; text-align: center; border-radius: 12px;">No flights available for this route. Please try different dates or destinations.</div>';
                resultCount.textContent = '0 results';
            } else {
                flightList.innerHTML = flights.map(flight => `
                    <div class="flight-card" onclick="selectFlight(${flight.id})">
                        <div class="flight-info">
                            <h3>✈️ ${flight.airline} • ${flight.flight_number}</h3>
                            <div class="flight-route">
                                <span class="flight-time">${flight.departure_time}</span>
                                <i class="fas fa-arrow-right"></i>
                                <span class="flight-time">${flight.arrival_time}</span>
                                <span class="flight-duration">${flight.duration}</span>
                            </div>
                            <div class="flight-duration">${flight.from_city} → ${flight.to_city}</div>
                        </div>
                        <div class="flight-price">
                            <div class="price-amount">₦${flight.price.toLocaleString()}<small>/pax</small></div>
                            <button class="book-btn">Select Flight</button>
                        </div>
                    </div>
                `).join('');
                resultCount.textContent = `${flights.length} flights found`;
            }
            
            document.getElementById('resultsSection').style.display = 'block';
            document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
        }

        function selectFlight(flightId) {
            selectedFlight = allFlights.find(f => f.id === flightId);
            const cabin = document.getElementById('cabinClass').value;
            const passengers = document.getElementById('passengers').value;
            const total = selectedFlight.price * parseInt(passengers);
            
            document.getElementById('modalDetails').innerHTML = `
                <p><strong>${selectedFlight.airline} ${selectedFlight.flight_number}</strong></p>
                <p>${selectedFlight.from_city} → ${selectedFlight.to_city}</p>
                <p>Departure: ${selectedFlight.departure_time} | ${selectedFlight.date}</p>
                <p>Cabin: ${cabin.toUpperCase()}</p>
                <p>Passengers: ${passengers}</p>
                <p><strong style="color: #C6A43B;">Total: ₦${total.toLocaleString()}</strong></p>
            `;
            document.getElementById('bookingModal').style.display = 'flex';
        }

        async function confirmBooking() {
            const name = document.getElementById('passengerName').value;
            const email = document.getElementById('passengerEmail').value;
            const phone = document.getElementById('passengerPhone').value;
            const passengers = document.getElementById('passengers').value;

            if (!name || !email || !phone) {
                alert('Please fill in all passenger details');
                return;
            }

            const total = selectedFlight.price * parseInt(passengers);

            try {
                const response = await fetch('/api/bookings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        flight: selectedFlight,
                        passenger_name: name,
                        email: email,
                        phone: phone,
                        total_amount: total,
                        passengers: passengers
                    })
                });
                
                const result = await response.json();
                alert(`✓ Booking Confirmed!\n\nReference: ${result.booking_reference}\n\nA Double H Concierge specialist will contact you within 24 hours.`);
                
                closeModal();
                document.getElementById('passengerName').value = '';
                document.getElementById('passengerEmail').value = '';
                document.getElementById('passengerPhone').value = '';
            } catch (error) {
                alert('Error processing booking. Please try again.');
            }
        }

        async function showBookings() {
            try {
                const response = await fetch('/api/bookings/my-bookings');
                const bookings = await response.json();
                
                const bookingsList = document.getElementById('bookingsList');
                if (bookings.length === 0) {
                    bookingsList.innerHTML = '<div style="text-align: center; padding: 2rem;">No bookings yet. Start your luxury journey with us.</div>';
                } else {
                    bookingsList.innerHTML = bookings.map(b => `
                        <div class="booking-card">
                            <div>
                                <strong>${b.booking_reference}</strong><br>
                                <small>${b.flight?.from_city} → ${b.flight?.to_city}</small>
                            </div>
                            <div>
                                <span style="color: #C6A43B;">₦${b.total_amount?.toLocaleString()}</span><br>
                                <small>${b.status || 'Confirmed'}</small>
                            </div>
                        </div>
                    `).join('');
                }
                
                document.getElementById('searchSection').style.display = 'none';
                document.getElementById('resultsSection').style.display = 'none';
                document.getElementById('bookingsSection').style.display = 'block';
            } catch (error) {
                alert('Error loading bookings');
            }
        }

        function showSearch() {
            document.getElementById('searchSection').style.display = 'block';
            document.getElementById('resultsSection').style.display = 'none';
            document.getElementById('bookingsSection').style.display = 'none';
        }

        function closeModal() {
            document.getElementById('bookingModal').style.display = 'none';
            selectedFlight = null;
        }

        function showLoading(show) {
            const btn = document.querySelector('.search-btn');
            if (show) {
                btn.textContent = 'Searching...';
                btn.disabled = true;
            } else {
                btn.textContent = 'Search Flights';
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
'''

# ========================================
# 50+ COUNTRIES WORLDWIDE
# ========================================

cities = [
    # Africa
    "Lagos (LOS)", "Abuja (ABV)", "Cape Town (CPT)", "Johannesburg (JNB)", "Nairobi (NBO)", 
    "Kampala (EBB)", "Entebbe (EBB)", "Accra (ACC)", "Casablanca (CMN)", "Cairo (CAI)",
    "Addis Ababa (ADD)", "Dar es Salaam (DAR)", "Kigali (KGL)", "Mauritius (MRU)", "Marrakech (RAK)",
    
    # Middle East
    "Dubai (DXB)", "Abu Dhabi (AUH)", "Doha (DOH)", "Riyadh (RUH)", "Jeddah (JED)", 
    "Kuwait (KWI)", "Muscat (MCT)", "Bahrain (BAH)", "Tel Aviv (TLV)", "Amman (AMM)",
    
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
    "Christchurch (CHC)", "Wellington (WLG)", "Fiji (NAN)", "Papua New Guinea (POM)", "New Caledonia (NOU)"
]

# Premium global airlines
airlines = [
    {"name": "Emirates", "code": "EK", "base_multiplier": 1.2, "hubs": ["DXB"]},
    {"name": "Qatar Airways", "code": "QR", "base_multiplier": 1.15, "hubs": ["DOH"]},
    {"name": "Etihad Airways", "code": "EY", "base_multiplier": 1.12, "hubs": ["AUH"]},
    {"name": "British Airways", "code": "BA", "base_multiplier": 1.1, "hubs": ["LHR"]},
    {"name": "Virgin Atlantic", "code": "VS", "base_multiplier": 1.1, "hubs": ["LHR"]},
    {"name": "Air France", "code": "AF", "base_multiplier": 1.08, "hubs": ["CDG"]},
    {"name": "Lufthansa", "code": "LH", "base_multiplier": 1.08, "hubs": ["FRA"]},
    {"name": "Turkish Airlines", "code": "TK", "base_multiplier": 1.05, "hubs": ["IST"]},
    {"name": "Singapore Airlines", "code": "SQ", "base_multiplier": 1.25, "hubs": ["SIN"]},
    {"name": "Cathay Pacific", "code": "CX", "base_multiplier": 1.22, "hubs": ["HKG"]},
    {"name": "United Airlines", "code": "UA", "base_multiplier": 1.02, "hubs": ["EWR"]},
    {"name": "Delta Air Lines", "code": "DL", "base_multiplier": 1.02, "hubs": ["ATL"]},
    {"name": "American Airlines", "code": "AA", "base_multiplier": 1.02, "hubs": ["JFK"]},
    {"name": "Kenya Airways", "code": "KQ", "base_multiplier": 0.95, "hubs": ["NBO"]},
    {"name": "RwandAir", "code": "WB", "base_multiplier": 0.92, "hubs": ["KGL"]},
    {"name": "Ethiopian Airlines", "code": "ET", "base_multiplier": 0.98, "hubs": ["ADD"]},
    {"name": "South African Airways", "code": "SA", "base_multiplier": 0.96, "hubs": ["JNB"]},
    {"name": "Uganda Airlines", "code": "UR", "base_multiplier": 0.88, "hubs": ["EBB"]}
]

cabin_multipliers = {"economy": 1.0, "business": 3.2, "first": 5.5}

# Base fare calculator based on distance
def calculate_base_fare(from_city, to_city):
    # Extract airport codes
    from_code = from_city.split("(")[-1].replace(")", "").strip()
    to_code = to_city.split("(")[-1].replace(")", "").strip()
    
    # Base fare matrix (simplified for demo)
    fare_map = {
        # Africa routes
        ("LOS", "JNB"): 450000, ("LOS", "CPT"): 500000, ("LOS", "NBO"): 380000,
        ("LOS", "EBB"): 320000, ("LOS", "KGL"): 350000, ("LOS", "ADD"): 360000,
        ("LOS", "CAI"): 420000, ("LOS", "CMN"): 480000, ("LOS", "ACC"): 220000,
        
        # Middle East routes
        ("LOS", "DXB"): 650000, ("LOS", "AUH"): 630000, ("LOS", "DOH"): 620000,
        ("LOS", "RUH"): 580000, ("LOS", "JED"): 560000, ("LOS", "KWI"): 590000,
        
        # Europe routes
        ("LOS", "LHR"): 850000, ("LOS", "CDG"): 780000, ("LOS", "FRA"): 800000,
        ("LOS", "AMS"): 790000, ("LOS", "MXP"): 770000, ("LOS", "BCN"): 760000,
        
        # North America
        ("LOS", "JFK"): 1200000, ("LOS", "LAX"): 1350000, ("LOS", "YYZ"): 1150000,
        
        # Asia
        ("LOS", "DXB"): 650000, ("DXB", "SIN"): 280000, ("DXB", "BKK"): 250000,
        ("DXB", "HKG"): 320000, ("DXB", "BOM"): 180000, ("DXB", "DEL"): 190000,
        
        # Intra-Africa
        ("NBO", "EBB"): 120000, ("NBO", "KGL"): 130000, ("NBO", "JNB"): 280000,
        ("EBB", "NBO"): 120000, ("EBB", "KGL"): 110000, ("EBB", "JNB"): 350000,
        ("JNB", "CPT"): 150000, ("JNB", "LOS"): 450000, ("JNB", "NBO"): 280000,
        
        # Europe connections
        ("LHR", "CDG"): 120000, ("LHR", "FRA"): 140000, ("LHR", "AMS"): 110000,
        ("LHR", "DXB"): 280000, ("LHR", "JFK"): 450000, ("CDG", "DXB"): 320000,
        
        # Default fare
        "default": 400000
    }
    
    key = (from_code, to_code)
    if key in fare_map:
        return fare_map[key]
    
    # Return default fare based on distance approximation
    return fare_map["default"]

# Generate flights - 6 months ahead, all routes
flights = []
flight_id = 1

# Only generate for popular routes to keep manageable
popular_routes = [
    # Major Africa routes
    ("Lagos (LOS)", "Dubai (DXB)"), ("Lagos (LOS)", "London (LHR)"), ("Lagos (LOS)", "New York (JFK)"),
    ("Lagos (LOS)", "Johannesburg (JNB)"), ("Lagos (LOS)", "Nairobi (NBO)"), ("Lagos (LOS)", "Kampala (EBB)"),
    ("Lagos (LOS)", "Accra (ACC)"), ("Lagos (LOS)", "Cairo (CAI)"), ("Lagos (LOS)", "Paris (CDG)"),
    
    # East Africa hub
    ("Kampala (EBB)", "Dubai (DXB)"), ("Kampala (EBB)", "London (LHR)"), ("Kampala (EBB)", "Nairobi (NBO)"),
    ("Kampala (EBB)", "Johannesburg (JNB)"), ("Kampala (EBB)", "Kigali (KGL)"), ("Kampala (EBB)", "Addis Ababa (ADD)"),
    
    # South Africa
    ("Cape Town (CPT)", "Dubai (DXB)"), ("Cape Town (CPT)", "London (LHR)"), ("Cape Town (CPT)", "Johannesburg (JNB)"),
    ("Johannesburg (JNB)", "Dubai (DXB)"), ("Johannesburg (JNB)", "London (LHR)"), ("Johannesburg (JNB)", "Nairobi (NBO)"),
    
    # Kenya
    ("Nairobi (NBO)", "Dubai (DXB)"), ("Nairobi (NBO)", "London (LHR)"), ("Nairobi (NBO)", "Kampala (EBB)"),
    ("Nairobi (NBO)", "Kigali (KGL)"), ("Nairobi (NBO)", "Johannesburg (JNB)"),
    
    # Middle East to Europe/Asia
    ("Dubai (DXB)", "London (LHR)"), ("Dubai (DXB)", "New York (JFK)"), ("Dubai (DXB)", "Singapore (SIN)"),
    ("Dubai (DXB)", "Bangkok (BKK)"), ("Dubai (DXB)", "Paris (CDG)"), ("Dubai (DXB)", "Istanbul (IST)"),
    ("Dubai (DXB)", "Cape Town (CPT)"), ("Dubai (DXB)", "Nairobi (NBO)"), ("Dubai (DXB)", "Kampala (EBB)"),
    
    # European connections
    ("London (LHR)", "New York (JFK)"), ("London (LHR)", "Dubai (DXB)"), ("London (LHR)", "Paris (CDG)"),
    ("London (LHR)", "Frankfurt (FRA)"), ("London (LHR)", "Singapore (SIN)"), ("London (LHR)", "Cape Town (CPT)"),
    
    ("Paris (CDG)", "New York (JFK)"), ("Paris (CDG)", "Dubai (DXB)"), ("Paris (CDG)", "Singapore (SIN)"),
    
    ("Frankfurt (FRA)", "New York (JFK)"), ("Frankfurt (FRA)", "Dubai (DXB)"), ("Frankfurt (FRA)", "Singapore (SIN)"),
    
    # Asian connections
    ("Singapore (SIN)", "Bangkok (BKK)"), ("Singapore (SIN)", "Hong Kong (HKG)"), ("Singapore (SIN)", "Tokyo (HND)"),
    ("Singapore (SIN)", "Sydney (SYD)"), ("Singapore (SIN)", "Dubai (DXB)"), ("Singapore (SIN)", "London (LHR)"),
    
    # US connections
    ("New York (JFK)", "London (LHR)"), ("New York (JFK)", "Dubai (DXB)"), ("New York (JFK)", "Paris (CDG)"),
    ("New York (JFK)", "Los Angeles (LAX)"), ("New York (JFK)", "Miami (MIA)"),
]

print("✈️ Generating global flights for 180 days...")

# Generate flights for each route
for from_city, to_city in popular_routes:
    base_fare = calculate_base_fare(from_city, to_city)
    
    for airline in airlines:
        # Skip airlines that don't serve certain routes (simplified)
        if airline["hubs"][0] not in from_city and airline["hubs"][0] not in to_city:
            if random.random() > 0.3:  # 30% chance for non-hub airlines
                continue
        
        economy_price = int(base_fare * airline["base_multiplier"])
        business_price = int(economy_price * cabin_multipliers["business"])
        first_price = int(economy_price * cabin_multipliers["first"])
        
        # Generate for next 180 days (6 months)
        for day_offset in range(1, 181):
            flight_date = (datetime.now() + timedelta(days=day_offset)).strftime('%Y-%m-%d')
            
            # Random times
            hour = random.choice([0, 2, 6, 8, 10, 12, 14, 16, 18, 20, 22])
            minute = random.choice([0, 15, 30, 45])
            duration_h = random.randint(2, 14)
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
                'economy_price': economy_price,
                'business_price': business_price,
                'first_price': first_price,
                'price': economy_price
            }
            flights.append(flight)
            flight_id += 1
            
            # Limit total flights to avoid memory issues (still plenty)
            if flight_id > 8000:
                break
        if flight_id > 8000:
            break
    if flight_id > 8000:
        break

print(f"✅ Generated {len(flights)} flights across {len(popular_routes)} routes")
print(f"📍 {len(cities)} cities worldwide")
print(f"✈️ {len(airlines)} premium airlines")
print(f"📅 Next 180 days of availability")

bookings = []

# ========================================
# API ENDPOINTS
# ========================================

@app.route('/')
def home():
    return HTML_CONTENT

@app.route('/api/cities')
def get_cities():
    return jsonify(cities)

@app.route('/api/flights/search', methods=['POST'])
def search_flights():
    data = request.json
    from_city = data.get('from')
    to_city = data.get('to')
    date = data.get('date')
    cabin_class = data.get('cabin_class', 'economy')
    
    results = []
    for f in flights:
        if f['from_city'] == from_city and f['to_city'] == to_city and f['date'] == date:
            flight_copy = f.copy()
            if cabin_class == 'economy':
                flight_copy['price'] = flight_copy['economy_price']
            elif cabin_class == 'business':
                flight_copy['price'] = flight_copy['business_price']
            else:
                flight_copy['price'] = flight_copy['first_price']
            results.append(flight_copy)
    
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
        'passengers': data.get('passengers'),
        'status': 'confirmed',
        'booking_date': datetime.now().isoformat()
    }
    bookings.append(booking)
    
    return jsonify({'message': 'Booking confirmed', 'booking_reference': ref})

@app.route('/api/bookings/my-bookings', methods=['GET'])
def get_bookings():
    return jsonify(bookings)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("✨ DOUBLE H CONCIERGE - GLOBAL LUXURY TRAVEL")
    print("="*50)
    print(f"🌍 Cities: {len(cities)} worldwide")
    print(f"✈️ Routes: {len(popular_routes)} major routes")
    print(f"💎 Airlines: {len(airlines)} premium carriers")
    print(f"📅 Flights available: {len(flights)} (next 180 days)")
    print(f"\n🇺🇬 Uganda included: Kampala (EBB), Entebbe (EBB)")
    print("\n🌐 Server running at: http://localhost:5000")
    print("📋 Press Ctrl+C to stop\n")
    app.run(debug=True, port=5000)