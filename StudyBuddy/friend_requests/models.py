from django.db import models
from students.models import Student
from tutors.models import Tutor

class FriendRequest(models.Model):
    # Define sender and receiver as generic fields for flexibility
    sender_student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='sent_requests'
    )
    sender_tutor = models.ForeignKey(
        Tutor, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='sent_requests'
    )
    receiver_student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='received_requests_student'
    )
    receiver_tutor = models.ForeignKey(
        Tutor, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='received_requests_tutor'
    )

    # Define status options
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'), 
            ('accepted', 'Accepted'), 
            ('declined', 'Declined')
        ],
        default='pending'
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.sender_student or self.sender_tutor} to {self.receiver_student or self.receiver_tutor}"

    @property
    def sender(self):
        """Retrieve sender regardless of type."""
        return self.sender_student or self.sender_tutor

    @property
    def receiver(self):
        """Retrieve receiver regardless of type."""
        return self.receiver_student or self.receiver_tutor
