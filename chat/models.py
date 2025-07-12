# chat/models.py
from django.db import models
from accounts.models import User # Import your custom User model
# from mentorship.models import MentorshipSession # If messages are tied to sessions

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    # session = models.OneToOneField(MentorshipSession, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_room') # If 1:1 with session

    def __str__(self):
        return self.name

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chat_messages') # Use unique related_name
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat_room.name} at {self.timestamp.strftime('%H:%M')}"