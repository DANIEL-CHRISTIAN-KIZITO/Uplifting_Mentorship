from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User # Import your custom User model

# Custom Registration Form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    # Add custom fields from your User model here if you want them in registration
    # For example, if you want 'role' to be selectable during registration:
    # role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role', 'photo', 'receive_notifications', 'profile_visibility')
        # Ensure 'email' is included if you want it during registration.
        # Add other custom fields here.

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

# Custom Login Form (inherits from Django's AuthenticationForm for convenience)
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    # No need for a custom clean method unless you have specific cross-field validation
    # that AuthenticationForm doesn't cover.
# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'expertise', 'interests', 'contact_info', 'profile_photo']
