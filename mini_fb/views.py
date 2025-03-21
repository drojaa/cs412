"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-02-27
Description: Functions to display singular Profiles, all Profiles, and forms to 
publish a status and create a new profile
"""

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, Image, StatusImage, StatusMessage, Friend
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
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
    
class UpdateProfileView(UpdateView):
        model = Profile
        form_class = UpdateProfileForm
        template_name = "mini_fb/update_profile_form.html"

class DeleteStatusMessageView(DeleteView):
    '''View class to handle updating a status message'''
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"

    def get_success_url(self):
        '''Returns URL to redirect'''
        pk = self.kwargs['pk']
        statusmessage = StatusMessage.objects.get(pk=pk)
        profile = statusmessage.profile
        #call reverse function
        return reverse('show_profile', kwargs={'pk': profile.pk})

class UpdateStatusMessageView(UpdateView):
    '''View class to handle updating a status message'''
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"

    def get_success_url(self):
        '''Returns URL to redirect'''
        pk = self.kwargs['pk']
        statusmessage = StatusMessage.objects.get(pk=pk)
        profile = statusmessage.profile
        #call reverse function
        return reverse('show_profile', kwargs={'pk': profile.pk})


class AddFriendView(View):
    '''View class to handle adding friends to a Profile'''
    model = Friend
    template_name = "mini_fb/show_profile.html"
   
    def dispatch(self, request, *args, **kwargs):
       pk1 = self.kwargs['pk']
       pk2 = self.kwargs['other_pk']

       profile1 = Profile.objects.get(pk = pk1)
       profile2 = Profile.objects.get(pk = pk2)

       Profile.add_friend(profile1, profile2)

       return redirect(reverse('show_profile', kwargs={'pk': pk1}))

 

class ShowFriendSuggetionsView(DetailView):
    '''View class to show friend suggestions'''
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"