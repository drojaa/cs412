#
# project/models.py
# Define the data objects for our application
#

from django.db import models

# Create your models here.

class ClothingItem(models.Model):
    '''Represents a single clothing item in the wardrobe.'''
    
    # Clothing type choices
    CLOTHING_TYPES = [
        ('top', 'Top'),
        ('dresses', 'Dresses'),
        ('bottom', 'Bottom'),
        ('shoes', 'Shoes'),
        ('accessory', 'Accessory'),
        ('outerwear', 'Outerwear'),
    ]
    
    # data attributes of a ClothingItem:
    name = models.TextField(blank=False)
    type = models.CharField(max_length=10, choices=CLOTHING_TYPES)
    color = models.TextField()
    image = models.ImageField()
    
    def __str__(self):
        '''Return a string representation of this ClothingItem.'''
        return f'{self.name} ({self.get_type_display()}) - {self.color}'

class Outfit(models.Model):
    '''Represents a complete outfit created from clothing items.'''
    
    # data attributes of an Outfit:
    name = models.TextField(blank=False)
    date_created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        '''Return a string representation of this Outfit.'''
        return f'{self.name}'

class OutfitItem(models.Model):
    '''Connects multiple clothing items to a single outfit.'''
    
    # data attributes of an OutfitItem:
    outfit = models.ForeignKey(Outfit, on_delete=models.CASCADE, related_name='outfit_items')
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE)
    
    def __str__(self):
        '''Return a string representation of this OutfitItem.'''
        return f'{self.clothing_item.name} in {self.outfit.name}'

class Event(models.Model):
    '''Represents an event with optional outfit selection.'''
    
    # data attributes of an Event:
    name = models.CharField(max_length=100)
    event_date = models.DateField()
    location = models.CharField(max_length=100)
    outfit = models.ForeignKey(Outfit, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    
    def __str__(self):
        '''Return a string representation of this Event.'''
        return f'{self.name} on {self.event_date}'
