#url paths for mini_fb project


from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
   path('', ShowAllProfilesView.as_view(), name="show_all_profiles"), 
   path('profile/<int:pk>', ShowAllProfilePageView.as_view(), name="show_profile"),
   path('profile/create', CreateProfileView.as_view(), name="create_profile")
]