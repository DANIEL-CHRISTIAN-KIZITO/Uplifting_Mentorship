# scheduling_sessions/urls.py
from django.urls import path
from . import views

app_name = 'scheduling_sessions' # Namespace for this app

urlpatterns = [
    path('slots/', views.available_slots, name='available_slots'),
    path('slots/<int:slot_pk>/book/', views.book_slot, name='book_slot'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    # Add more URLs as needed
    # --- NEW PROPOSAL AND CONFIRMATION URLs ---
    # Mentee proposes to a specific mentor
    path('propose/<int:mentor_pk>/', views.propose_session, name='propose_session_to_mentor'),
    # Mentor proposes to a mentee (mentee_pk would be in POST or query param)
    path('propose/', views.propose_session, name='propose_session_general'),
    path('my-proposals/', views.my_proposals, name='my_proposals'),
    path('proposals/<int:proposal_pk>/respond/', views.respond_to_proposal, name='respond_to_proposal'),

]