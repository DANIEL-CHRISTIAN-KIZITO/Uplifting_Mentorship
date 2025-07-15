from django.urls import path
from .views import dashboard_home, analytics_dashboard, export_report_csv, export_report_pdf # Import required views

app_name = 'dashboard' # Define a namespace for the dashboard app

urlpatterns = [
    path('', dashboard_home, name='dashboard_home'), # Maps /dashboard/ to dashboard_home
    # Add other dashboard-specific URLs here
    path('analytics/', analytics_dashboard, name='analytics_dashboard'),
    path('export/csv/', export_report_csv, name='export_csv'),
    path('export/pdf/', export_report_pdf, name='export_pdf'), 
]
