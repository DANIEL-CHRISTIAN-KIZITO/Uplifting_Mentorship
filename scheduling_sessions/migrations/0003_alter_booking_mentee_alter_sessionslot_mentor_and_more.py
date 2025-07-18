# Generated by Django 5.2.4 on 2025-07-17 19:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorship', '0005_mentorshipassignment_mentorship_request_and_more'),
        ('scheduling_sessions', '0002_session'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='mentee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_bookings', to='mentorship.menteeprofile'),
        ),
        migrations.AlterField(
            model_name='sessionslot',
            name='mentor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='session_slots', to='mentorship.mentorprofile'),
        ),
        migrations.CreateModel(
            name='SessionProposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposed_start_time', models.DateTimeField()),
                ('proposed_end_time', models.DateTimeField()),
                ('message', models.TextField(blank=True, help_text='Optional message with the proposal.')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_proposals', to='mentorship.menteeprofile')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_proposals', to='mentorship.mentorprofile')),
                ('proposed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initiated_proposals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Session',
        ),
    ]
