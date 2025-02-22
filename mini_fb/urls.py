#url paths for mini_fb project


from django.urls import path
from django.conf import settings
from .views import ShowAllProfilesView
from .views import ShowAllProfilePageView

urlpatterns = [
   path('', ShowAllProfilesView.as_view(), name="show_all_profiles"), 
   path('profile/<int:pk>', ShowAllProfilePageView.as_view(), name="show_profile")
]