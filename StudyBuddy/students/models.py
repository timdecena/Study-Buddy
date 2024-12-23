from django.db import models
from Course.models import Course  # Import the Course model

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Reference to the Course model
    year = models.IntegerField()
    section = models.CharField(max_length=100)
    username = models.CharField(max_length=255, null=True, blank=True,unique=True)  # Temporarily allow null values


    password = models.CharField(max_length=128, default="default_password")
    profile_image = models.ImageField(upload_to='profile_pics/',null=True,blank=True,default='profile_pics/default.jpg')  # Set a default image
    status = models.CharField(max_length=20, choices=[('accepted', 'Accepted'), ('pending', 'Pending')], default='pending')



    def __str__(self):
        return self.fullname