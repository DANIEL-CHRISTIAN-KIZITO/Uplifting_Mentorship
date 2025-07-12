# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat' # Namespace for this app

urlpatterns = [
    path('rooms/', views.chat_room_list, name='chat_room_list'),
    path('rooms/<int:pk>/', views.chat_room_detail, name='chat_room_detail'),
    # Add more URLs as needed
]
