from django.db import models
from tutors.models import Tutor  # Import the Tutor model
from students.models import Student  # Import the Student model
from Course.models import Course  # Import the Course model

class Session(models.Model):
    session_id = models.AutoField(primary_key=True)
    session_name = models.CharField(max_length=100)
    schedule_date = models.DateField()
    time_start = models.TimeField()  # Changed to TimeField
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.session_name
