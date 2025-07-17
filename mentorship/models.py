# mentorship/models.py
from django.db import models
from django.contrib.auth import get_user_model # Use get_user_model for User model

# Get the custom User model
User = get_user_model()

class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField(blank=True)
    available_for_mentorship = models.BooleanField(default=True)
    expertise = models.CharField(max_length=255, default='Not specified')
    location = models.CharField(max_length=255, default='Not specified')
    interests = models.TextField(default="General mentoring")

    def __str__(self):
        return f"Mentor: {self.user.username} ({self.expertise})"

class MenteeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentee_profile')
    goals = models.TextField(blank=True)
    learning_interests = models.CharField(max_length=255, help_text="e.g., Python, Data Science", blank=True)
    # Add other mentee-specific fields

    def __str__(self):
        return f"Mentee: {self.user.username}"

class MentorshipRequest(models.Model):
    # mentee and mentor link to their respective profiles
    mentee = models.ForeignKey(MenteeProfile, related_name='sent_requests', on_delete=models.CASCADE)
    mentor = models.ForeignKey(MentorProfile, related_name='received_requests', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'), # Use 'accepted' when assigned
        ('rejected', 'Rejected'),
        ('assigned', 'Assigned'), # New status for when a mentor is explicitly assigned
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.mentee.user.username} to {self.mentor.user.username} ({self.status})"

class MentorshipSession(models.Model):
    mentee = models.ForeignKey(MenteeProfile, on_delete=models.CASCADE, related_name='mentorship_sessions_as_mentee')
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='mentorship_sessions_as_mentor')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    topic = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Session: {self.topic} ({self.start_time.strftime('%Y-%m-%d %H:%M')})"

class MentorshipAssignment(models.Model):
    # Links a mentee profile to a mentor profile
    mentee = models.OneToOneField(
        MenteeProfile,
        related_name='current_assignment', # A mentee has one current assignment
        on_delete=models.CASCADE,
        help_text="The mentee who is assigned a mentor."
    )
    mentor = models.ForeignKey(
        MentorProfile,
        related_name='assigned_mentees', # A mentor can have many assigned mentees
        on_delete=models.CASCADE,
        help_text="The mentor assigned to this mentee."
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    # Optionally link to the request that led to this assignment
    mentorship_request = models.OneToOneField(
        MentorshipRequest,
        on_delete=models.SET_NULL, # If request is deleted, assignment remains
        null=True, blank=True,
        related_name='assignment',
        help_text="The request that led to this assignment (optional)."
    )

    def __str__(self):
        return f"Assignment: {self.mentee.user.username} assigned to {self.mentor.user.username}"

    class Meta:
        # Ensure a mentee can only be assigned to one mentor at a time
        unique_together = ('mentee', 'assigned_at') # Or just 'mentee' if you want only one active assignment
