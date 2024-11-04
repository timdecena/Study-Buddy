from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)  # Unique identifier for each student
    year = models.IntegerField()  # Represents the year level of the student

    def __str__(self):
        return self.student_id
