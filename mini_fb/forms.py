from django import forms
from .models import Profile, StatusMessage
#defines the forms we use CRUD

class CreateProfileForm(forms.ModelForm):
    '''A form to add Profile to the database'''
     

    class Meta:
        '''assocate this form with a model to our database'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image']
    
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email = forms.EmailField(label="Email", required=True)
    image = forms.CharField(label="Profile Picture", required=True)
