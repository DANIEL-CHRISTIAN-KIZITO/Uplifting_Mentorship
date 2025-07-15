# mentorship/models.py
from django.db import models
from accounts.models import User # Import your custom User model

class MentorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=255, help_text="e.g., Web Development, Career Coaching")
    available_for_mentorship = models.BooleanField(default=True)
    # Add other mentor-specific fields

    def __str__(self):
        return f"Mentor: {self.user.username} ({self.expertise})"

class MenteeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentee_profile')
    goals = models.TextField(blank=True)
    learning_interests = models.CharField(max_length=255, help_text="e.g., Python, Data Science")
    # Add other mentee-specific fields

    def __str__(self):
        return f"Mentee: {self.user.username}"

class MentorshipRequest(models.Model):
    mentee = models.ForeignKey(MenteeProfile, on_delete=models.CASCADE, related_name='sent_requests')
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='received_requests')
    message = models.TextField()
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.mentee.user.username} to {self.mentor.user.username} - {self.status}"

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
    
    from django.db import models
from accounts.models import User

class MentorshipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    mentee = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    mentor = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mentee} → {self.mentor} ({self.status})"
