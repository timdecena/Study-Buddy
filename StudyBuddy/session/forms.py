# session/forms.py
from django import forms
from .models import Session
from tutors.models import Tutor
from students.models import Student
from Course.models import Course

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['session_name', 'schedule_date', 'time_start', 'tutor', 'student', 'course']
        widgets = {
            'schedule_date': forms.DateInput(attrs={'type': 'date'}),
            'time_start': forms.NumberInput(attrs={'min': 0, 'max': 24}),
        }

    tutor = forms.ModelChoiceField(queryset=Tutor.objects.all(), empty_label="Select Tutor")
    student = forms.ModelChoiceField(queryset=Student.objects.all(), empty_label="Select Student")
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Select Course")
