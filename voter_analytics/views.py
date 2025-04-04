"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-04-2
Description: Defines Profile and StatusMessage Model
"""
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
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
    



    def get_queryset(self):
        '''filter voter data based on any combination of criteria'''
        base_queryset = super().get_queryset()
        
        # Get filter parameters from GET request
        party = self.request.GET.get('party')
        min_year = self.request.GET.get('min_year')
        max_year = self.request.GET.get('max_year')
        voter_score = self.request.GET.get('voter_score')
        v20state = self.request.GET.get('v20state')
        v21town = self.request.GET.get('v21town')
        v21primary = self.request.GET.get('v21primary')
        v23town = self.request.GET.get('v23town')

        queryset = base_queryset

        # Apply filters only if they are provided (not empty)
        if party:
            # Add space to match 2-character width format in database
            party_padded = f"{party:<2}"  # Left-align and pad to 2 chars with space
            queryset = queryset.filter(party_affiliation=party_padded)
        
        if min_year:
            queryset = queryset.filter(date_of_birth__year__gte=int(min_year))
        
        if max_year:
            queryset = queryset.filter(date_of_birth__year__lte=int(max_year))
        
        if voter_score:
            queryset = queryset.filter(voter_score=int(voter_score))
        
        # Boolean filters - only apply if checkbox is checked
        if v20state:
            queryset = queryset.filter(v20state='TRUE')
        
        if v21town:
            queryset = queryset.filter(v21town='TRUE')
        
        if v21primary:
            queryset = queryset.filter(v21primary='TRUE')
        
        if v23town:
            queryset = queryset.filter(v23town='TRUE')

        return queryset.order_by('last_name', 'first_name')  # Add ordering to avoid pagination warning

class SingleVoterView(DetailView):
    '''View to display a single voter'''
    model = Voter
    template_name = "voter_analytics/voter.html"
    context_object_name = "voter"

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            # Redirect to the voters list page with an error message
            return redirect(reverse('voters'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time'] = time.ctime()  # Add time to context
        return context
    
