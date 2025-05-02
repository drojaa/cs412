"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-02-27
Description: Defines the forms we use CRUD with
"""
from django import forms
from .models import ClothingItem, Outfit, Event


class CreateClothingForm(forms.ModelForm):
    '''A form to add Clothing to the database'''
    
    class Meta:
        '''associate this form with a model in our database'''
        model = ClothingItem
        fields = ['name', 'type', 'color', 'image']
    
    name = forms.CharField(label="Name", required=True)
    color = forms.CharField(label="Color", required=True)
    image = forms.ImageField(label="Image", required=True)


class CreateOutfitForm(forms.ModelForm):
    '''A form to add Outfits to the database'''
    
    class Meta:
        '''associate this form with a model in our database'''
        model = Outfit
        fields = ['name']
    
    name = forms.CharField(label="Outfit Name", required=True)
    
    # Add a multiple selection field for clothing items
    clothing_items = forms.ModelMultipleChoiceField(
        queryset=ClothingItem.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Clothing Items"
    )


class CreateEventForm(forms.ModelForm):
    '''Form to create a new Event'''
    
    class Meta:
        model = Event
        fields = ['name', 'event_date', 'location', 'outfit']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g., Birthday Party'}),
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g., Home, Restaurant, etc.'}),
            'outfit': forms.Select(attrs={'class': 'outfit-select'})
        }
        labels = {
            'name': 'Event Name',
            'event_date': 'Date',
            'location': 'Location',
            'outfit': 'Outfit'
        }
