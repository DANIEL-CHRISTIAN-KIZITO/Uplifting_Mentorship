from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import models

# In this setup, the main dashboard logic is handled by accounts.views.dashboard.
# This file can be used for other dashboard-specific views if your dashboard app grows.
# For now, you can have a simple redirect or a placeholder view if needed.

# This view will render the main dashboard page.
@login_required
def dashboard_home(request):
    return render(request, 'dashboard_home.html')


from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
import csv
from io import BytesIO
from reportlab.pdfgen import canvas

from accounts.models import User
from scheduling_sessions.models import Session
from feedback.models import Feedback

@staff_member_required
def analytics_dashboard(request):
    total_users = User.objects.count()
    active_mentors = User.objects.filter(role='mentor').count()
    active_mentees = User.objects.filter(role='mentee').count()

    total_sessions = Session.objects.count()
    completed_sessions = Session.objects.filter(status='completed').count()
    avg_rating = Feedback.objects.aggregate(avg=models.Avg('rating'))['avg'] or 0
    total_feedback = Feedback.objects.count()

    context = {
        'total_users': total_users,
        'active_mentors': active_mentors,
        'active_mentees': active_mentees,
        'total_sessions': total_sessions,
        'completed_sessions': completed_sessions,
        'avg_rating': round(avg_rating, 2),
        'total_feedback': total_feedback,
    }
    return render(request, 'dashboard/analytics_dashboard.html', context)


@staff_member_required
def export_report_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mentorship_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Metric', 'Value'])
    writer.writerow(['Total Users', User.objects.count()])
    writer.writerow(['Active Mentors', User.objects.filter(role='mentor').count()])
    writer.writerow(['Active Mentees', User.objects.filter(role='mentee').count()])
    writer.writerow(['Total Sessions', Session.objects.count()])
    writer.writerow(['Completed Sessions', Session.objects.filter(status='completed').count()])
    writer.writerow(['Average Feedback Rating', Feedback.objects.aggregate(avg=models.Avg('rating'))['avg'] or 0])
    writer.writerow(['Total Feedback Entries', Feedback.objects.count()])

    return response


@staff_member_required
def export_report_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    p.setFont("Helvetica", 14)
    p.drawString(100, 800, "Uplifting Mentorship - Analytics Report")

    p.setFont("Helvetica", 12)
    y = 760
    p.drawString(100, y, f"Total Users: {User.objects.count()}")
    p.drawString(100, y - 20, f"Active Mentors: {User.objects.filter(role='mentor').count()}")
    p.drawString(100, y - 40, f"Active Mentees: {User.objects.filter(role='mentee').count()}")
    p.drawString(100, y - 60, f"Total Sessions: {Session.objects.count()}")
    p.drawString(100, y - 80, f"Completed Sessions: {Session.objects.filter(status='completed').count()}")
    p.drawString(100, y - 100, f"Average Rating: {Feedback.objects.aggregate(avg=models.Avg('rating'))['avg'] or 0}")
    p.drawString(100, y - 120, f"Total Feedback Entries: {Feedback.objects.count()}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf', headers={
        'Content-Disposition': 'attachment; filename="mentorship_report.pdf"'
    })

