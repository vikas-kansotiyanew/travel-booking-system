# Travel Booking Application

A Django-based web application for booking travel tickets (flights, trains, and buses) with user authentication, search functionality, and booking management.

## Live Demo

🌐 **Deployed Application**: https://travel-booking-system-28pq.onrender.com/

## Features

- **User Management**: Registration, login, logout, and profile management
- **Travel Options**: Browse flights, trains, and buses with search and filtering
- **Booking System**: Book tickets with passenger details and contact information
- **Booking Management**: View, track, and cancel bookings
- **Responsive Design**: Dark-themed UI with Bootstrap styling
- **Admin Panel**: Django admin interface for managing data

## File Structure

```
travel_booking_project/
├── .env                       # Environment variables
├── .gitignore                 # Git ignore file
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker compose setup
├── init.sql                   # Database initialization
├── requirements.txt           # Python dependencies
├── manage.py                  # Django management script
├── static/                    # Static files directory
├── media/                     # Media files directory
├── staticfiles/               # Collected static files
├── templates/                 # Global templates (if any)
├── travel_booking/            # Main project directory
│   ├── __init__.py
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
└── booking/                   # Main application
    ├── __init__.py
    ├── admin.py               # Admin interface configuration
    ├── apps.py                # App configuration
    ├── models.py              # Database models
    ├── views.py               # View functions
    ├── forms.py               # Django forms
    ├── urls.py                # App URL patterns
    ├── tests.py               # Unit tests
    ├── migrations/            # Database migrations
    ├── management/            # Custom management commands
    │   └── commands/
    │       └── populate_data.py # Sample data population
    └── templates/
        ├── base.html          # Base template (dark theme)
        └── booking/           # App-specific templates
            ├── home.html
            ├── register.html
            ├── login.html
            ├── profile.html
            ├── travel_options.html
            ├── travel_option_detail.html
            ├── book_travel.html
            ├── my_bookings.html
            ├── booking_detail.html
            └── cancel_booking.html
```

## Running with Docker

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd travel_booking
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   - Web App: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

4. **Populate sample data** (optional)
   ```bash
   docker-compose exec web python manage.py populate_data --count 100
   ```

## Traditional Setup

1. **Prerequisites**
   - Python 3.8+
   - PostgreSQL

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database setup**
   ```bash
   # Create PostgreSQL database
   createdb travel_booking_db
   
   # Set environment variables
   export DB_NAME=travel_booking_db
   export DB_USER=your_db_user
   export DB_PASSWORD=your_db_password
   export DB_HOST=localhost
   export DB_PORT=5432
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Populate sample data** (optional)
   ```bash
   python manage.py populate_data --count 100
   ```

## Default Access

- Application: http://localhost:8000
- Admin Panel: http://localhost:8000/admin (use created superuser credentials)

The application includes comprehensive travel data covering domestic and international routes with realistic pricing and scheduling.