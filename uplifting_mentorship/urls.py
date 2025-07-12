from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
#from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


# Import Django's built-in authentication views
from django.contrib.auth import views as auth_views
from dashboard.views import dashboard_home

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', TemplateView.as_view(template_name='login.html'), name='accounts:login'),
path('', dashboard_home, name='dashboard_home'),  # Redirect to the dashboard home view
    # Include your custom 'accounts' app URLs.
    # These will be accessible at /accounts/register/, /accounts/login/, /accounts/logout/ etc.
    # The 'accounts' namespace is set within accounts/urls.py.
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # Explicitly define Django's built-in password reset URLs.
    # These are also placed under the 'accounts/' path prefix.
    # We give them 'name' attributes that are within the 'accounts' namespace,
    # so {% url 'accounts:password_reset' %} will correctly resolve.
    # We explicitly set template_name to point to your 'templates/accounts/' directory.
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        success_url=reverse_lazy('accounts:password_reset_done')
    ), name='password_reset'),

    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),

    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    # Include other app URLs
    path('mentorship/', include('mentorship.urls')),
    path('scheduling_sessions/', include('scheduling_sessions.urls')),
    path('chat/', include('chat.urls')),
    path('progress/', include('progress.urls')),
    path('feedback/', include('feedback.urls')),
    path('dashboard/', include('dashboard.urls')), # Dashboard app URLs
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')), # For Django Rest Framework browsable API
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
