from django.urls import path
from .views import dashboard_home, analytics_dashboard, export_report_csv, export_report_pdf, custom_admin_dashboard # Import required views

app_name = 'dashboard' # Define a namespace for the dashboard app

from .views import (
    dashboard_home,
    analytics_dashboard,
    export_report_csv,
    export_report_pdf,
    custom_admin_dashboard,
    manage_users,
    manage_sessions,
    manage_resources,
)

urlpatterns = [
    path('', dashboard_home, name='dashboard_home'),  # Maps /dashboard/ to dashboard_home
    path('analytics/', analytics_dashboard, name='analytics_dashboard'),
    path('export/csv/', export_report_csv, name='export_csv'),
    path('export/pdf/', export_report_pdf, name='export_pdf'),
    path('admin/', custom_admin_dashboard, name='custom_admin'),
    path('admin/users/', manage_users, name='manage_users'),
    path('admin/sessions/', manage_sessions, name='manage_sessions'),
    path('admin/resources/', manage_resources, name='manage_resources'),
]
