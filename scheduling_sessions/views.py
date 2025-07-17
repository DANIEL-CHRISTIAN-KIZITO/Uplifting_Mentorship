# scheduling_sessions/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction # For atomic operations
from django.core.mail import send_mail # For notifications
from django.utils import timezone # For handling time-related queries

# Correct imports for models:
from .models import SessionSlot, Booking, SessionProposal # These are in scheduling_sessions/models.py
from mentorship.models import MentorProfile, MenteeProfile, MentorshipSession, MentorshipAssignment # These are in mentorship/models.py, ensure MentorshipAssignment is imported

from .forms import SessionProposalForm, SessionProposalResponseForm


@login_required
def available_slots(request):
    # Changed to filter for *available* (unbooked) slots
    slots = SessionSlot.objects.filter(is_booked=False).order_by('start_time')
    return render(request, 'scheduling_sessions/available_slots.html', {'slots': slots})

@login_required
def book_slot(request, slot_pk):
    slot = get_object_or_404(SessionSlot, pk=slot_pk, is_booked=False)
    # Ensure mentee profile exists
    mentee_profile, created = MenteeProfile.objects.get_or_create(user=request.user)
    if created:
        messages.info(request, "A mentee profile was created for you to book a session.")

    if request.method == 'POST':
        with transaction.atomic(): # Ensure atomicity
            if not slot.is_booked: # Double check to prevent race conditions
                Booking.objects.create(session_slot=slot, mentee=mentee_profile, status='confirmed')
                slot.is_booked = True
                slot.save()

                # Also create a MentorshipSession when a slot is booked directly
                # You might need a way to get the topic/notes here, or or use a default
                MentorshipSession.objects.create(
                    mentee=mentee_profile,
                    mentor=slot.mentor,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    topic=f"Directly Booked Session with {slot.mentor.user.username}", # Default topic
                    notes="This session was booked directly from an available slot."
                )

                messages.success(request, 'Session booked successfully!')

                # Send notification to mentor
                send_mail(
                    'New Session Booking',
                    f'Hi {slot.mentor.user.username},\n\nYour session slot on {slot.start_time.strftime("%Y-%m-%d %H:%M")} has been booked by {request.user.username}.',
                    'admin@uplifting.com',
                    [slot.mentor.user.email],
                    fail_silently=True,
                )
                return redirect(reverse('scheduling_sessions:my_bookings'))
            else:
                messages.error(request, "This slot is already booked.")
                return redirect(reverse('scheduling_sessions:available_slots'))
    return render(request, 'scheduling_sessions/book_slot.html', {'slot': slot})

@login_required
def my_bookings(request):
    # Get mentee profile or redirect
    try:
        mentee_profile = MenteeProfile.objects.get(user=request.user)
    except MenteeProfile.DoesNotExist:
        messages.info(request, "You don't have a mentee profile yet.")
        return render(request, 'scheduling_sessions/my_bookings.html', {'bookings': []}) # Render empty list

    bookings = Booking.objects.filter(mentee=mentee_profile).order_by('session_slot__start_time')
    return render(request, 'scheduling_sessions/my_bookings.html', {'bookings': bookings})


# --- PROPOSAL AND CONFIRMATION VIEWS ---

@login_required
def propose_session(request, mentor_pk=None):
    current_mentee_profile = None # Renamed for clarity
    current_mentor_profile = None # Renamed for clarity
    target_mentor_profile = None # The mentor for the proposal
    target_mentee_profile = None # The mentee for the proposal (if mentor is proposing)

    is_mentee_user = False
    is_mentor_user = False

    # Initialize mentees_for_proposal to None
    mentees_for_proposal = None # <--- INITIALIZED HERE

    # Determine if current user is mentee or mentor
    try:
        current_mentee_profile = MenteeProfile.objects.get(user=request.user)
        is_mentee_user = True
    except MenteeProfile.DoesNotExist:
        try:
            current_mentor_profile = MentorProfile.objects.get(user=request.user)
            is_mentor_user = True
        except MentorProfile.DoesNotExist:
            messages.error(request, "You must have a mentee or mentor profile to propose sessions.")
            return redirect(reverse('accounts:dashboard'))

    # Determine the target for the proposal (GET request logic)
    if is_mentee_user:
        # User is a mentee
        try:
            # Check if mentee has an assigned mentor
            assignment = MentorshipAssignment.objects.get(mentee=current_mentee_profile)
            assigned_mentor = assignment.mentor
            
            if mentor_pk:
                # If a specific mentor_pk is provided in the URL, use that mentor
                # This allows a mentee to propose to someone other than their assigned mentor
                target_mentor_profile = get_object_or_404(MentorProfile, pk=mentor_pk)
                if target_mentor_profile != assigned_mentor:
                    messages.info(request, f"You are proposing to {target_mentor_profile.user.username} (different from your assigned mentor).")
            else:
                # If no specific mentor_pk, default to the assigned mentor
                target_mentor_profile = assigned_mentor
                messages.info(request, f"Proposing to your assigned mentor: {target_mentor_profile.user.username}.")

        except MentorshipAssignment.DoesNotExist:
            # Mentee has no assigned mentor, so mentor_pk MUST be provided in URL
            if mentor_pk:
                target_mentor_profile = get_object_or_404(MentorProfile, pk=mentor_pk)
            else:
                messages.warning(request, "Please select a mentor to propose a session to.")
                return redirect(reverse('mentorship:mentor_list'))
    elif is_mentor_user:
        # User is a mentor, they will select a mentee from a dropdown in the form
        if mentor_pk: # Mentor should not have mentor_pk in URL for proposing to mentee
            messages.error(request, "Invalid URL for mentor-initiated proposal.")
            return redirect(reverse('accounts:dashboard'))
        # For GET request, prepare list of mentees for the form
        mentees_for_proposal = MenteeProfile.objects.all() # Or filter by assigned mentees if applicable


    if request.method == 'POST':
        form = SessionProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.proposed_by = request.user

            if is_mentee_user:
                # Mentee's proposal
                proposal.mentee = current_mentee_profile
                proposal.mentor = target_mentor_profile # Use the mentor determined in GET logic
            elif is_mentor_user:
                # Mentor's proposal
                mentee_pk_from_form = request.POST.get('mentee_pk')
                if not mentee_pk_from_form:
                    messages.error(request, "Please select a mentee to propose to.")
                    # Re-render form with error
                    mentees_for_proposal = MenteeProfile.objects.all() # Re-fetch for re-render
                    return render(request, 'scheduling_sessions/propose_session.html', {
                        'form': form,
                        'mentees_for_proposal': mentees_for_proposal,
                        'is_mentor_proposing': is_mentor_user
                    })
                target_mentee_profile = get_object_or_404(MenteeProfile, pk=mentee_pk_from_form)
                proposal.mentee = target_mentee_profile
                proposal.mentor = current_mentor_profile
            else:
                # This 'else' block means it's a POST request, but the user type couldn't be determined
                messages.error(request, "Invalid proposal context during submission.")
                return redirect(reverse('accounts:dashboard'))

            proposal.save()
            messages.success(request, 'Session proposal sent successfully!')

            # Send notification to the recipient
            recipient_user = proposal.mentor.user if is_mentee_user else proposal.mentee.user
            send_mail(
                'New Session Proposal',
                f'Hi {recipient_user.username},\n\nYou have a new session proposal from {request.user.username} for {proposal.proposed_start_time.strftime("%Y-%m-%d %H:%M")}.',
                'admin@uplifting.com',
                [recipient_user.email],
                fail_silently=True,
            )
            return redirect(reverse('scheduling_sessions:my_proposals'))
    else: # GET request
        form = SessionProposalForm()
        # Context variables for the template are handled by the logic above
        # No need for extra redirects here, as the target mentor/mentee is already determined
        pass # Logic for setting mentor_profile/mentees_for_proposal is above

    # Final render for both GET and POST (if form invalid)
    return render(request, 'scheduling_sessions/propose_session.html', {
        'form': form,
        'mentor': target_mentor_profile, # This will be None if mentor is proposing
        'is_mentee_proposing': is_mentee_user,
        'is_mentor_proposing': is_mentor_user,
        'mentees_for_proposal': mentees_for_proposal # This will be None if mentee is proposing
    })


@login_required
def my_proposals(request):
    sent_proposals = SessionProposal.objects.none()
    received_proposals = SessionProposal.objects.none()

    try:
        mentee_profile = MenteeProfile.objects.get(user=request.user)
        sent_proposals = SessionProposal.objects.filter(mentee=mentee_profile).order_by('-created_at')
    except MenteeProfile.DoesNotExist:
        pass

    try:
        mentor_profile = MentorProfile.objects.get(user=request.user)
        received_proposals = SessionProposal.objects.filter(mentor=mentor_profile).order_by('-created_at')
    except MentorProfile.DoesNotExist:
        pass

    context = {
        'sent_proposals': sent_proposals,
        'received_proposals': received_proposals,
    }
    return render(request, 'scheduling_sessions/my_proposals.html', context)


@login_required
def respond_to_proposal(request, proposal_pk):
    proposal = get_object_or_404(SessionProposal, pk=proposal_pk)

    is_authorized = False
    # Only the mentor associated with the proposal can accept or reject it
    if request.user == proposal.mentor.user: # <--- MODIFIED THIS LINE
        is_authorized = True

    if not is_authorized or proposal.status != 'pending':
        messages.error(request, "You are not authorized to respond to this proposal or it's no longer pending.")
        return redirect(reverse('scheduling_sessions:my_proposals'))

    if request.method == 'POST':
        form = SessionProposalResponseForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            with transaction.atomic():
                if action == 'accept':
                    proposal.status = 'accepted'
                    proposal.save()

                    # Create a confirmed SessionSlot
                    session_slot = SessionSlot.objects.create(
                        mentor=proposal.mentor,
                        start_time=proposal.proposed_start_time,
                        end_time=proposal.proposed_end_time,
                        is_booked=True
                    )
                    # Create a Booking for the mentee
                    Booking.objects.create(
                        session_slot=session_slot,
                        mentee=proposal.mentee,
                        status='confirmed'
                    )

                    # FR: Record session details in MentorshipSession
                    MentorshipSession.objects.create(
                        mentee=proposal.mentee,
                        mentor=proposal.mentor,
                        start_time=proposal.proposed_start_time,
                        end_time=proposal.proposed_end_time,
                        topic=f"Mentorship Session: {proposal.message[:100] or 'No specific topic'}",
                        notes=f"Confirmed from proposal by {proposal.proposed_by.username}."
                    )

                    messages.success(request, 'Proposal accepted and session booked!')

                    # FR: Notify both parties of confirmation
                    send_mail(
                        'Session Proposal Accepted!',
                        f'Hi {proposal.mentee.user.username},\n\nYour session proposal with {proposal.mentor.user.username} for {proposal.proposed_start_time.strftime("%Y-%m-%d %H:%M")} has been accepted.',
                        'admin@uplifting.com',
                        [proposal.mentee.user.email],
                        fail_silently=True,
                    )
                    send_mail(
                        'Session Proposal Accepted!',
                        f'Hi {proposal.mentor.user.username},\n\nYou have accepted the session proposal from {proposal.mentee.user.username} for {proposal.proposed_start_time.strftime("%Y-%m-%d %H:%M")}.',
                        'admin@uplifting.com',
                        [proposal.mentor.user.email],
                        fail_silently=True,
                    )

                elif action == 'reject':
                    proposal.status = 'rejected'
                    proposal.save()
                    messages.info(request, 'Proposal rejected.')

                    # Notify the other party
                    recipient_user = proposal.mentee.user # Mentee is always the recipient of rejection from mentor
                    send_mail(
                        'Session Proposal Rejected',
                        f'Hi {recipient_user.username},\n\nYour session proposal for {proposal.proposed_start_time.strftime("%Y-%m-%d %H:%M")} has been rejected by {request.user.username}.',
                        'admin@uplifting.com',
                        [recipient_user.email],
                        fail_silently=True,
                    )
            return redirect(reverse('scheduling_sessions:my_proposals'))
    else:
        form = SessionProposalResponseForm()

    context = {
        'proposal': proposal,
        'form': form,
        'is_mentor_responding': request.user == proposal.mentor.user, # Still useful for template logic
        'is_mentee_responding': request.user == proposal.mentee.user, # Still useful for template logic
    }
    return render(request, 'scheduling_sessions/respond_to_proposal.html', context)
