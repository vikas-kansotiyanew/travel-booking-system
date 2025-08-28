from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, Booking, TravelOption

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already registered')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Passwords do not match')
        
        if password and len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'date_of_birth']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats', 'passenger_names', 'contact_email', 'contact_phone']
        widgets = {
            'number_of_seats': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'passenger_names': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter passenger names separated by commas'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        max_seats = kwargs.pop('max_seats', 10)
        super().__init__(*args, **kwargs)
        self.fields['number_of_seats'].widget.attrs['max'] = max_seats
    
    def clean_number_of_seats(self):
        seats = self.cleaned_data.get('number_of_seats')
        if seats <= 0:
            raise ValidationError('Number of seats must be at least 1')
        return seats
    
    def clean_contact_phone(self):
        phone = self.cleaned_data.get('contact_phone')
        if phone and len(phone) < 10:
            raise ValidationError('Please enter a valid phone number')
        return phone

class TravelSearchForm(forms.Form):
    SORT_CHOICES = [
        ('', 'Sort By'),
        ('price_low', 'Price: Low to High'),
        ('price_high', 'Price: High to Low'),
        ('departure', 'Departure Time'),
    ]
    
    type = forms.ChoiceField(
        choices=[('', 'All Types')] + TravelOption.TRAVEL_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    source = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'From'})
    )
    destination = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'To'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Price'})
    )
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )