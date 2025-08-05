from django.urls import path

from infermerieapp.views import *

urlpatterns = [
    path('login/',auth_login),
    path('dashbord/',gestionnaire),
    path('filtre/', filter_employers)  # Assuming you have a view for filtering employers
]