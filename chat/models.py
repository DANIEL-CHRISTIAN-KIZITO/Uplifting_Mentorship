# chat/models.py
from django.db import models
from accounts.models import User # Import your custom User model
# from mentorship.models import MentorshipSession # If messages are tied to sessions

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, default='General', unique=True)
    topic = models.TextField(blank=True, null=True, help_text="A brief description or topic for this chat room.") # <--- ADDED THIS LINE
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms_as_p1', null=True, blank=True)
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms_as_p2', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        # Ensure uniqueness for pairs of participants, regardless of order
        unique_together = ('participant1', 'participant2')

    def __str__(self):
        return self.name

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chat_messages') # Use unique related_name
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False) # To track unread messages

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat_room.name} at {self.timestamp.strftime('%H:%M')}"
