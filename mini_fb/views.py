from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile
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
   