"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-02-27
Description: Defines Profile and StatusMessage Model
"""

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
    image_file = models.TextField(blank=True)

    def __str__(self):
        '''Return a string representation of this Profile object.'''
        return f'{self.first_name} {self.last_name}'
    def get_status_messages(self):
        '''returns all messages for specifc Profile'''
        status_messages = StatusMessage.objects.filter(profile=self).order_by('-timestamp')
        return status_messages
    def get_absolute_url(self):
        '''Return a URL to display once instance of this object'''
        return reverse('show_profile', kwargs={'pk':self.pk})
    def get_friends(self):
        '''Return a List of given profile's friends'''
        friend_list = []
        friends = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)
        '''Checks if the friend isn't already inside the list'''
        '''Checks if profile1 or profile2 isn't the self object'''
        for friend in friends:
            if friend.profile1 not in friend_list:
                if self.first_name != friend.profile1.first_name:
                    if self.last_name != friend.profile1.last_name:
                         prof_friend = Profile.objects.get(first_name=friend.profile1.first_name, last_name=friend.profile1.last_name)
                         friend_list.append(prof_friend)
            if friend.profile2 not in friend_list:
                if self.first_name != friend.profile2.first_name:
                    if self.last_name != friend.profile2.last_name:
                        prof_friend = Profile.objects.get(first_name=friend.profile2.first_name, last_name=friend.profile2.last_name) 
                        friend_list.append(prof_friend)
        return friend_list
    
    def add_friend(self, other):
        '''Add Profile as a Friend'''
        all_friends = Friend.objects.all()
        for f in all_friends:
            if self != other:
                if not((f.profile1 == self or f.profile2 == self) and (f.profile1 == other or f.profile2 == other)):
                    new_friends = Friend(profile1=self, profile2=other)
                    new_friends.save()
                else:
                    print("Already are Friends!")
                

    
    def get_friend_suggestions(self):
        '''Get friend suggestion for an instance of a Profile'''
        prof_friends = Profile.get_friends(self)
        all_profiles = Profile.objects.all()
        prof_list = []
        for prof in all_profiles:
            if prof not in prof_friends and prof != self:
                print(prof)
                prof_list.append(prof)

        return prof_list 









       
class StatusMessage(models.Model): 
    '''Encapsulate the data of Facebook Status Message for each Profile'''

    # define the data attributes of the Profile object 
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp =  models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    
    def __str__(self):
        '''Returns a string representation of this Status Message'''
        return f'{self.message}'

    def get_images(self):
        '''Returns all images associated with this Status Message'''
        all_imgs = StatusImage.objects.filter(stat_msg=self)
        return all_imgs
    
   
class Image(models.Model):
    '''Encap Image for Status Message'''
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    img_file = models.ImageField(blank=True) # an actual image
    timestamp =  models.DateTimeField(auto_now=True)

class StatusImage(models.Model):
    '''Encap Image for Status Message'''
    img_file = models.ForeignKey(Image, on_delete=models.CASCADE)
    stat_msg = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)

class Friend(models.Model):
    '''Encaps the Friend relationship amongst Profiles'''
    profile1 =  models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 =  models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    timestamp =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile1} and  {self.profile2}'