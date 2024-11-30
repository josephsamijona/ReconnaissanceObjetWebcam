# logic/models.py

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    """
    Extends the default Django User model to include additional information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    huggingface_api_key = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
