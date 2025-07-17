# scheduling_sessions/models.py
from django.db import models
from accounts.models import User # Assuming User is involved in scheduling
from mentorship.models import MentorProfile, MenteeProfile # Import profile models

class SessionSlot(models.Model):
    """Represents a confirmed, available time slot offered by a mentor."""
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='session_slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False) # True if a booking exists for this slot

    def __str__(self):
        return f"Slot for {self.mentor.user.username} from {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class SessionProposal(models.Model):
    """Represents a proposed session time between a mentee and a mentor."""
    PROPOSAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    mentee = models.ForeignKey(MenteeProfile, on_delete=models.CASCADE, related_name='sent_proposals')
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='received_proposals')
    proposed_start_time = models.DateTimeField()
    proposed_end_time = models.DateTimeField()
    message = models.TextField(blank=True, help_text="Optional message with the proposal.")
    status = models.CharField(max_length=10, choices=PROPOSAL_STATUS_CHOICES, default='pending')
    proposed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_proposals') # Who initiated the proposal
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Proposal from {self.mentee.user.username} to {self.mentor.user.username} ({self.proposed_start_time.strftime('%Y-%m-%d %H:%M')}) - {self.status}"

class Booking(models.Model):
    """Represents a confirmed booking of a SessionSlot by a mentee."""
    session_slot = models.OneToOneField(SessionSlot, on_delete=models.CASCADE, related_name='booking')
    mentee = models.ForeignKey(MenteeProfile, on_delete=models.CASCADE, related_name='my_bookings')
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='confirmed') # e.g., confirmed, cancelled

    def __str__(self):
        return f"Booking of {self.session_slot} by {self.mentee.user.username}"

