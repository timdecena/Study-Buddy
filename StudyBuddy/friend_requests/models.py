from django.db import models
from students.models import Student
from tutors.models import Tutor

class FriendRequest(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when created
    accepted_at = models.DateTimeField(null=True, blank=True)
    declined_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    def __str__(self):
        return f"Friend request from {self.student} to {self.tutor} - Status: {self.status}"

    # Method to update status to accepted
    def accept(self):
        self.status = self.ACCEPTED
        self.accepted_at = models.DateTimeField(auto_now=True)
        self.save()

    # Method to update status to declined
    def decline(self):
        self.status = self.DECLINED
        self.declined_at = models.DateTimeField(auto_now=True)
        self.save()
