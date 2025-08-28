from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('travel-options/', views.travel_options, name='travel_options'),
    path('travel-option/<int:pk>/', views.travel_option_detail, name='travel_option_detail'),
    path('book-travel/<int:pk>/', views.book_travel, name='book_travel'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('cancel-booking/<int:pk>/', views.cancel_booking, name='cancel_booking'),
]