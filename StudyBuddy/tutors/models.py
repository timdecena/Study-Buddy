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

from django.db import models

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title