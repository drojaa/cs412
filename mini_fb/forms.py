"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-02-27
Description: Defines the forms we use CRUD with
"""
from django import forms
from .models import Profile, StatusMessage


class CreateProfileForm(forms.ModelForm):
    '''A form to add Profile to the database'''
     

    class Meta:
        '''assocate this form with a model to our database'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_file']
    
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email = forms.EmailField(label="Email", required=True)
    image_file = forms.CharField(label="Profile Picture", required=True)

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add Status message to database'''
    class Meta:
        '''associate this form with a model to our database'''
        model = StatusMessage
        fields = ["message"]
    message = forms.CharField(
        label="Message",
        required=True,
        widget=forms.Textarea(attrs={"rows": 4, "cols": 50})  # Optional: Adjust size
    )
    
class UpdateProfileForm (forms.ModelForm):
    '''A form to update indiv user Profile'''
    class Meta:
        '''associate this form with a model to our database'''
        model = Profile
        fields = ['city', 'email', 'image_file']
    city = forms.CharField(label="City", required=False)
    email = forms.EmailField(label="Email", required=False)
    image_file = forms.CharField(label="Profile Picture", required=False)

