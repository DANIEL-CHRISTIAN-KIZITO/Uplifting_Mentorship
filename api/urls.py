# api/urls.py
from django.urls import path
from .views import UserDataAPIView, WelcomeAPIView # Import your API views

app_name = 'api' # Namespace for this app

urlpatterns = [
    path('user-data/', UserDataAPIView.as_view(), name='user_data'),
    path('welcome/', WelcomeAPIView.as_view(), name='welcome_api'),
    # Add more API endpoints here
]
