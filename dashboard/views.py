from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# In this setup, the main dashboard logic is handled by accounts.views.dashboard.
# This file can be used for other dashboard-specific views if your dashboard app grows.
# For now, you can have a simple redirect or a placeholder view if needed.

# This view will render the main dashboard page.
@login_required
def dashboard_home(request):
    return render(request, 'dashboard_home.html')


# Or if you want this app to render its own dashboard content
# @login_required
# def dashboard_main(request):
#     context = {
#         'message': 'Welcome to your main dashboard!',
#         # ... additional dashboard-specific data
#     }
#     return render(request, 'dashboard/dashboard.html', context)
