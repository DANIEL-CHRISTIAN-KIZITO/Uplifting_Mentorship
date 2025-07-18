# progress/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Goal, ProgressUpdate
# from .forms import GoalForm, ProgressUpdateForm # You'll create these
from mentorship.models import MenteeProfile, MentorProfile, MentorshipAssignment # Import MentorshipAssignment

# Helper function to check if user is a mentee
def is_mentee(user):
    return hasattr(user, 'mentee_profile') and user.mentee_profile is not None

# Helper function to check if user is a mentor
def is_mentor(user):
    return hasattr(user, 'mentor_profile') and user.mentor_profile is not None

@login_required
@user_passes_test(is_mentee, login_url='/accounts/dashboard/') # Only mentees can view their goals
def my_goals(request):
    """
    FR17. The system shall allow mentees to set personal development goals.
    Displays a mentee's goals and allows them to create new ones.
    """
    mentee_profile = get_object_or_404(MenteeProfile, user=request.user)
    goals = Goal.objects.filter(user=request.user).order_by('-created_at')

    # Placeholder for GoalForm (assuming it will be defined later)
    # if request.method == 'POST':
    #     form = GoalForm(request.POST)
    #     if form.is_valid():
    #         goal = form.save(commit=False)
    #         goal.user = request.user # Assign the goal to the current user (mentee)
    #         goal.save()
    #         messages.success(request, 'Goal added successfully!')
    #         return redirect(reverse('progress:my_goals'))
    #     else:
    #         messages.error(request, 'Please correct the errors below.')
    # else:
    #     form = GoalForm()
    form = None # Placeholder if form is not implemented yet

    context = {
        'goals': goals,
        'form': form,
        'is_mentee': True, # Explicitly pass for template logic
    }
    return render(request, 'progress/my_goals.html', context)


@login_required
def goal_detail(request, pk):
    """
    FR19. The system shall provide a dashboard for both mentors and mentees to view progress history.
    Displays details of a specific goal and its progress updates.
    Allows mentors to record progress updates.
    """
    goal = get_object_or_404(Goal, pk=pk)

    # Authorization check:
    # 1. User is the mentee who owns the goal
    # 2. User is a mentor assigned to this mentee
    is_authorized = False
    if request.user == goal.user: # User is the mentee
        is_authorized = True
    elif is_mentor(request.user): # User is a mentor, check if assigned to this mentee
        try:
            mentor_profile = MentorProfile.objects.get(user=request.user)
            # Check if this mentor is assigned to the mentee who owns the goal
            # Use the related_name 'current_assignment' from MenteeProfile
            MentorshipAssignment.objects.get(mentor=mentor_profile, mentee=goal.user.mentee_profile)
            is_authorized = True
        except (MentorProfile.DoesNotExist, MentorshipAssignment.DoesNotExist):
            pass # Not authorized

    if not is_authorized:
        messages.error(request, "You are not authorized to view this goal.")
        return redirect(reverse('accounts:dashboard')) # Or appropriate redirect

    # Corrected: Order by 'date' instead of 'timestamp'
    updates = goal.updates.all().order_by('date')

    progress_form = None
    # Only the assigned mentor can record progress
    # Check if the user is a mentor AND if they are the assigned mentor for this mentee
    if is_mentor(request.user):
        try:
            mentee_assignment = MentorshipAssignment.objects.get(mentee=goal.user.mentee_profile)
            if mentee_assignment.mentor.user == request.user:
                # Placeholder for ProgressUpdateForm (assuming it will be defined later)
                # if request.method == 'POST':
                #     progress_form = ProgressUpdateForm(request.POST)
                #     if progress_form.is_valid():
                #         progress_update = progress_form.save(commit=False)
                #         progress_update.goal = goal
                #         progress_update.save()
                #         # Update goal completion status if 100%
                #         if progress_update.progress_percentage == 100 and not goal.is_completed:
                #             goal.is_completed = True
                #             goal.completed_at = timezone.now()
                #             goal.save()
                #             messages.success(request, 'Goal marked as completed!')
                #         messages.success(request, 'Progress updated successfully!')
                #         return redirect(reverse('progress:goal_detail', args=[pk]))
                #     else:
                #         messages.error(request, 'Please correct the errors in the progress update.')
                # else:
                #     progress_form = ProgressUpdateForm()
                pass # Placeholder if form is not implemented yet
        except MentorshipAssignment.DoesNotExist:
            pass # No assignment, so no form for this mentor

    context = {
        'goal': goal,
        'updates': updates,
        'progress_form': progress_form,
        'is_mentee_owner': request.user == goal.user,
        'is_mentor_reviewer': is_mentor(request.user) and progress_form is not None, # Mentor can review and record if assigned
    }
    return render(request, 'progress/goal_detail.html', context)


@login_required
@user_passes_test(is_mentor, login_url='/accounts/dashboard/') # Only mentors can view mentee progress
def mentee_progress_overview(request):
    """
    FR19. The system shall provide a dashboard for both mentors and mentees to view progress history.
    Allows a mentor to see a list of their assigned mentees and their goals.
    """
    mentor_profile = get_object_or_404(MentorProfile, user=request.user)
    
    # Corrected: Get MenteeProfiles through MentorshipAssignment
    # Filter MentorshipAssignment by the current mentor, then get the mentee profiles from those assignments.
    assigned_mentee_assignments = MentorshipAssignment.objects.filter(mentor=mentor_profile)
    assigned_mentees = [assignment.mentee for assignment in assigned_mentee_assignments]

    mentees_with_goals = []
    for mentee in assigned_mentees:
        goals = Goal.objects.filter(user=mentee.user).order_by('-created_at')
        mentees_with_goals.append({
            'mentee': mentee,
            'goals': goals,
            'total_goals': goals.count(),
            'completed_goals': goals.filter(is_completed=True).count(),
        })

    context = {
        'mentees_with_goals': mentees_with_goals,
        'is_mentor': True, # Explicitly pass for template logic
    }
    return render(request, 'progress/mentee_progress_overview.html', context)


@login_required
@user_passes_test(is_mentee, login_url='/accounts/dashboard/')
def mark_goal_completed(request, pk):
    """
    Allows a mentee to mark their own goal as completed.
    """
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if not goal.is_completed:
        goal.is_completed = True
        goal.completed_at = timezone.now()
        goal.save()
        messages.success(request, f"Goal '{goal.title}' marked as completed!")
    else:
        messages.info(request, f"Goal '{goal.title}' is already completed.")
    return redirect(reverse('progress:my_goals'))

