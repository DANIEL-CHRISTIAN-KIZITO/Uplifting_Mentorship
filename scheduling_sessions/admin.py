
# scheduling_sessions/admin.py
from django.contrib import admin
from .models import SessionSlot, Booking, SessionProposal # Import SessionProposal

admin.site.register(SessionSlot)
admin.site.register(Booking)
admin.site.register(SessionProposal) # Register the new model
