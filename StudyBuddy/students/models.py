# students/models.py

from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)  # Unique identifier for each student
    fullname = models.CharField(max_length=100, default="Default Full Name") # Full name of the student
    year = models.IntegerField()  # Represents the year level of the student
    course = models.CharField(max_length=50, default="Default Course")  # Course enrolled
    section = models.CharField(max_length=10, default="Default Section")  # Section of the student

    def __str__(self):
        return f"{self.student_id} - {self.fullname}"
