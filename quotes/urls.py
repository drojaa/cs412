

from django.urls import path
from django.conf import settings
from . import views 
# URL pattern list defining the routing of requests to specific views
urlpatterns = [
    path(r'', views.quote, name="quote"),
    path(r'quote', views.quote, name="quote"), 
    path(r'show_all', views.show_all, name="show_all"), 
    path(r'about', views.about, name="about"), 
]
