from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.db import transaction
from datetime import datetime
from .models import TravelOption, Booking, UserProfile
from .forms import UserRegistrationForm, UserProfileForm, BookingForm, TravelSearchForm

def home(request):
    featured_options = TravelOption.objects.filter(
        departure_date_time__gte=timezone.now(),
        available_seats__gt=0
    )[:6]
    return render(request, 'booking/home.html', {'featured_options': featured_options})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome aboard!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'booking/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'booking/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Update User model fields
            request.user.first_name = request.POST.get('first_name', '')
            request.user.last_name = request.POST.get('last_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()
            
            # Save profile
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    recent_bookings = Booking.objects.filter(user=request.user)[:5]
    return render(request, 'booking/profile.html', {
        'form': form,
        'profile': profile,
        'recent_bookings': recent_bookings
    })

def travel_options(request):
    form = TravelSearchForm(request.GET)
    options = TravelOption.objects.filter(
        departure_date_time__gte=timezone.now(),
        available_seats__gt=0
    )
    
    # Search and filter functionality
    if form.is_valid():
        if form.cleaned_data.get('type'):
            options = options.filter(type=form.cleaned_data['type'])
        
        if form.cleaned_data.get('source'):
            options = options.filter(source__icontains=form.cleaned_data['source'])
        
        if form.cleaned_data.get('destination'):
            options = options.filter(destination__icontains=form.cleaned_data['destination'])
        
        if form.cleaned_data.get('date_from'):
            options = options.filter(departure_date_time__date__gte=form.cleaned_data['date_from'])
        
        if form.cleaned_data.get('date_to'):
            options = options.filter(departure_date_time__date__lte=form.cleaned_data['date_to'])
        
        if form.cleaned_data.get('max_price'):
            options = options.filter(price__lte=form.cleaned_data['max_price'])
        
        # Sorting
        sort_by = form.cleaned_data.get('sort_by')
        if sort_by == 'price_low':
            options = options.order_by('price')
        elif sort_by == 'price_high':
            options = options.order_by('-price')
        elif sort_by == 'departure':
            options = options.order_by('departure_date_time')
    
    # Pagination
    paginator = Paginator(options, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'booking/travel_options.html', {
        'page_obj': page_obj,
        'form': form,
        'total_count': paginator.count
    })

def travel_option_detail(request, pk):
    option = get_object_or_404(TravelOption, pk=pk)
    similar_options = TravelOption.objects.filter(
        source=option.source,
        destination=option.destination,
        departure_date_time__gte=timezone.now()
    ).exclude(pk=pk)[:3]
    
    return render(request, 'booking/travel_option_detail.html', {
        'option': option,
        'similar_options': similar_options
    })

@login_required
@transaction.atomic
def book_travel(request, pk):
    option = get_object_or_404(TravelOption, pk=pk)
    
    if not option.is_available:
        messages.error(request, 'This travel option is no longer available.')
        return redirect('travel_options')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, max_seats=option.available_seats)
        if form.is_valid():
            with transaction.atomic():
                booking = form.save(commit=False)
                booking.user = request.user
                booking.travel_option = option
                booking.total_price = option.price * booking.number_of_seats
                booking.status = 'CONFIRMED'
                booking.save()
                
                # Update available seats
                option.available_seats -= booking.number_of_seats
                option.save()
                
                messages.success(request, f'Booking {booking.booking_id} confirmed successfully!')
                return redirect('booking_detail', pk=booking.pk)
    else:
        initial = {
            'contact_email': request.user.email,
            'contact_phone': request.user.profile.phone if hasattr(request.user, 'profile') else ''
        }
        form = BookingForm(initial=initial, max_seats=option.available_seats)
    
    return render(request, 'booking/book_travel.html', {
        'form': form,
        'option': option
    })

@login_required
def my_bookings(request):
    status_filter = request.GET.get('status', '')
    bookings = Booking.objects.filter(user=request.user)
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    # Separate current and past bookings
    current_bookings = bookings.filter(
        travel_option__departure_date_time__gte=timezone.now(),
        status='CONFIRMED'
    )
    past_bookings = bookings.filter(
        Q(travel_option__departure_date_time__lt=timezone.now()) | Q(status='CANCELLED')
    )
    
    return render(request, 'booking/my_bookings.html', {
        'current_bookings': current_bookings,
        'past_bookings': past_bookings,
        'status_filter': status_filter
    })

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    # Split passenger names into a list
    passenger_names = [name.strip() for name in booking.passenger_names.split(',') if name.strip()]
    
    return render(request, 'booking/booking_detail.html', {
        'booking': booking,
        'passenger_names': passenger_names
    })

@login_required
@transaction.atomic
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if not booking.is_cancellable:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('booking_detail', pk=pk)
    
    if request.method == 'POST':
        with transaction.atomic():
            # Return seats to available pool
            booking.travel_option.available_seats += booking.number_of_seats
            booking.travel_option.save()
            
            # Update booking status
            booking.status = 'CANCELLED'
            booking.save()
            
            messages.success(request, f'Booking {booking.booking_id} has been cancelled successfully.')
            return redirect('my_bookings')
    
    return render(request, 'booking/cancel_booking.html', {'booking': booking})