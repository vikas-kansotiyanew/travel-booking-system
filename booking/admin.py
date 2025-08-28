from django.contrib import admin
from .models import UserProfile, TravelOption, Booking

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ['created_at', 'updated_at']

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ['travel_id', 'type', 'source', 'destination', 'departure_date_time', 'price', 'available_seats']
    list_filter = ['type', 'departure_date_time', 'source', 'destination']
    search_fields = ['travel_id', 'source', 'destination', 'operator']
    ordering = ['departure_date_time']
    
    fieldsets = (
        (None, {
            'fields': ('travel_id', 'type', 'operator')
        }),
        ('Route Information', {
            'fields': ('source', 'destination', 'departure_date_time', 'arrival_date_time')
        }),
        ('Pricing & Availability', {
            'fields': ('price', 'available_seats', 'total_seats')
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'travel_option', 'number_of_seats', 'total_price', 'status', 'booking_date']
    list_filter = ['status', 'booking_date']
    search_fields = ['booking_id', 'user__username', 'contact_email', 'contact_phone']
    readonly_fields = ['booking_id', 'booking_date', 'total_price']
    
    fieldsets = (
        (None, {
            'fields': ('booking_id', 'user', 'travel_option', 'status')
        }),
        ('Booking Details', {
            'fields': ('number_of_seats', 'total_price', 'passenger_names')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Timestamps', {
            'fields': ('booking_date',)
        }),
    )