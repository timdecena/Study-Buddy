from django import forms
from .models import Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name']
        labels = {
            'subject_name': '',  # Set an empty label
        }
        widgets = {
            'subject_name': forms.TextInput(attrs={'placeholder': 'Enter here'}),
        }
