# chat/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q # Import Q for complex lookups
from accounts.models import User # Import User model to create chat rooms

from .models import ChatRoom, Message
# from .forms import MessageForm # You'll create this

@login_required
def chat_room_list(request):
    # Get chat rooms where the current user is either participant1 or participant2
    chat_rooms = ChatRoom.objects.filter(Q(participant1=request.user) | Q(participant2=request.user)).order_by('-created_at')

    # For each chat room, find the other participant and the last message
    for room in chat_rooms:
        if room.participant1 == request.user:
            room.other_participant = room.participant2
        else:
            room.other_participant = room.participant1

        # Get the last message in the chat room
        # Corrected: Use order_by('-timestamp').first() to get the most recent message
        room.last_message = room.messages.order_by('-timestamp').first()
        # Count unread messages for the current user in this room
        room.unread_count = room.messages.filter(is_read=False).exclude(sender=request.user).count()

    return render(request, 'chat/chat_room_list.html', {'chat_rooms': chat_rooms})

@login_required
def chat_room_detail(request, room_id): # <--- CHANGED 'pk' TO 'room_id'
    chat_room = get_object_or_404(ChatRoom, pk=room_id) # <--- USE 'room_id' HERE

    # Ensure user is a participant
    if request.user not in [chat_room.participant1, chat_room.participant2]:
        messages.error(request, "You are not a participant in this chat room.")
        return redirect(reverse('chat:chat_room_list'))

    # Mark messages as read when the user views the chat room
    # Exclude messages sent by the current user themselves
    chat_room.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)

    messages_in_room = chat_room.messages.all()

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(chat_room=chat_room, sender=request.user, content=content)
            return redirect(reverse('chat:chat_room_detail', args=[room_id])) # <--- USE 'room_id' HERE
        else:
            messages.error(request, "Message cannot be empty.")

    # Determine the other participant for display
    if chat_room.participant1 == request.user:
        other_participant = chat_room.participant2
    else:
        other_participant = chat_room.participant1

    context = {
        'chat_room': chat_room,
        'messages': messages_in_room,
        'other_participant': other_participant,
    }
    return render(request, 'chat/chat_room_detail.html', context)


@login_required
def create_or_get_chat_room(request, user_pk):
    """
    Creates a chat room between the current user and another user,
    or redirects to an existing one.
    """
    other_user = get_object_or_404(User, pk=user_pk)

    # Prevent creating a chat with oneself
    if request.user == other_user:
        messages.error(request, "You cannot create a chat room with yourself.")
        return redirect(reverse('chat:chat_room_list'))

    # Try to find an existing chat room between these two users
    # Order of participants doesn't matter for finding the room
    chat_room = ChatRoom.objects.filter(
        (Q(participant1=request.user) & Q(participant2=other_user)) |
        (Q(participant1=other_user) & Q(participant2=request.user))
    ).first()

    if not chat_room:
        # If no room exists, create a new one
        chat_room = ChatRoom.objects.create(
            name=f"Chat between {request.user.username} and {other_user.username}",
            participant1=request.user,
            participant2=other_user
        )
        # Add participants to the ManyToMany field (if you decide to use it, currently not in model)
        # chat_room.participants.add(request.user, other_user)
        messages.success(request, f"New chat room created with {other_user.username}.")
    else:
        messages.info(request, f"Redirecting to existing chat with {other_user.username}.")

    return redirect(reverse('chat:chat_room_detail', args=[chat_room.pk]))
