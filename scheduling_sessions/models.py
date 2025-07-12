# scheduling_sessions/models.py
from django.db import models
from accounts.models import User # Assuming User is involved in scheduling
# from mentorship.models import MentorProfile, MenteeProfile # If you want to link to mentorship profiles

class SessionSlot(models.Model):
    # If linking to MentorProfile, use: mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='slots')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_slots') # Or your MentorProfile
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Slot for {self.mentor.username} from {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Booking(models.Model):
    session_slot = models.OneToOneField(SessionSlot, on_delete=models.CASCADE, related_name='booking')
    # If linking to MenteeProfile, use: mentee = models.ForeignKey(MenteeProfile, on_delete=models.CASCADE, related_name='bookings')
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_bookings') # Or your MenteeProfile
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='confirmed') # e.g., confirmed, cancelled

    def __str__(self):
        return f"Booking of {self.session_slot} by {self.mentee.username}"
