from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm # <--- ProfileUpdateForm UNCOMMENTED
from .models import User # Import your custom User model
from mentorship.models import MenteeProfile, MentorProfile, MentorshipRequest, MentorshipSession, MentorshipAssignment # Import mentorship models

# Django signals for superuser role (can be moved to signals.py or apps.py ready method)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model() # Re-get User model for signal

@receiver(post_save, sender=User)
def set_role_for_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        instance.role = 'admin'
        instance.save()

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
    return redirect(reverse('accounts:login')) # Changed to login for clarity

# Public Home Page View (if not authenticated, shows a welcome; if authenticated, redirects to dashboard)
def dashboard_home(request):
    if request.user.is_authenticated:
        return redirect(reverse('accounts:dashboard'))  # Redirect to dashboard if logged in
    else:
        # This template should be in your project's base templates directory (e.g., templates/dashboard_home.html)
        return render(request, 'dashboard_home.html') # Ensure this template exists and is public

# Main Authenticated Dashboard View
@login_required
def dashboard(request):
    user_role = request.user.role if hasattr(request.user, 'role') else 'N/A'
    user_photo_url = request.user.photo.url if request.user.photo else None

    mentorship_summary = {}

    if user_role == 'mentee':
        try:
            mentee_profile = MenteeProfile.objects.get(user=request.user)
            mentorship_summary['is_mentee'] = True
            mentorship_summary['pending_requests_count'] = MentorshipRequest.objects.filter(
                mentee=mentee_profile, status='pending'
            ).count()
            mentorship_summary['accepted_requests_count'] = MentorshipRequest.objects.filter(
                mentee=mentee_profile, status='accepted'
            ).count()
            mentorship_summary['assigned_mentor'] = None
            try:
                assigned_assignment = MentorshipAssignment.objects.get(mentee=mentee_profile)
                mentorship_summary['assigned_mentor'] = assigned_assignment.mentor
            except MentorshipAssignment.DoesNotExist:
                pass
            mentorship_summary['upcoming_sessions_count'] = MentorshipSession.objects.filter(
                mentee=mentee_profile, start_time__gte=timezone.now(), is_completed=False
            ).count()
            mentorship_summary['completed_sessions_count'] = MentorshipSession.objects.filter(
                mentee=mentee_profile, is_completed=True
            ).count()
        except MenteeProfile.DoesNotExist:
            mentorship_summary['is_mentee'] = False
            messages.info(request, "You don't have a mentee profile yet. Create one to access mentee features.")

    elif user_role == 'mentor':
        try:
            mentor_profile = MentorProfile.objects.get(user=request.user)
            mentorship_summary['is_mentor'] = True
            mentorship_summary['received_pending_requests_count'] = MentorshipRequest.objects.filter(
                mentor=mentor_profile, status='pending'
            ).count()
            mentorship_summary['assigned_mentees_count'] = MentorshipAssignment.objects.filter(
                mentor=mentor_profile
            ).count()
            mentorship_summary['upcoming_sessions_count'] = MentorshipSession.objects.filter(
                mentor=mentor_profile, start_time__gte=timezone.now(), is_completed=False
            ).count()
            mentorship_summary['completed_sessions_count'] = MentorshipSession.objects.filter(
                mentor=mentor_profile, is_completed=True
            ).count()
        except MentorProfile.DoesNotExist:
            mentorship_summary['is_mentor'] = False
            messages.info(request, "You don't have a mentor profile yet. Create one to access mentor features.")

    context = {
        'username': request.user.username,
        'user_role': user_role,
        'user_photo_url': user_photo_url,
        'receive_notifications': request.user.receive_notifications,
        'profile_visibility': request.user.profile_visibility,
        'mentorship_summary': mentorship_summary, # Pass the summary to the template
    }
    # This renders a template in dashboard app, which is appropriate for the main dashboard
    return render(request, 'dashboard/dashboard.html', context)

# --- Profile Management Views (UNCOMMENTED) ---
@login_required
def profile_detail(request):
    return render(request, 'accounts/profile_detail.html', {'user': request.user})

@login_required
def update_profile(request):
    # ProfileUpdateForm is now imported at the top
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/update_profile.html', {'form': form})
