#voter_analytics/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.VoterListView.as_view(), name="voters"),
    path('voters', views.VoterListView.as_view(), name="voter"),
    path('voter/<int:pk>', views.SingleVoterView.as_view(), name="voter"),
]