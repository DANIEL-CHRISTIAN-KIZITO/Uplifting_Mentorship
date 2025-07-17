# mentorship/urls.py
from django.urls import path
from . import views

app_name = 'mentorship' # Namespace for this app

urlpatterns = [
    path('mentors/', views.mentor_list, name='mentor_list'),
    path('mentors/<int:pk>/', views.mentor_detail, name='mentor_detail'),
    path('mentors/<int:mentor_pk>/request/', views.request_mentorship, name='request_mentorship'),
    path('mentee/dashboard/', views.mentee_dashboard, name='mentee_dashboard'),
    # Add more URLs as needed
    
    path('search/', views.search_mentors, name='search_mentors'),
    path('manage/', views.manage_requests, name='manage_requests'),
    path('update/<int:request_id>/<str:action>/', views.update_request_status, name='update_status'),
    path('assign/', views.assign_mentor, name='assign_mentor'),
    path('assign/success/', views.assign_success, name='assign_success'),
    path('my-mentees/', views.my_mentees_view, name='my_mentees'),
    # --- NEW ADMIN ASSIGNMENT URLs ---
    path('admin/assign-mentor/', views.assign_mentor, name='assign_mentor'),
    path('admin/assign-success/', views.assign_success, name='assign_success'),
    # Add more URLs as needed
]
