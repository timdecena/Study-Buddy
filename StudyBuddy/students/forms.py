from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        max_length=128,
        label="Password"
    )

    class Meta:
        model = Student
        fields = ['fullname', 'course', 'year', 'section', 'username', 'password']
