from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random
from booking.models import TravelOption

class Command(BaseCommand):
    help = 'Populate database with realistic Indian travel options'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10000,
            help='Number of travel options to create',
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Major Indian cities with proper classification
        tier1_cities = [
            'Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad',
            'Pune', 'Ahmedabad', 'Surat', 'Jaipur'
        ]
        
        tier2_cities = [
            'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane', 'Bhopal',
            'Visakhapatnam', 'Pimpri-Chinchwad', 'Patna', 'Vadodara',
            'Ghaziabad', 'Ludhiana', 'Agra', 'Nashik', 'Faridabad',
            'Meerut', 'Rajkot', 'Kalyan-Dombivali', 'Vasai-Virar', 'Varanasi',
            'Srinagar', 'Aurangabad', 'Dhanbad', 'Amritsar', 'Allahabad',
            'Ranchi', 'Howrah', 'Coimbatore', 'Jabalpur', 'Gwalior'
        ]
        
        tier3_cities = [
            'Vijayawada', 'Jodhpur', 'Madurai', 'Raipur', 'Kota', 'Guwahati',
            'Chandigarh', 'Solapur', 'Hubballi-Dharwad', 'Tiruchirappalli',
            'Bareilly', 'Mysuru', 'Tiruppur', 'Gurgaon', 'Aligarh',
            'Jalandhar', 'Bhubaneswar', 'Salem', 'Warangal', 'Guntur',
            'Bhiwandi', 'Saharanpur', 'Gorakhpur', 'Bikaner', 'Amravati',
            'Noida', 'Jamshedpur', 'Bhilai Nagar', 'Cuttack', 'Firozabad',
            'Kochi', 'Nellore', 'Bhavnagar', 'Dehradun', 'Durgapur',
            'Asansol', 'Rourkela', 'Nanded', 'Kolhapur', 'Ajmer',
            'Akola', 'Gulbarga', 'Jamnagar', 'Ujjain', 'Loni',
            'Siliguri', 'Jhansi', 'Ulhasnagar', 'Jammu', 'Sangli-Miraj',
            'Belgaum', 'Mangalore', 'Ambattur', 'Tirunelveli', 'Malegaon'
        ]
        
        all_indian_cities = tier1_cities + tier2_cities + tier3_cities
        
        # International destinations accessible from major Indian airports
        international_destinations = [
            # Middle East
            'Dubai', 'Abu Dhabi', 'Sharjah', 'Doha', 'Kuwait City', 'Riyadh', 'Jeddah',
            'Muscat', 'Manama', 'Baghdad', 'Tehran', 'Beirut',
            
            # Southeast Asia
            'Singapore', 'Bangkok', 'Kuala Lumpur', 'Jakarta', 'Manila', 'Ho Chi Minh City',
            'Hanoi', 'Phuket', 'Denpasar', 'Yangon', 'Phnom Penh', 'Vientiane',
            
            # East Asia
            'Hong Kong', 'Tokyo', 'Osaka', 'Seoul', 'Busan', 'Taipei', 'Shanghai',
            'Beijing', 'Guangzhou', 'Shenzhen', 'Macau',
            
            # Europe
            'London', 'Paris', 'Frankfurt', 'Amsterdam', 'Zurich', 'Vienna',
            'Rome', 'Milan', 'Madrid', 'Barcelona', 'Brussels', 'Copenhagen',
            'Stockholm', 'Helsinki', 'Warsaw', 'Prague', 'Budapest', 'Bucharest',
            'Moscow', 'St. Petersburg', 'Istanbul', 'Athens',
            
            # North America
            'New York', 'Los Angeles', 'Chicago', 'San Francisco', 'Washington DC',
            'Boston', 'Atlanta', 'Dallas', 'Houston', 'Seattle', 'Toronto',
            'Vancouver', 'Montreal',
            
            # Oceania
            'Sydney', 'Melbourne', 'Perth', 'Brisbane', 'Adelaide', 'Auckland',
            
            # Africa
            'Johannesburg', 'Cape Town', 'Cairo', 'Nairobi', 'Lagos', 'Addis Ababa',
            'Dar es Salaam', 'Mauritius', 'Seychelles',
            
            # South America
            'São Paulo', 'Buenos Aires', 'Santiago', 'Lima',
            
            # Other destinations
            'Kathmandu', 'Dhaka', 'Karachi', 'Lahore', 'Islamabad', 'Colombo',
            'Male', 'Thimphu', 'Tashkent', 'Almaty', 'Ashgabat'
        ]
        
        # Realistic operators
        operators = {
            'FLIGHT': [
                # Indian carriers
                'IndiGo', 'Air India', 'SpiceJet', 'GoFirst', 'Vistara', 'Air India Express',
                'Alliance Air', 'TruJet', 'Star Air',
                # International carriers operating in India
                'Emirates', 'Qatar Airways', 'Etihad Airways', 'Singapore Airlines',
                'Thai Airways', 'Malaysia Airlines', 'Cathay Pacific', 'British Airways',
                'Lufthansa', 'KLM', 'Air France', 'Turkish Airlines', 'Flydubai',
                'Kuwait Airways', 'Oman Air', 'Saudi Arabian Airlines'
            ],
            'TRAIN': [
                'Indian Railways', 'Rajdhani Express', 'Shatabdi Express', 'Duronto Express',
                'Garib Rath', 'Jan Shatabdi', 'Intercity Express', 'Superfast Express',
                'Mail Express', 'Passenger Train', 'MEMU', 'DEMU', 'Vande Bharat Express',
                'Tejas Express', 'Double Decker Express', 'Humsafar Express'
            ],
            'BUS': [
                # Government operators
                'KSRTC', 'MSRTC', 'APSRTC', 'TNSTC', 'UPSRTC', 'RSRTC', 'GSRTC',
                'HRTC', 'PEPSU', 'DTC', 'BMTC', 'MTC', 'BEST',
                # Private operators
                'RedBus', 'Travels India', 'VRL Travels', 'SRS Travels', 'Kallada Travels',
                'Orange Tours', 'Neeta Tours', 'Prasanna Purple', 'Raj National Express',
                'Parveen Travels', 'Jabbar Travels', 'Paulo Travels', 'Sharma Travels',
                'Rajasthan Roadways', 'Punjab Roadways'
            ]
        }
        
        travel_types = ['FLIGHT', 'TRAIN', 'BUS']
        
        # Airport cities (can have international flights)
        international_airport_cities = [
            'Delhi', 'Mumbai', 'Bengaluru', 'Chennai', 'Kolkata', 'Hyderabad',
            'Pune', 'Ahmedabad', 'Kochi', 'Goa', 'Thiruvananthapuram', 'Calicut',
            'Coimbatore', 'Tiruchirappalli', 'Madurai', 'Amritsar', 'Chandigarh',
            'Jaipur', 'Lucknow', 'Varanasi', 'Guwahati', 'Bhubaneswar',
            'Visakhapatnam', 'Vijayawada', 'Indore', 'Nagpur', 'Srinagar'
        ]
        
        # Clear existing data
        TravelOption.objects.all().delete()
        
        created_count = 0
        
        for i in range(count):
            # Random travel type
            travel_type = random.choice(travel_types)
            
            # Determine if this should be international (only for flights from major airports)
            is_international = False
            if travel_type == 'FLIGHT' and random.random() < 0.15:  # 15% international flights
                source = random.choice(international_airport_cities)
                if random.random() < 0.5:
                    # India to International
                    destination = random.choice(international_destinations)
                    is_international = True
                else:
                    # International to India
                    source, destination = random.choice(international_destinations), source
                    is_international = True
            
            if not is_international:
                # Domestic routes
                if travel_type == 'FLIGHT':
                    # Flights prefer tier 1 and tier 2 cities
                    available_cities = tier1_cities + tier2_cities + tier3_cities[:20]
                elif travel_type == 'TRAIN':
                    # Trains connect all cities
                    available_cities = all_indian_cities
                else:  # BUS
                    # Buses prefer shorter routes, mostly tier 2 and tier 3 cities
                    available_cities = tier1_cities + tier2_cities + tier3_cities
                
                source = random.choice(available_cities)
                destination = random.choice([city for city in available_cities if city != source])
            
            # Random dates (next 90 days)
            departure_date = timezone.now() + timedelta(days=random.randint(1, 90))
            
            # Random departure time based on transport type
            if travel_type == 'FLIGHT':
                departure_hour = random.choice([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
                departure_minute = random.choice([0, 15, 30, 45])
            elif travel_type == 'TRAIN':
                departure_hour = random.choice([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])
                departure_minute = random.choice([0, 15, 30, 45])
            else:  # BUS
                departure_hour = random.choice([6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
                departure_minute = random.choice([0, 30])
            
            departure_date = departure_date.replace(
                hour=departure_hour, 
                minute=departure_minute, 
                second=0, 
                microsecond=0
            )
            
            # Calculate duration and pricing based on travel type and route
            if travel_type == 'FLIGHT':
                if is_international:
                    # International flight durations
                    if destination in ['Dubai', 'Abu Dhabi', 'Sharjah', 'Doha', 'Kuwait City', 'Muscat']:
                        duration_hours = random.uniform(2.5, 4.5)
                        base_price = random.uniform(15000, 45000)
                    elif destination in ['Singapore', 'Bangkok', 'Kuala Lumpur']:
                        duration_hours = random.uniform(3.5, 6.0)
                        base_price = random.uniform(18000, 55000)
                    elif destination in ['London', 'Paris', 'Frankfurt']:
                        duration_hours = random.uniform(8.0, 11.0)
                        base_price = random.uniform(35000, 80000)
                    elif destination in ['New York', 'Los Angeles']:
                        duration_hours = random.uniform(14.0, 18.0)
                        base_price = random.uniform(45000, 120000)
                    else:
                        duration_hours = random.uniform(4.0, 12.0)
                        base_price = random.uniform(20000, 60000)
                    
                    total_seats = random.choice([150, 180, 200, 250, 300, 350])
                else:
                    # Domestic flight durations
                    duration_hours = random.uniform(1.0, 3.5)
                    base_price = random.uniform(3000, 15000)
                    total_seats = random.choice([150, 180, 200, 250])
            
            elif travel_type == 'TRAIN':
                # Train durations based on distance estimation
                duration_hours = random.uniform(2.0, 36.0)  # Up to 36 hours for long routes
                base_price = random.uniform(200, 3500)
                total_seats = random.choice([72, 100, 150, 200, 300])  # AC/Sleeper combinations
            
            else:  # BUS
                duration_hours = random.uniform(2.0, 18.0)
                base_price = random.uniform(300, 2500)
                total_seats = random.choice([35, 40, 45, 49, 53])  # Various bus sizes
            
            arrival_date = departure_date + timedelta(hours=duration_hours)
            
            # Add realistic price variation
            price = round(base_price * random.uniform(0.7, 1.4), 2)
            
            # Random availability (80-95% occupancy is common)
            occupancy_rate = random.uniform(0.05, 0.95)
            available_seats = max(1, int(total_seats * (1 - occupancy_rate)))
            
            # Generate travel ID
            if travel_type == 'FLIGHT':
                airline_codes = {
                    'IndiGo': '6E', 'Air India': 'AI', 'SpiceJet': 'SG', 'Vistara': 'UK',
                    'Emirates': 'EK', 'Qatar Airways': 'QR', 'Singapore Airlines': 'SQ'
                }
                operator_name = random.choice(operators[travel_type])
                code = airline_codes.get(operator_name, 'AI')
                travel_id = f"{code}{random.randint(100, 9999)}"
            elif travel_type == 'TRAIN':
                travel_id = f"{random.randint(10000, 99999)}"
            else:  # BUS
                travel_id = f"BUS{random.randint(1000, 9999)}"
            
            try:
                travel_option = TravelOption.objects.create(
                    travel_id=travel_id,
                    type=travel_type,
                    source=source,
                    destination=destination,
                    departure_date_time=departure_date,
                    arrival_date_time=arrival_date,
                    price=price,
                    available_seats=available_seats,
                    total_seats=total_seats,
                    operator=random.choice(operators[travel_type])
                )
                created_count += 1
                
                if created_count % 100 == 0:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created {created_count} travel options...')
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating travel option: {e}')
                )
                continue
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} travel options!'
            )
        )
        
        # Display statistics
        flights = TravelOption.objects.filter(type='FLIGHT').count()
        trains = TravelOption.objects.filter(type='TRAIN').count()
        buses = TravelOption.objects.filter(type='BUS').count()
        
        # Count international vs domestic flights
        international_flights = TravelOption.objects.filter(
            type='FLIGHT'
        ).exclude(
            destination__in=all_indian_cities
        ).count() + TravelOption.objects.filter(
            type='FLIGHT'
        ).exclude(
            source__in=all_indian_cities
        ).count()
        
        domestic_flights = flights - international_flights
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n=== TRAVEL OPTIONS SUMMARY ===\n'
                f'Total Options: {flights + trains + buses}\n\n'
                f'Flights: {flights}\n'
                f'  - Domestic: {domestic_flights}\n'
                f'  - International: {international_flights}\n\n'
                f'Trains: {trains}\n'
                f'Buses: {buses}\n\n'
                f'Coverage:\n'
                f'  - Indian Cities: {len(all_indian_cities)}\n'
                f'  - International Destinations: {len(international_destinations)}\n'
                f'  - Airlines: {len(operators["FLIGHT"])}\n'
                f'  - Train Services: {len(operators["TRAIN"])}\n'
                f'  - Bus Operators: {len(operators["BUS"])}'
            )
        )