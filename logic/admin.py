# logic/admin.py

from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile.
    """
    list_display = ('user', 'huggingface_api_key')
    search_fields = ('user__username', 'huggingface_api_key')
