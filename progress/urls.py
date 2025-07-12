# progress/urls.py
from django.urls import path
from . import views

app_name = 'progress' # Namespace for this app

urlpatterns = [
    path('my-goals/', views.my_goals, name='my_goals'),
    path('goals/<int:pk>/', views.goal_detail, name='goal_detail'),
    # Add more URLs as needed
]
