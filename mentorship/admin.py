# mentorship/admin.py
from django.contrib import admin
from .models import MentorProfile, MenteeProfile, MentorshipRequest, MentorshipSession, MentorshipAssignment # <--- ADDED MentorshipAssignment

admin.site.register(MentorProfile)
admin.site.register(MenteeProfile)
admin.site.register(MentorshipRequest)
admin.site.register(MentorshipSession)
admin.site.register(MentorshipAssignment) # <--- REGISTERED MentorshipAssignment
