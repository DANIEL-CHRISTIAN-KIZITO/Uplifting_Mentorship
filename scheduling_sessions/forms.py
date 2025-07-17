# scheduling_sessions/forms.py
from django import forms
from .models import SessionProposal
from django.utils import timezone

class SessionProposalForm(forms.ModelForm):
    """Form for proposing a new session time."""
    # These fields will be hidden and set in the view
    mentee = forms.ModelChoiceField(queryset=None, widget=forms.HiddenInput(), required=False)
    mentor = forms.ModelChoiceField(queryset=None, widget=forms.HiddenInput(), required=False)
    proposed_by = forms.ModelChoiceField(queryset=None, widget=forms.HiddenInput(), required=False)

    # User-visible fields
    proposed_start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="Proposed Start Time",
        help_text="Format: YYYY-MM-DD HH:MM (e.g., 2025-07-20 14:30)"
    )
    proposed_end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="Proposed End Time",
        help_text="Format: YYYY-MM-DD HH:MM (e.g., 2025-07-20 15:30)"
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        required=False,
        label="Message (optional)"
    )

    class Meta:
        model = SessionProposal
        fields = ['proposed_start_time', 'proposed_end_time', 'message', 'mentee', 'mentor', 'proposed_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set queryset for hidden fields dynamically in the view if needed, or remove if always set in view
        # self.fields['mentee'].queryset = MenteeProfile.objects.all()
        # self.fields['mentor'].queryset = MentorProfile.objects.all()
        # self.fields['proposed_by'].queryset = User.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('proposed_start_time')
        end_time = cleaned_data.get('proposed_end_time')

        if start_time and end_time:
            if start_time >= end_time:
                self.add_error('proposed_end_time', "End time must be after start time.")
            if start_time < timezone.now():
                self.add_error('proposed_start_time', "Start time cannot be in the past.")
        return cleaned_data

class SessionProposalResponseForm(forms.Form):
    """Form for accepting or rejecting a session proposal."""
    action = forms.ChoiceField(
        choices=[('accept', 'Accept'), ('reject', 'Reject')],
        widget=forms.RadioSelect,
        label="Action"
    )
    # Optional: Add a message field for rejection reasons
    # rejection_message = forms.CharField(
    #     widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
    #     required=False,
    #     label="Reason for rejection (optional)"
    # )
