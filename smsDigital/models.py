
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class SMSLog(models.Model):
    mobile_number = models.CharField(max_length=15)
    message = models.TextField()
    status = models.CharField(max_length=250)  # Sent, Failed, etc.
    sent_at = models.DateTimeField()
    response = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this field

    def __str__(self):
        return f"{self.mobile_number} - {self.status} - Sent by {self.user.username}"

#User
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sms_count = models.PositiveIntegerField(default=10)  # Default limit can be set to any number

    def __str__(self):
        return f"{self.user.username} - SMS Count: {self.sms_count}"

# Add signals to automatically create/update UserProfile when User is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()