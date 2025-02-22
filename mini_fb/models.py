from django.db import models

# Create your models here.

from django.db import models
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
