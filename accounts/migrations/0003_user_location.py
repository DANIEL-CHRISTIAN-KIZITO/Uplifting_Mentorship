# Generated by Django 5.2.4 on 2025-07-17 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_bio_user_contact_info_user_expertise_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(default='Not specified', max_length=255),
        ),
    ]
