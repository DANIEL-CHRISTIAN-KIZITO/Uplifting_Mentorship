from django.contrib import admin
from .models import MentorshipRequest, MentorshipAssignment

admin.site.register(MentorshipRequest)
admin.site.register(MentorshipAssignment)

# mentorship/admin.py
from django.contrib import admin
from .models import MentorProfile

@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'location', 'available_for_mentorship')
    list_filter = ('available_for_mentorship', 'location', 'expertise')
