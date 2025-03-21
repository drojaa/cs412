"""
Author: Derinell Rojas
Email: droja@bu.edu
Date: 2025-02-27
Description: Urls for mini_fb project
"""


from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
   path('', ShowAllProfilesView.as_view(), name="show_all_profiles"), 
   path('profile/create', CreateProfileView.as_view(), name="create_profile"),
   path('profile/<int:pk>', ShowAllProfilePageView.as_view(), name="show_profile"),
   path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"),
   path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"),
   path('statusmessage/<int:pk>/update', UpdateStatusMessageView.as_view(), name="update_status"),
   path('statusmessage/<int:pk>/delete', DeleteStatusMessageView.as_view(), name="delete_status"),
   path('profile/<int:pk>/add_friend/<int:other_pk>', AddFriendView.as_view(), name="add_friend"),
   path('profile/<int:pk>/friend_suggestions', ShowFriendSuggetionsView.as_view(), name="friend_suggestions"),
]