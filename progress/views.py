# progress/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Goal, ProgressUpdate
# from .forms import GoalForm, ProgressUpdateForm # You'll create these

@login_required
def my_goals(request):
    goals = Goal.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'progress/my_goals.html', {'goals': goals})

@login_required
def goal_detail(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    updates = goal.updates.all().order_by('-date')
    return render(request, 'progress/goal_detail.html', {'goal': goal, 'updates': updates})

# Add views for creating/updating goals and progress updates