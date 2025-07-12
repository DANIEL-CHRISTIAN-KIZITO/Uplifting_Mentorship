# scheduling_sessions/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SessionSlot, Booking
# from .forms import SessionSlotForm, BookingForm # You'll create these

@login_required
def available_slots(request):
    slots = SessionSlot.objects.filter(is_booked=False).order_by('start_time')
    return render(request, 'scheduling_sessions/available_slots.html', {'slots': slots})

@login_required
def book_slot(request, slot_pk):
    slot = get_object_or_404(SessionSlot, pk=slot_pk, is_booked=False)
    if request.method == 'POST':
        # Assuming request.user is the mentee
        Booking.objects.create(session_slot=slot, mentee=request.user, status='confirmed')
        slot.is_booked = True
        slot.save()
        messages.success(request, 'Session booked successfully!')
        return redirect(reverse('scheduling_sessions:my_bookings'))
    return render(request, 'scheduling_sessions/book_slot.html', {'slot': slot})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(mentee=request.user).order_by('session_slot__start_time')
    return render(request, 'scheduling_sessions/my_bookings.html', {'bookings': bookings})

# Add views for mentor's slots, cancelling bookings, etc.