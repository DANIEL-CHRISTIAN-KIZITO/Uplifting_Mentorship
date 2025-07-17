# scheduling_sessions/management/commands/send_upcoming_session_reminders.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from mentorship.models import MentorshipSession # Import your MentorshipSession model

class Command(BaseCommand):
    help = 'Sends email reminders for upcoming mentorship sessions.'

    def handle(self, *args, **options):
        now = timezone.now()
        # Define the timeframe for upcoming sessions (e.g., sessions starting within the next 24 hours)
        # and not already completed
        upcoming_sessions = MentorshipSession.objects.filter(
            start_time__gte=now,
            start_time__lte=now + timedelta(hours=24),
            is_completed=False
        )

        if not upcoming_sessions.exists():
            self.stdout.write(self.style.SUCCESS('No upcoming sessions found for reminders.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Found {upcoming_sessions.count()} upcoming sessions to send reminders for.'))

        for session in upcoming_sessions:
            mentee_email = session.mentee.user.email
            mentor_email = session.mentor.user.email

            session_time_str = session.start_time.strftime('%Y-%m-%d at %H:%M %Z')
            session_topic = session.topic or "a general mentorship session"

            # Email to Mentee
            mentee_subject = f"Reminder: Your Upcoming Mentorship Session with {session.mentor.user.username}"
            mentee_message = (
                f"Hi {session.mentee.user.username},\n\n"
                f"Just a friendly reminder about your upcoming mentorship session with {session.mentor.user.username}.\n"
                f"Topic: {session_topic}\n"
                f"Time: {session_time_str}\n\n"
                f"Please be prepared for your session!\n\n"
                f"The Uplifting Mentorship Team"
            )
            send_mail(mentee_subject, mentee_message, 'admin@uplifting.com', [mentee_email], fail_silently=True)

            # Email to Mentor
            mentor_subject = f"Reminder: Your Upcoming Mentorship Session with {session.mentee.user.username}"
            mentor_message = (
                f"Hi {session.mentor.user.username},\n\n"
                f"Just a friendly reminder about your upcoming mentorship session with {session.mentee.user.username}.\n"
                f"Topic: {session_topic}\n"
                f"Time: {session_time_str}\n\n"
                f"Please be prepared for your session!\n\n"
                f"The Uplifting Mentorship Team"
            )
            send_mail(mentor_subject, mentor_message, 'admin@uplifting.com', [mentor_email], fail_silently=True)

            self.stdout.write(self.style.SUCCESS(f'Sent reminder for session {session.id} to {mentee_email} and {mentor_email}'))

        self.stdout.write(self.style.SUCCESS('Upcoming session reminders sent successfully!'))

