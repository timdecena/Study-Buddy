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
from tutors.models import Tutor  # Assuming the Tutor model is in the tutors app

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)  # Link each assignment to a tutor

    def __str__(self):
        return self.title
