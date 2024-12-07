from django import forms
from .models import Student
from tutors.models import Assignment
from .models import Course


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
    
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Select Course")


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['file_upload']  # Only allow file upload field to be updated