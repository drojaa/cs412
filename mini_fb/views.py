"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-02-27
Description: Functions to display singular Profiles, all Profiles, and forms to 
publish a status and create a new profile
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .models import Profile, Image, StatusImage, StatusMessage, Friend
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusMessageForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin #for authentications
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.
import time
# function is used to display all profiles at once
class ShowAllProfilesView(ListView):
    '''Define a view class to show all Profiles'''

    model = Profile
    template_name = "mini_fb/show_all_profiles.html"
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        '''Override dispatch method to add deubugging information'''

        if request.user.is_authenticated:
            print(f'ShowAllProfilesView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllProfilesView.dispatch(): not logged in')
        return super().dispatch(request, *args, **kwargs)
   
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        context['user_creation_form'] = UserCreationForm()
        return context
    def form_valid(self, form):
        '''Process the form submission and create both User and Profile'''
        # Create User instance from POST data
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            # Save the User instance
            user = user_form.save()
            
            # Log the user in
            login(self.request, user)
            
            # Attach User to Profile
            form.instance.user = user
            
            # Let the superclass handle the rest
            return super().form_valid(form)
        
        # If user form is not valid, re-render the template with errors
        return self.form_invalid(form)


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_success_url(self):
        '''Return URL to redirect to after successful creation'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

    def form_valid(self, form):
        '''Process the form submission'''
        form.instance.profile = self.request.user.profile_set.first()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        '''Return dictionary of context variables'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user.profile_set.first()
        return context
    def get_context_data(self):
        '''Returm dictionary of context variables'''
        context = super().get_context_data()
        # find/add the article
        profile = Profile.get_object(self)
       

        context['profile'] = profile
        return context

    def form_valid(self, form):
        '''Inspects data and find foreign key of article and attatching it'''
        profile = Profile.get_object(self)
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
    
   
    
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_object(self):
        '''Get the profile object for the logged-in user'''
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        '''Return URL to redirect to after successful update'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        '''Add profile to context'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_object()
        return context
          
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''View class to handle deleting a status message'''
    model = StatusMessage
    template_name = "mini_fb/delete_status_form.html"

    def get_object(self, queryset=None):
        '''Get the status message object and verify ownership'''
        obj = super().get_object(queryset)
        # Verify the user owns this status message
        if obj.profile.user != self.request.user:
            raise PermissionDenied
        return obj

    def get_success_url(self):
        '''Returns URL to redirect to after successful deletion'''
        profile_pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': profile_pk})

    def get_context_data(self, **kwargs):
        '''Add status message to context'''
        context = super().get_context_data(**kwargs)
        context['statusmessage'] = self.get_object()
        return context

    def delete(self, request, *args, **kwargs):
        '''Handle the deletion of the status message'''
        try:
            self.object = self.get_object()
            profile_pk = self.object.profile.pk
            self.object.delete()
            return redirect('show_profile', pk=profile_pk)
        except StatusMessage.DoesNotExist:
            # If status message doesn't exist, redirect to user's profile
            return redirect('show_profile', pk=request.user.profile_set.first().pk)

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''View class to handle updating a status message'''
    model = StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"

    def get_success_url(self):
        '''Returns URL to redirect to after successful update'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

    def get_object(self, queryset=None):
        '''Get the status message object and verify ownership'''
        status_message = super().get_object(queryset)
        
        return status_message

    def get_context_data(self, **kwargs):
        '''Add status message to context'''
        context = super().get_context_data(**kwargs)
        context['statusmessage'] = self.get_object()
        return context


class AddFriendView(LoginRequiredMixin, View):
    '''View class to handle adding friends to a Profile'''
    model = Friend
    template_name = "mini_fb/show_profile.html"

    def dispatch(self, request, *args, **kwargs):
        '''Handle adding a friend relationship'''
        # Get the current user's profile
        profile1 = request.user.profile_set.first()
        # Get the profile to be added as friend
        profile2 = Profile.objects.get(pk=kwargs['other_pk'])

        # Add the friend relationship
        Profile.add_friend(profile1, profile2)

        # Redirect back to the current user's profile
        return redirect(reverse('show_profile', kwargs={'pk': profile1.pk}))



class ShowFriendSuggetionsView(LoginRequiredMixin, DetailView):
    '''View class to show friend suggestions'''
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

    def get_object(self):
        '''Get the profile object for the logged-in user'''
        return self.request.user.profile_set.first()

class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    '''View class to show news feed of profile instance and friends stats'''
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"

    def get_object(self):
        '''Get the profile object for the logged-in user'''
        return self.request.user.profile_set.first()
