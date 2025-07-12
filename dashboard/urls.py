from django.urls import path
from .views import dashboard_home # Assuming you use dashboard_home from above

app_name = 'dashboard' # Define a namespace for the dashboard app

urlpatterns = [
    path('', dashboard_home, name='home'), # Maps /dashboard/ to dashboard_home
    # Add other dashboard-specific URLs here
]
