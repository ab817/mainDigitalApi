from django.db import models

class SMSLog(models.Model):
    mobile_number = models.CharField(max_length=15)
    message = models.TextField()
    status = models.CharField(max_length=10)  # Sent, Failed, etc.
    sent_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.mobile_number} - {self.status}"