# mentorship/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MentorProfile, MenteeProfile, MentorshipRequest, MentorshipSession
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

# Add other views like mentor_dashboard, session_detail, etc.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Q
from .models import MentorshipRequest
from accounts.models import User

# FR6: Search mentors
@login_required
def search_mentors(request):
    query = request.GET.get('q') # Get the search query from the URL parameter 'q'
    expertise_filter = request.GET.get('expertise') # Get expertise filter

    mentors = MentorProfile.objects.filter(available_for_mentorship=True)

    if query:
        # Search by username or expertise in the MentorProfile
        mentors = mentors.filter(
            Q(user__username__icontains=query) | # Search username on User model
            Q(expertise__icontains=query) # Search expertise on MentorProfile model
        ).distinct() # Use distinct to avoid duplicate mentors if they match multiple criteria

    if expertise_filter:
        mentors = mentors.filter(expertise__icontains=expertise_filter)

    # You can also order them, e.g., by username
    mentors = mentors.order_by('user__username') # Order by username on the related User model

    return render(request, 'mentorship/search_mentors.html', {'mentors': mentors, 'query': query, 'expertise_filter': expertise_filter})



# FR7: Send request
@login_required
def request_mentorship(request, mentor_id):
    mentor = get_object_or_404(User, id=mentor_id, role='mentor')
    if request.method == 'POST':
        message = request.POST.get('message', '')
        MentorshipRequest.objects.create(
            mentee=request.user,
            mentor=mentor,
            message=message
        )
        # FR8: Email or in-app notification (simple email example)
        send_mail(
            'New Mentorship Request',
            f'Hi {mentor.username}, you have a new mentorship request from {request.user.username}.',
            'admin@uplifting.com',
            [mentor.email],
            fail_silently=True,
        )
        messages.success(request, 'Mentorship request sent!')
        return redirect('dashboard')
    return render(request, 'mentorship/request_form.html', {'mentor': mentor})

# FR9: Accept or reject
@login_required
def manage_requests(request):
    requests = MentorshipRequest.objects.filter(mentor=request.user)
    return render(request, 'mentorship/manage_requests.html', {'requests': requests})

@login_required
def update_request_status(request, request_id, action):
    mentorship_request = get_object_or_404(MentorshipRequest, id=request_id, mentor=request.user)
    if action in ['accept', 'reject']:
        mentorship_request.status = 'accepted' if action == 'accept' else 'rejected'
        mentorship_request.save()
        messages.success(request, f'Request {action}ed successfully.')
    return redirect('manage_requests')
