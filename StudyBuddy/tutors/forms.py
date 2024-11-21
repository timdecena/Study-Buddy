from django import forms
from .models import Assignment
from students.models import Student

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description']

class AssignStudentForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label="Assign to Student")
