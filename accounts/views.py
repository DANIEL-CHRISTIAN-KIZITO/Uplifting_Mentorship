from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q # <--- Ensure Q is imported for complex lookups
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm
from .models import User
from mentorship.models import MenteeProfile, MentorProfile, MentorshipRequest, MentorshipSession, MentorshipAssignment # <--- MentorshipAssignment now imported
from chat.models import ChatRoom, Message
from progress.models import Goal, ProgressUpdate # <--- ADDED PROGRESS MODELS IMPORT

# Django signals for superuser role (can be moved to signals.py or apps.py ready method)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save, sender=User)
def set_role_for_superuser(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        instance.role = 'admin'
        instance.save()

# Registration View
def register(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect(reverse('accounts:dashboard'))

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
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
        return redirect(reverse('accounts:dashboard'))

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
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
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

# Logout View
def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect(reverse('accounts:login'))

# Public Home Page View
def dashboard_home(request):
    if request.user.is_authenticated:
        return redirect(reverse('accounts:dashboard'))
    else:
        return render(request, 'dashboard_home.html')

# Main Authenticated Dashboard View
@login_required
def dashboard(request):
    user_role = request.user.role if hasattr(request.user, 'role') else 'N/A'
    user_photo_url = request.user.photo.url if request.user.photo else None

    mentorship_summary = {}
    chat_summary = {}
    progress_summary = {} # <--- NEW: Progress Summary

    # Calculate unread messages for the current user
    user_chat_rooms = ChatRoom.objects.filter(Q(participant1=request.user) | Q(participant2=request.user))
    total_unread_messages = Message.objects.filter(
        chat_room__in=user_chat_rooms,
        is_read=False
    ).exclude(sender=request.user).count()
    chat_summary['total_unread_messages'] = total_unread_messages
    chat_summary['chat_rooms_count'] = user_chat_rooms.count()

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

            # Progress Summary Logic for mentee
            total_goals = Goal.objects.filter(user=request.user).count()
            completed_goals = Goal.objects.filter(user=request.user, is_completed=True).count()
            progress_summary['total_goals'] = total_goals
            progress_summary['completed_goals'] = completed_goals
            progress_summary['goals_in_progress'] = total_goals - completed_goals

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
            # For mentors, also count goals of their assigned mentees
            # Corrected lookup: use 'current_assignment' which is the related_name for the OneToOneField from MentorshipAssignment to MenteeProfile
            assigned_mentees_for_mentor = MenteeProfile.objects.filter(current_assignment__mentor=mentor_profile) # <--- CORRECTED THIS LINE
            progress_summary['mentees_total_goals'] = Goal.objects.filter(user__in=[m.user for m in assigned_mentees_for_mentor]).count()
            progress_summary['mentees_completed_goals'] = Goal.objects.filter(user__in=[m.user for m in assigned_mentees_for_mentor], is_completed=True).count()
            progress_summary['mentees_goals_in_progress'] = progress_summary['mentees_total_goals'] - progress_summary['mentees_completed_goals']

        except MentorProfile.DoesNotExist:
            mentorship_summary['is_mentor'] = False
            messages.info(request, "You don't have a mentor profile yet. Create one to access mentor features.")
    else: # For users with no specific role (or admin)
        # Initialize progress summary for other roles to avoid KeyError in template
        progress_summary['total_goals'] = 0
        progress_summary['completed_goals'] = 0
        progress_summary['goals_in_progress'] = 0
        # Also initialize mentor-specific progress summary keys if they might be accessed
        progress_summary['mentees_total_goals'] = 0
        progress_summary['mentees_completed_goals'] = 0
        progress_summary['mentees_goals_in_progress'] = 0


    context = {
        'username': request.user.username,
        'user_role': user_role,
        'user_photo_url': user_photo_url,
        'receive_notifications': request.user.receive_notifications,
        'profile_visibility': request.user.profile_visibility,
        'mentorship_summary': mentorship_summary,
        'chat_summary': chat_summary,
        'progress_summary': progress_summary, # <--- NEW: Pass progress summary
    }
    return render(request, 'dashboard/dashboard.html', context)

# --- Profile Management Views ---
@login_required
def profile_detail(request):
    return render(request, 'accounts/profile_detail.html', {'user': request.user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('accounts:dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/update_profile.html', {'form': form})
