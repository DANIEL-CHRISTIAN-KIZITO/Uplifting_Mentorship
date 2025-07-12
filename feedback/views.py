# feedback/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User # To select recipient
from .models import Feedback, Rating
# from .forms import FeedbackForm, RatingForm # You'll create these

@login_required
def submit_feedback(request):
    # This is a placeholder; you'd use a form
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        message = request.POST.get('message')
        if recipient_id and message:
            recipient_user = get_object_or_404(User, pk=recipient_id)
            Feedback.objects.create(sender=request.user, recipient=recipient_user, message=message)
            messages.success(request, 'Feedback submitted successfully!')
            return redirect(reverse('feedback:my_feedback'))
        else:
            messages.error(request, 'Recipient and message are required.')
    
    users = User.objects.exclude(pk=request.user.pk) # Example: allow sending feedback to other users
    return render(request, 'feedback/submit_feedback.html', {'users': users})

@login_required
def my_feedback(request):
    sent_feedback = Feedback.objects.filter(sender=request.user).order_by('-created_at')
    received_feedback = Feedback.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'feedback/my_feedback.html', {'sent_feedback': sent_feedback, 'received_feedback': received_feedback})

# Add views for submitting ratings, viewing public feedback, etc.
