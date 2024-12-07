from django import forms
from .models import Student
from tutors.models import Assignment


class StudentForm(forms.ModelForm):
    delete_profile_image = forms.BooleanField(required=False, label="Delete Profile Picture")
    password = forms.CharField(
        widget=forms.PasswordInput,
        max_length=128,
        label="Password"
    )

    class Meta:
        model = Student
        fields = ['fullname', 'course', 'year', 'section', 'username', 'password', 'profile_image']

class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['file_upload']  # Only allow file upload field to be updated