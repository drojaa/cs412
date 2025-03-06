"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-02-27
Description: Functions to display singular Profiles, all Profiles, and forms to 
publish a status and create a new profile
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Image, StatusImage
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse
# Create your views here.
import time
# function is used to display all profiles at once
class ShowAllProfilesView(ListView):
    '''Define a view class to show all Profiles'''

    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"
   
# function is used display a single profile
class ShowAllProfilePageView(DetailView):
    '''Define a view class to show a signle profile'''

    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

# fedine a subclass of CreateView to handle creation of Profile Object
class CreateProfileView(CreateView):
    '''Display HTML form to user and process submission to store'''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"
    def get_success_url(self):

        '''Provide a URL to redirect after creating a new comment'''
        '''Inspects data and find foreign key of article and attatching it'''
        pk = self.kwargs['pk']

        #call reverse function
        return reverse('show_profile', kwargs={'pk': pk})
    def get_context_data(self):
        '''Returm dictionary of context variables'''
        context = super().get_context_data()
        # find/add the article
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk = pk)

        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Inspects data and find foreign key of article and attatching it'''
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk = pk)
        form.instance.profile = profile 
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for file in files:
            #each file in files holds the url each img
            image = Image(profile=profile, img_file=file)
            image.save()
            status_image = StatusImage(img_file=image, stat_msg=sm)
            status_image.save()

        #delegate the work to the superclass
        return super().form_valid(form)
    
