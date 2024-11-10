from django.db import models

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)  # Use AutoField if you want an integer ID
    fullname = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year = models.IntegerField()
    section = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname
