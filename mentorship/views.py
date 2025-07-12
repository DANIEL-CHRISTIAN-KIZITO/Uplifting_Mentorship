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
