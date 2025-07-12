# progress/models.py
from django.db import models
from accounts.models import User # Import your custom User model

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    target_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Goal: {self.title}"

class ProgressUpdate(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='updates')
    date = models.DateField(auto_now_add=True)
    notes = models.TextField()
    progress_percentage = models.IntegerField(default=0, help_text="Percentage of goal completion")

    def __str__(self):
        return f"Update for '{self.goal.title}' on {self.date}"