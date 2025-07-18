# progress/urls.py
from django.urls import path
from . import views

app_name = 'progress' # Namespace for this app

urlpatterns = [
    path('my-goals/', views.my_goals, name='my_goals'), # Mentees view/create goals
    path('goals/<int:pk>/', views.goal_detail, name='goal_detail'), # View goal details & updates
    path('goals/<int:pk>/complete/', views.mark_goal_completed, name='mark_goal_completed'), # Mark goal as complete
    path('mentees-progress/', views.mentee_progress_overview, name='mentee_progress_overview'), # Mentor's view of mentee progress
]
