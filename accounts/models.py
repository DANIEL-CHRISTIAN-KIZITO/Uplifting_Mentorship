from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Custom fields for your User model
    ROLE_CHOICES = [
        ('mentor', 'Mentor'),
        ('mentee', 'Mentee'),
        ('admin', 'Administrator'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='mentee')
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    receive_notifications = models.BooleanField(default=True)
    PROFILE_VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('friends_only', 'Friends Only'),
    ]
    profile_visibility = models.CharField(
        max_length=20,
        choices=PROFILE_VISIBILITY_CHOICES,
        default='public',
        verbose_name='Profile Visibility'
    )

    # Add related_name to avoid clashes if you have multiple ForeignKeys to User
    # (though AbstractUser usually handles its own groups/user_permissions relations)
    # If you encounter FieldError related to groups or user_permissions, uncomment these:
    # groups = models.ManyToManyField(
    #     'auth.Group',
    #     verbose_name=('groups'),
    #     blank=True,
    #     help_text=(
    #         'The groups this user belongs to. A user will get all permissions '
    #         'granted to each of their groups.'
    #     ),
    #     related_name="custom_user_set", # Unique related_name
    #     related_query_name="user",
    # )
    # user_permissions = models.ManyToManyField(
    #     'auth.Permission',
    #     verbose_name=('user permissions'),
    #     blank=True,
    #     help_text=('Specific permissions for this user.'),
    #     related_name="custom_user_permissions", # Unique related_name
    #     related_query_name="user",
    # )

    def __str__(self):
        return self.username

