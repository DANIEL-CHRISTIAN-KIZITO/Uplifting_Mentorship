# mentorship/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required # Keep login_required here
from django.contrib.admin.views.decorators import staff_member_required # <--- CORRECTED IMPORT
from django.contrib import messages
from django.db.models import Q, Avg # Import Avg for analytics if needed
from django.core.mail import send_mail # For sending emails

from .models import MentorProfile, MenteeProfile, MentorshipRequest, MentorshipSession, MentorshipAssignment # Ensure MentorshipAssignment is imported

from accounts.models import User # Import your custom User model
# from .forms import MentorProfileForm, MenteeProfileForm, MentorshipRequestForm, MentorshipSessionForm, AssignMentorForm # You'll create these forms

# You might have a custom decorator in accounts/decorators.py
# from accounts.decorators import mentor_required # If you have this


@login_required
def mentor_list(request):
    # This will fetch all mentor profiles
    mentors = MentorProfile.objects.all()
    return render(request, 'mentorship/mentor_list.html', {'mentors': mentors})

@login_required
def mentor_detail(request, pk):
    mentor = get_object_or_404(MentorProfile, pk=pk)
    return render(request, 'mentorship/mentor_detail.html', {'mentor': mentor})

# FR7: Send request
@login_required
def request_mentorship(request, mentor_pk): # Correctly accepts mentor_pk
    mentor_profile = get_object_or_404(MentorProfile, pk=mentor_pk)
    mentor_user = mentor_profile.user # Get the User object related to the MentorProfile

    # Ensure the current user has a mentee profile. If not, create one.
    mentee_profile, created = MenteeProfile.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, "A mentee profile was created for you to proceed with the request.")

    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        if not message:
            messages.error(request, "Message cannot be empty.")
            return render(request, 'mentorship/request_mentorship.html', {'mentor': mentor_profile})

        # Check if a pending request already exists from this mentee to this mentor
        existing_request = MentorshipRequest.objects.filter(
            mentee=mentee_profile,
            mentor=mentor_profile, # Use mentor_profile here
            status='pending'
        ).exists()

        if existing_request:
            messages.warning(request, "You already have a pending mentorship request to this mentor.")
        else:
            MentorshipRequest.objects.create(mentee=mentee_profile, mentor=mentor_profile, message=message)
            messages.success(request, 'Mentorship request sent successfully!')

            # FR8: Email or in-app notification (simple email example)
            send_mail(
                'New Mentorship Request',
                f'Hi {mentor_user.username},\n\nYou have a new mentorship request from {request.user.username}.\nMessage: "{message}"\n\nPlease log in to manage your requests.',
                'admin@uplifting.com', # Your sender email
                [mentor_user.email], # Recipient email
                fail_silently=True,
            )
        return redirect(reverse('mentorship:mentor_detail', args=[mentor_pk]))

    return render(request, 'mentorship/request_mentorship.html', {'mentor': mentor_profile})


# FR9: Accept or reject mentorship requests
@login_required
def manage_requests(request):
    # Mentor's view to manage requests received
    mentor_profile = get_object_or_404(MentorProfile, user=request.user)
    requests = MentorshipRequest.objects.filter(mentor=mentor_profile).order_by('-created_at')
    return render(request, 'mentorship/manage_requests.html', {'requests': requests})

@login_required
def update_request_status(request, request_id, action):
    mentorship_request = get_object_or_404(MentorshipRequest, id=request_id)

    # Ensure only the mentor who received the request can update its status
    try:
        mentor_profile = MentorProfile.objects.get(user=request.user)
    except MentorProfile.DoesNotExist:
        messages.error(request, "You must be a mentor to manage requests.")
        return redirect(reverse('accounts:dashboard')) # Or appropriate redirect

    if mentorship_request.mentor != mentor_profile:
        messages.error(request, "You are not authorized to manage this request.")
        return redirect(reverse('mentorship:manage_requests'))

    if action in ['accept', 'reject']:
        mentorship_request.status = 'accepted' if action == 'accept' else 'rejected'
        mentorship_request.save()
        messages.success(request, f'Request {action}ed successfully.')

        # Optional: Notify mentee about status change
        mentee_user = mentorship_request.mentee.user
        send_mail(
            f'Mentorship Request {action.capitalize()}ed',
            f'Hi {mentee_user.username},\n\nYour mentorship request to {request.user.username} has been {action}ed.',
            'admin@uplifting.com',
            [mentee_user.email],
            fail_silently=True,
        )
    else:
        messages.error(request, "Invalid action.")

    return redirect(reverse('mentorship:manage_requests'))


# Admin/Staff view to assign mentors (assuming MentorshipAssignment model exists)
# If MentorshipAssignment model doesn't exist, remove this section.
# You'd also need AssignMentorForm in mentorship/forms.py
@staff_member_required
def assign_mentor(request):
    # Ensure MentorshipAssignment is imported at the top
    # from .models import MentorshipAssignment
    # from .forms import AssignMentorForm # You need to create this form
    messages.info(request, "Assign Mentor view is a placeholder. Implement form and logic.")
    return render(request, 'mentorship/assign_mentor.html', {}) # Render a simple template for now

def assign_success(request):
    return render(request, 'mentorship/assign_success.html')

# Mentor's view to see their mentees
@login_required
def my_mentees_view(request):
    user = request.user
    try:
        mentor_profile = MentorProfile.objects.get(user=user)
    except MentorProfile.DoesNotExist:
        messages.error(request, "You must have a mentor profile to view your mentees.")
        return redirect(reverse('accounts:dashboard'))

    assignments = MentorshipAssignment.objects.filter(mentor=mentor_profile) # <--- CRUCIAL FIX HERE
    return render(request, 'mentorship/my_mentees.html', {'assignments': assignments})


@login_required
def mentee_dashboard(request):
    mentee_profile = get_object_or_404(MenteeProfile, user=request.user)
    requests = MentorshipRequest.objects.filter(mentee=mentee_profile).order_by('-created_at')
    sessions = MentorshipSession.objects.filter(mentee=mentee_profile).order_by('-start_time')

    # NEW: Fetch the mentee's current assignment
    assigned_mentor = None
    try:
        # Assuming a mentee has only one active assignment (OneToOneField)
        current_assignment = MentorshipAssignment.objects.get(mentee=mentee_profile)
        assigned_mentor = current_assignment.mentor # This is a MentorProfile object
    except MentorshipAssignment.DoesNotExist:
        pass # No mentor assigned yet

    context = {
        'mentee_profile': mentee_profile,
        'requests': requests,
        'sessions': sessions,
        'assigned_mentor': assigned_mentor, # Pass the assigned mentor to the template
    }
    return render(request, 'mentorship/mentee_dashboard.html', context)


# Consolidated Mentor Search View
@login_required
def search_mentors(request):
    query = request.GET.get('q', '').strip()
    expertise_filter = request.GET.get('expertise', '').strip()

    # Start with all available mentors
    mentors = MentorProfile.objects.filter(available_for_mentorship=True)

    if query:
        # Search by username (on User model) or expertise (on MentorProfile model)
        mentors = mentors.filter(
            Q(user__username__icontains=query) |
            Q(expertise__icontains=query)
        ).distinct()

    if expertise_filter:
        # Further filter by expertise
        mentors = mentors.filter(expertise__icontains=expertise_filter)

    # Order by username for consistent display
    mentors = mentors.order_by('user__username')

    return render(request, 'mentorship/search_mentors.html', {'mentors': mentors, 'query': query, 'expertise_filter': expertise_filter})

