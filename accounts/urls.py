from django.urls import path
from .views import register, user_login, user_logout, dashboard, dashboard_home # Import your custom views

app_name = 'accounts' # This sets the namespace for URLs in this app

urlpatterns = [
    path('', dashboard_home, name='dashboard_home'), # Default to login view
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'), # Your custom dashboard view
    # Do NOT include django.contrib.auth.urls here, they are included in project urls.py
]
