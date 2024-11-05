# Course/forms.py
from django import forms
from .models import Course
from Subject.models import Subject

class CourseForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), empty_label="Select Subject")  # Add subject dropdown

    class Meta:
        model = Course
        fields = ['course_name', 'course_code', 'description', 'subject']
