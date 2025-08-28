from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import TravelOption, Booking, UserProfile

class TravelBookingTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        UserProfile.objects.create(user=self.user)
        
        self.travel_option = TravelOption.objects.create(
            travel_id='T1234',
            type='FLIGHT',
            source='New York',
            destination='Los Angeles',
            departure_date_time=timezone.now() + timedelta(days=7),
            arrival_date_time=timezone.now() + timedelta(days=7, hours=5),
            price=299.99,
            available_seats=150,
            total_seats=200,
            operator='Test Airlines'
        )

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_travel_options_page(self):
        response = self.client.get(reverse('travel_options'))
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123',
            'confirm_password': 'newpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration

    def test_booking_creation(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('book_travel', args=[self.travel_option.pk]), {
            'number_of_seats': 2,
            'passenger_names': 'John Doe, Jane Doe',
            'contact_email': 'test@example.com',
            'contact_phone': '1234567890'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful booking
        self.assertTrue(Booking.objects.filter(user=self.user).exists())