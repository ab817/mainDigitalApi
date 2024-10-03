from django.db import models
from django.contrib.auth.models import User

class SMSLog(models.Model):
    mobile_number = models.CharField(max_length=15)
    message = models.TextField()
    status = models.CharField(max_length=250)  # Sent, Failed, etc.
    sent_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this field

    def __str__(self):
        return f"{self.mobile_number} - {self.status} - Sent by {self.user.username}"