# feedback/urls.py
from django.urls import path
from . import views

app_name = 'feedback' # Namespace for this app

urlpatterns = [
    path('submit/', views.submit_feedback, name='submit_feedback'),
    path('my-feedback/', views.my_feedback, name='my_feedback'),
    # Add more URLs as needed
]
