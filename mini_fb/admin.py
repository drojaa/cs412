"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-02-27
Description: Register models Profile and StatusMessage
"""
from django.contrib import admin

# Register your models here.

from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage
admin.site.register(Profile)
admin.site.register(StatusMessage)



