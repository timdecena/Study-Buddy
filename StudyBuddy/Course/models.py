# Course/models.py
from django.db import models
from Subject.models import Subject

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=50)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)  # Allow null temporarily

    def __str__(self):
        return f"{self.course_name} ({self.subject.subject_name if self.subject else 'No Subject'})"
