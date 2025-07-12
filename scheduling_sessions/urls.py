# scheduling_sessions/urls.py
from django.urls import path
from . import views

app_name = 'scheduling_sessions' # Namespace for this app

urlpatterns = [
    path('slots/', views.available_slots, name='available_slots'),
    path('slots/<int:slot_pk>/book/', views.book_slot, name='book_slot'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    # Add more URLs as needed
]