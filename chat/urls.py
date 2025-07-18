# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat' # Namespace for this app

urlpatterns = [
    path('rooms/', views.chat_room_list, name='chat_room_list'),
    path('rooms/<int:room_id>/', views.chat_room_detail, name='chat_room_detail'), # <--- CHANGED 'pk' TO 'room_id' HERE
    path('create-or-get/<int:user_pk>/', views.create_or_get_chat_room, name='create_or_get_chat_room'), # New URL
    # Add more URLs as needed
]
