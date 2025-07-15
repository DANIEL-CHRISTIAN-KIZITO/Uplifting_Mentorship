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
    path('search/', views.search_mentors, name='search'),
    path('request/<int:mentor_id>/', views.request_mentorship, name='request'),
    path('manage/', views.manage_requests, name='manage_requests'),
    path('update/<int:request_id>/<str:action>/', views.update_request_status, name='update_status'),
]
