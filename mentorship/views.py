# mentorship/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models # Import models for Q objects
from .models import MentorProfile, MenteeProfile, MentorshipRequest, MentorshipSession, MentorshipAssignment # <--- ADDED MentorshipAssignment
# from .forms import MentorProfileForm, MenteeProfileForm, MentorshipRequestForm, MentorshipSessionForm # You'll create these

@login_required
def mentor_list(request):
    mentors = MentorProfile.objects.filter(available_for_mentorship=True)
    return render(request, 'mentorship/mentor_list.html', {'mentors': mentors})

@login_required
def mentor_detail(request, pk):
    mentor = get_object_or_404(MentorProfile, pk=pk)
    return render(request, 'mentorship/mentor_detail.html', {'mentor': mentor})

@login_required
def request_mentorship(request, mentor_pk):
    mentor = get_object_or_404(MentorProfile, pk=mentor_pk)
    mentee_profile = get_object_or_404(MenteeProfile, user=request.user)
    # This is a placeholder; you'd use a form here
    if request.method == 'POST':
        message = request.POST.get('message', 'No message provided.')
        MentorshipRequest.objects.create(mentee=mentee_profile, mentor=mentor, message=message)
        messages.success(request, 'Mentorship request sent successfully!')
        return redirect(reverse('mentorship:mentor_detail', args=[mentor_pk]))
    return render(request, 'mentorship/request_mentorship.html', {'mentor': mentor})

@login_required
def mentee_dashboard(request):
    mentee_profile = get_object_or_404(MenteeProfile, user=request.user)
    requests = MentorshipRequest.objects.filter(mentee=mentee_profile)
    sessions = MentorshipSession.objects.filter(mentee=mentee_profile)
    return render(request, 'mentorship/mentee_dashboard.html', {'mentee_profile': mentee_profile, 'requests': requests, 'sessions': sessions})

@login_required
def search_mentors(request):
    query = request.GET.get('q') # Get the search query from the URL parameter 'q'
    expertise_filter = request.GET.get('expertise') # Get expertise filter

    mentors = MentorProfile.objects.filter(available_for_mentorship=True)

    if query:
        # Search by username or expertise in the MentorProfile
        mentors = mentors.filter(
            models.Q(user__username__icontains=query) | # Search username on User model
            models.Q(expertise__icontains=query) # Search expertise on MentorProfile model
        ).distinct() # Use distinct to avoid duplicate mentors if they match multiple criteria

    if expertise_filter:
        mentors = mentors.filter(expertise__icontains=expertise_filter)

    # You can also order them, e.g., by username
    mentors = mentors.order_by('user__username') # Order by username on the related User model

    return render(request, 'mentorship/search_mentors.html', {'mentors': mentors, 'query': query, 'expertise_filter': expertise_filter})

# Add other views like mentor_dashboard, session_detail, etc.
@login_required
def my_mentees(request):
    """
    Displays a list of mentees assigned to the current mentor.
    """
    mentor_profile = get_object_or_404(MentorProfile, user=request.user)
    # Get MenteeProfile objects through MentorshipAssignment
    assigned_mentees = MenteeProfile.objects.filter(current_assignment__mentor=mentor_profile)

    context = {
        'assigned_mentees': assigned_mentees,
    }
    return render(request, 'mentorship/my_mentees.html', context)

@login_required
def manage_requests(request):
    """
    Mentors can manage incoming mentorship requests.
    """
    mentor_profile = get_object_or_404(MentorProfile, user=request.user)
    received_requests = MentorshipRequest.objects.filter(mentor=mentor_profile, status='pending').order_by('-created_at')

    context = {
        'received_requests': received_requests,
    }
    return render(request, 'mentorship/manage_requests.html', context)

@login_required
def respond_to_request(request, request_pk, action):
    """
    Mentor responds to a mentorship request (accept/reject).
    """
    mentorship_request = get_object_or_404(MentorshipRequest, pk=request_pk, mentor__user=request.user)

    if action == 'accept':
        mentorship_request.status = 'accepted'
        mentorship_request.save()
        # Create a MentorshipAssignment when a request is accepted
        MentorshipAssignment.objects.get_or_create(
            mentee=mentorship_request.mentee,
            mentor=mentorship_request.mentor
        )
        messages.success(request, f"Mentorship request from {mentorship_request.mentee.user.username} accepted. An assignment has been created!")
    elif action == 'reject':
        mentorship_request.status = 'rejected'
        mentorship_request.save()
        messages.info(request, f"Mentorship request from {mentorship_request.mentee.user.username} rejected.")
    else:
        messages.error(request, "Invalid action.")

    return redirect(reverse('mentorship:manage_requests'))
