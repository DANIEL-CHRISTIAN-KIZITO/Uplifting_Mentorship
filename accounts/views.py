from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm
from .models import User # Import your custom User model

# Registration View
def register(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect(reverse('accounts:dashboard')) # Redirect if already logged in

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES) # Include request.FILES for ImageField
        if form.is_valid():
            user = form.save()
            # Optionally log the user in immediately after registration
            # login(request, user)
            messages.success(request, 'Registration successful! Please log in.')
            return redirect(reverse('accounts:login'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login View
def user_login(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect(reverse('accounts:dashboard')) # Redirect if already logged in

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST) # AuthenticationForm expects request as first arg
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_url = request.GET.get('next', reverse('accounts:dashboard'))
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        # If form is not valid, errors are automatically attached to form.errors
    else:
        form = UserLoginForm() # Empty form for GET request

    return render(request, 'accounts/login.html', {'form': form})

# Logout View
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect(reverse('accounts:login')) # Redirect to login page after logout

# Dashboard View (requires login)
@login_required
def dashboard(request):
    # Access user-specific data here
    user_role = request.user.role if hasattr(request.user, 'role') else 'N/A'
    user_photo_url = request.user.photo.url if request.user.photo else None

    context = {
        'username': request.user.username,
        'user_role': user_role,
        'user_photo_url': user_photo_url,
        'receive_notifications': request.user.receive_notifications,
        'profile_visibility': request.user.profile_visibility,
        # Add more data as needed for your dashboard
    }
    return render(request, 'dashboard/dashboard.html', context) # Note: this renders a template in dashboard app
