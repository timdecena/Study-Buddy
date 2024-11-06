from django.db import models
from tutors.models import Tutor


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    payment_method = models.CharField(max_length=50)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.student} to {self.tutor}"
