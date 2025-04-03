"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-04-2
Description: Defines Profile and StatusMessage Model
"""
from django.shortcuts import render
from django.views.generic import ListView
from . models import Voter
import time

class VoterListView(ListView):
    '''View to display voter information'''
    model = Voter
    template_name = "voter_analytics/voters.html"
    paginate_by = 25
    context_object_name = "voters"

    def get_context_data(self, **kwargs):
        '''Add additional context variables'''
        context = super().get_context_data(**kwargs)
        context['time'] = time.ctime()
        return context
    



    # def get_queryset(self):
    #     '''limit the result queryset (for now)'''
    #     voters = super().get_queryset()
    #     return voters[:25] # slice to return first 25 records 
    

    
