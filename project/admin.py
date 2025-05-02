"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-02-27
Description: Register models Profile and StatusMessage
"""

from django.contrib import admin

# Register your models here.
from .models import ClothingItem, Outfit, OutfitItem, Event
admin.site.register(ClothingItem)
admin.site.register(Outfit)
admin.site.register(OutfitItem)
admin.site.register(Event)
