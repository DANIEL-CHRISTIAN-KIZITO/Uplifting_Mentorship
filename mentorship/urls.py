# mentorship/urls.py
from django.urls import path
from . import views

app_name = 'mentorship' # Namespace for this app

urlpatterns = [
    path('mentors/', views.mentor_list, name='mentor_list'),
    path('mentors/<int:pk>/', views.mentor_detail, name='mentor_detail'),
    path('mentors/<int:mentor_pk>/request/', views.request_mentorship, name='request_mentorship'),
    path('mentee/dashboard/', views.mentee_dashboard, name='mentee_dashboard'),
    path('search/', views.search_mentors, name='search_mentors'),
    path('my-mentees/', views.my_mentees, name='my_mentees'), # New URL for mentor's mentees
    path('requests/manage/', views.manage_requests, name='manage_requests'), # New URL for managing requests
    path('requests/<int:request_pk>/<str:action>/', views.respond_to_request, name='respond_to_request'), # New URL for responding to requests
    # Add more URLs as needed
]
