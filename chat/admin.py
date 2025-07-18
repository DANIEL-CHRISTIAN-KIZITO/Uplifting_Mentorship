# chat/admin.py
from django.contrib import admin
from .models import ChatRoom, Message

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant1', 'participant2', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('participant1__username', 'participant2__username')
    raw_id_fields = ('participant1', 'participant2') # Use raw_id_fields for User foreign keys

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_room', 'sender', 'timestamp', 'is_read')
    list_filter = ('timestamp', 'is_read', 'sender__username')
    search_fields = ('chat_room__participant1__username', 'chat_room__participant2__username', 'sender__username', 'content')
    date_hierarchy = 'timestamp'
    raw_id_fields = ('chat_room', 'sender') # Use raw_id_fields for foreign keys
