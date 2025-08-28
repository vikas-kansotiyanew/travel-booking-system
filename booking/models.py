from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class TravelOption(models.Model):
    TRAVEL_TYPES = [
        ('FLIGHT', 'Flight'),
        ('TRAIN', 'Train'),
        ('BUS', 'Bus'),
    ]
    
    travel_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=10, choices=TRAVEL_TYPES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_date_time = models.DateTimeField()
    arrival_date_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    available_seats = models.PositiveIntegerField()
    total_seats = models.PositiveIntegerField()
    operator = models.CharField(max_length=100, default='Default Operator')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['departure_date_time']
    
    def __str__(self):
        return f"{self.travel_id} - {self.type} from {self.source} to {self.destination}"
    
    @property
    def is_available(self):
        return self.available_seats > 0 and self.departure_date_time > timezone.now()
    
    @property
    def duration(self):
        delta = self.arrival_date_time - self.departure_date_time
        hours = delta.total_seconds() // 3600
        minutes = (delta.total_seconds() % 3600) // 60
        return f"{int(hours)}h {int(minutes)}m"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('PENDING', 'Pending'),
    ]
    
    booking_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    travel_option = models.ForeignKey(TravelOption, on_delete=models.CASCADE, related_name='bookings')
    number_of_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    passenger_names = models.TextField(help_text="Comma-separated passenger names")
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    
    class Meta:
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            import random
            import string
            self.booking_id = 'BK' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        if not self.total_price:
            self.total_price = self.travel_option.price * self.number_of_seats
        
        super().save(*args, **kwargs)
    
    @property
    def is_cancellable(self):
        return self.status == 'CONFIRMED' and self.travel_option.departure_date_time > timezone.now()