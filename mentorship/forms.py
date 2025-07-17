# mentorship/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import MentorshipAssignment
from .models import MentorshipRequest, MentorProfile

User = get_user_model()

class AssignMentorForm(forms.ModelForm):
    class Meta:
        model = MentorshipAssignment
        fields = ['mentee', 'mentor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mentee'].queryset = User.objects.filter(role='mentee')
        self.fields['mentor'].queryset = User.objects.filter(role='mentor')
        
# mentorship/forms.py

from django import forms

class MentorSearchForm(forms.Form):
    expertise = forms.CharField(required=False, label='Expertise')
    location = forms.CharField(required=False, label='Location')
    interests = forms.CharField(required=False, label='Interests')

class MentorshipRequestForm(forms.ModelForm):
    class Meta:
        model = MentorshipRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Why do you want this mentorship?'}),
        }
        
        
        
# mentorship/forms.py
class MentorProfileForm(forms.ModelForm):
    class Meta:
        model = MentorProfile
        fields = ['bio', 'expertise', 'location', 'interests', 'available_for_mentorship']
        
        
# mentorship/forms.py
from django import forms
from .models import MentorshipRequest, MentorProfile, MentorshipAssignment, MenteeProfile

class AssignMentorForm(forms.Form):
    # Field to select a pending mentorship request
    mentorship_request = forms.ModelChoiceField(
        queryset=MentorshipRequest.objects.filter(status='pending').order_by('created_at'),
        empty_label="Select a pending request",
        label="Pending Mentorship Request",
        help_text="Select a request to assign a mentor to."
    )

    # Field to select an available mentor
    mentor = forms.ModelChoiceField(
        queryset=MentorProfile.objects.filter(available_for_mentorship=True).order_by('user__username'),
        empty_label="Select an available mentor",
        label="Available Mentor",
        help_text="Choose a mentor to assign."
    )

    def clean(self):
        cleaned_data = super().clean()
        mentorship_request = cleaned_data.get('mentorship_request')
        mentor = cleaned_data.get('mentor')

        if mentorship_request and mentor:
            # Optional: Add custom validation here, e.g., to prevent assigning the mentor
            # who was originally requested if they rejected it, or if the mentee
            # already has an active assignment.
            # For example, check if the mentee already has an active assignment
            if MentorshipAssignment.objects.filter(mentee=mentorship_request.mentee).exists():
                 self.add_error('mentorship_request', "This mentee already has an active mentor assignment.")

            # Check if the chosen mentor is the same as the one the mentee originally requested
            # if mentorship_request.mentor == mentor:
            #     # This might be fine, but if you want to ensure it's a *new* assignment, you could add a warning.
            #     pass

        return cleaned_data

    def save(self):
        mentorship_request = self.cleaned_data['mentorship_request']
        mentor = self.cleaned_data['mentor']

        # Create the MentorshipAssignment
        assignment = MentorshipAssignment.objects.create(
            mentee=mentorship_request.mentee,
            mentor=mentor,
            mentorship_request=mentorship_request # Link to the original request
        )

        # Update the status of the original MentorshipRequest
        mentorship_request.status = 'assigned' # Or 'accepted' if that fits your flow
        mentorship_request.save()

        return assignment

# You can also add other forms here, e.g., for creating/updating profiles
# class MentorProfileForm(forms.ModelForm):
#     class Meta:
#         model = MentorProfile
#         fields = ['bio', 'expertise', 'location', 'interests', 'available_for_mentorship']
#
# class MenteeProfileForm(forms.ModelForm):
#     class Meta:
#         model = MenteeProfile
#         fields = ['goals', 'learning_interests']


