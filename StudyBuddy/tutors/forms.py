from django import forms
from .models import Assignment, Tutor
from students.models import Student

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description']

class AssignStudentForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label="Assign to Student")

class TutorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['first_name', 'last_name', 'username', 'password', 'email']  # Add any other fields you need
        widgets = {
            'password': forms.PasswordInput(),
        }
