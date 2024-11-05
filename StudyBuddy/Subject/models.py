# Subject/models.py
from django.db import models

class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=200)

    def __str__(self):
        return self.subject_name
