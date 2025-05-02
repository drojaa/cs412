"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-02-27
Description: Urls for Closet project
"""


from django.urls import path
from . import views

urlpatterns = [
    path('clothing/', views.ShowAllClothingItem.as_view(), name='show_all_clothing_items'),
    path('outfits/', views.ShowAllOutfits.as_view(), name='show_all_outfits'),
    path('events/', views.ShowAllEvents.as_view(), name='show_all_events'),
    path('clothing/create/', views.CreateClothingView.as_view(), name='create_clothing'),
    path('outfits/create/', views.CreateOutfitView.as_view(), name='create_outfit'),
    path('events/create/', views.CreateEventView.as_view(), name='create_event'),
    path('events/update/<int:pk>/', views.UpdateEventView.as_view(), name='update_event'),
    path('events/delete/<int:pk>/', views.DeleteEventView.as_view(), name='delete_event'),
    path('outfit/<int:pk>/', views.OutfitDetailView.as_view(), name='outfit_detail'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('outfits/update/<int:pk>/', views.UpdateOutfitView.as_view(), name='update_outfit'),
    path('outfits/delete/<int:pk>/', views.DeleteOutfitView.as_view(), name='delete_outfit'),
]
