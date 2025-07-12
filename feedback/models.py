# feedback/models.py
from django.db import models
from accounts.models import User # Import your custom User model
# from mentorship.models import MentorshipSession, MentorProfile, MenteeProfile # If feedback is for sessions/profiles

class Feedback(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_feedback')
    # Can be for a specific user, session, or general
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_feedback')
    # session = models.ForeignKey(MentorshipSession, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedback')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False) # If feedback can be public/private

    def __str__(self):
        return f"Feedback from {self.sender.username} to {self.recipient.username if self.recipient else 'N/A'}"

class Rating(models.Model):
    rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    # Can rate a user (e.g., mentor), or a session
    rated_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='received_ratings')
    # rated_session = models.ForeignKey(MentorshipSession, on_delete=models.CASCADE, null=True, blank=True, related_name='ratings')
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], help_text="Score from 1 to 5")
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating by {self.rater.username}: {self.score} for {self.rated_user.username if self.rated_user else 'Session'}"
