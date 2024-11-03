# Course/models.py
from django.db import models

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.course_name
