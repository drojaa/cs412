from django.db import models

# Create your models here.

from django.db import models
from django.urls import reverse
import time
# Define data models for mini_fb
# Create your models here.

class Profile(models.Model):
    '''Encapsulate the data of indivisual Facebook users'''

    # define the data attributes of the Profile object 
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.TextField(blank=True)
    image = models.TextField(blank=True)

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name}'
    def get_status_messages(self):
        '''returns all messages for specifc Profile'''
        status_messages = StatusMessage.objects.filter(profile=self).order_by('timestamp')
        return status_messages
    def get_absolute_url(self):
        '''Return a URL to display once instance of this object'''
        return reverse('show_profile', kwargs={'pk':self.pk})

class StatusMessage(models.Model): 
    '''Encapsulate the data of Facebook Status Message for each Profile'''

    # define the data attributes of the Profile object 
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp =  models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    
    def __str__(self):
        '''Returns a string representation of this Status Message'''
        return f'{self.message}'