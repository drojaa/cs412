"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-02-27
Description: Views to display content for Closet project
"""



from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import CreateClothingForm, CreateOutfitForm, CreateEventForm
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import Http404
from django.urls import reverse

# Create your views here.

class ShowAllClothingItem(ListView):
    '''Create a subclass of ListView to display all clothing items.'''

    model = ClothingItem # retrieve objects of type ClothingItem from the database
    template_name = 'project/show_all_clothing_items.html'
    context_object_name = 'clothing' # how to find the data in the template file
    
    def get_queryset(self):
        '''Filter clothing items based on type'''
        base_queryset = super().get_queryset()
        item_type = self.request.GET.get('type')
        
        if item_type and item_type != 'all':
            return base_queryset.filter(type=item_type)
        return base_queryset

class ShowAllOutfits(ListView):
    '''Create a subclass of ListView to display all outfits.'''

    model = Outfit # retrieve objects of type ClothingItem from the database
    template_name = 'project/show_all_outfit.html'
    context_object_name = 'outfit' # how to find the data in the template file
    
    def get_queryset(self):
        '''Filter outfits based on criteria'''
        base_queryset = super().get_queryset()
        filter_type = self.request.GET.get('filter')
        
        if filter_type == 'recent':
            # Show most recently created outfits first
            return base_queryset.order_by('-date_created')
        elif filter_type == 'oldest':
            # Show oldest outfits first
            return base_queryset.order_by('date_created')
        
        # Default ordering (most recent first)
        return base_queryset.order_by('-date_created')

class ShowAllEvents(ListView):
    '''Create a subclass of ListView to display all events.'''

    model = Event # retrieve objects of type Event from the database
    template_name = 'project/show_all_events.html'
    context_object_name = 'events' # how to find the data in the template file
    
    def get_queryset(self):
        '''Filter events based on criteria'''
        base_queryset = super().get_queryset()
        filter_type = self.request.GET.get('filter', 'all')
        
        today = timezone.now().date()
        
        if filter_type == 'upcoming':
            # Show only upcoming events
            return base_queryset.filter(event_date__gte=today).order_by('event_date')
        elif filter_type == 'past':
            # Show only past events
            return base_queryset.filter(event_date__lt=today).order_by('-event_date')
        elif filter_type == 'this_week':
            # Show events in the next 7 days
            next_week = today + timedelta(days=7)
            return base_queryset.filter(event_date__gte=today, event_date__lte=next_week).order_by('event_date')
        elif filter_type == 'this_month':
            # Show events in the next 30 days
            next_month = today + timedelta(days=30)
            return base_queryset.filter(event_date__gte=today, event_date__lte=next_month).order_by('event_date')
        elif filter_type == 'has_outfit':
            # Show only events with an outfit assigned
            return base_queryset.filter(outfit__isnull=False).order_by('event_date')
        elif filter_type == 'no_outfit':
            # Show only events without an outfit assigned
            return base_queryset.filter(outfit__isnull=True).order_by('event_date')
        
        # Default: show all events ordered by date (upcoming first)
        return base_queryset.order_by('event_date')
    
    def get_context_data(self, **kwargs):
        '''Add filter information to context'''
        context = super().get_context_data(**kwargs)
        context['current_filter'] = self.request.GET.get('filter', 'all')
        context['today'] = timezone.now().date()
        return context


class CreateClothingView(CreateView):
    '''Display HTML form to user and process submission to store'''
    model = ClothingItem
    form_class = CreateClothingForm
    template_name = "project/create_clothing_form.html"
    success_url = reverse_lazy('show_all_clothing_items')
    
    def get_context_data(self, **kwargs):
        '''Add additional context data'''
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        '''Process the form submission'''
        # Save the form data to create a new ClothingItem
        self.object = form.save()
        return super().form_valid(form)

class CreateOutfitView(CreateView):
    '''Display HTML form to user and process submission to store an outfit'''
    model = Outfit
    form_class = CreateOutfitForm
    template_name = "project/create_outfit_form.html"
    success_url = reverse_lazy('show_all_outfits')
    
    def form_valid(self, form):
        '''Process the form submission'''
        # First save the outfit
        self.object = form.save()
        
        # Then create OutfitItem objects for each selected clothing item
        clothing_items = form.cleaned_data.get('clothing_items')
        for item in clothing_items:
            OutfitItem.objects.create(outfit=self.object, clothing_item=item)
            
        return super().form_valid(form)

class CreateEventView(CreateView):
    '''Display HTML form to user and process submission to store an event'''
    model = Event
    form_class = CreateEventForm
    template_name = "project/create_event_form.html"
    success_url = reverse_lazy('show_all_events')
    
    def form_valid(self, form):
        '''Process the form submission'''
        # Save the event
        self.object = form.save()
        return super().form_valid(form)

class UpdateEventView(UpdateView):
    '''Display HTML form to update an existing event'''
    model = Event
    form_class = CreateEventForm
    template_name = "project/update_event_form.html"
    success_url = reverse_lazy('show_all_events')
    
    def form_valid(self, form):
        '''Process the form submission'''
        # Save the event
        self.object = form.save()
        return super().form_valid(form)

class DeleteEventView(DeleteView):
    '''View to delete an event'''
    model = Event
    template_name = "project/delete_event_confirm.html"
    success_url = reverse_lazy('show_all_events')
    context_object_name = 'event'

class OutfitDetailView(DetailView):
    '''Display details of a specific outfit'''
    model = Outfit
    template_name = 'project/outfit_detail.html'
    context_object_name = 'outfit'
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            # Redirect to the outfits list page if outfit not found
            return redirect(reverse('show_all_outfits'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get events that use this outfit
        context['events'] = Event.objects.filter(outfit=self.object)
        return context

class EventDetailView(DetailView):
    '''Display details of a specific event'''
    model = Event
    template_name = 'project/event_detail.html'
    context_object_name = 'event'
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            # Redirect to the events list page if event not found
            return redirect(reverse('show_all_events'))

class UpdateOutfitView(UpdateView):
    '''Display HTML form to update an existing outfit'''
    model = Outfit
    form_class = CreateOutfitForm  # You can reuse the same form or create a specific update form
    template_name = "project/update_outfit_form.html"
    success_url = reverse_lazy('show_all_outfits')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add selected clothing items to context
        context['selected_items'] = [item.clothing_item.id for item in self.object.outfit_items.all()]
        return context
    
    def form_valid(self, form):
        '''Process the form submission'''
        # First save the outfit
        self.object = form.save()
        
        # Remove all existing outfit items
        self.object.outfit_items.all().delete()
        
        # Then create OutfitItem objects for each selected clothing item
        clothing_items = form.cleaned_data.get('clothing_items')
        for item in clothing_items:
            OutfitItem.objects.create(outfit=self.object, clothing_item=item)
            
        return super().form_valid(form)

class DeleteOutfitView(DeleteView):
    '''Display confirmation before deleting an outfit'''
    model = Outfit
    template_name = "project/delete_outfit_form.html"
    success_url = reverse_lazy('show_all_outfits')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get events that use this outfit
        context['events'] = Event.objects.filter(outfit=self.object)
        return context
