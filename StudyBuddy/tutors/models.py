from django.utils import timezone
from django.db import models

class Tutor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)  # Added username field
    password = models.CharField(max_length=128)  # Added password field
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# models.py
from django.db import models
from tutors.models import Tutor  # Import relevant models
from students.models import Student


class Assignment(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="assignments")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="assignments", default=1)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    file_upload = models.FileField(upload_to='assignments/', null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)  # Store grade out of 100
    grade_submission_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.tutor})"