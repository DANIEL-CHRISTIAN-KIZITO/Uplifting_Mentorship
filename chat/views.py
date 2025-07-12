# chat/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ChatRoom, Message
# from .forms import MessageForm # You'll create this

@login_required
def chat_room_list(request):
    chat_rooms = request.user.chat_rooms.all() # Assuming User has related_name 'chat_rooms'
    return render(request, 'chat/chat_room_list.html', {'chat_rooms': chat_rooms})

@login_required
def chat_room_detail(request, pk):
    chat_room = get_object_or_404(ChatRoom, pk=pk)
    # Ensure user is a participant
    if request.user not in chat_room.participants.all():
        messages.error(request, "You are not a participant in this chat room.")
        return redirect(reverse('chat:chat_room_list'))

    messages_in_room = chat_room.messages.all()
    # This is a placeholder; you'd use a form for sending messages
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(chat_room=chat_room, sender=request.user, content=content)
            return redirect(reverse('chat:chat_room_detail', args=[pk])) # Redirect to clear POST data
        else:
            messages.error(request, "Message cannot be empty.")

    return render(request, 'chat/chat_room_detail.html', {'chat_room': chat_room, 'messages': messages_in_room})

# Add views for creating chat rooms, etc.