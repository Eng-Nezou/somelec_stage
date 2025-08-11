from django.urls import path

from infermerieapp.views import *

urlpatterns = [
    path('login/',auth_login),
    path('dashbord/',gestionnaire),
    path('filtre/', filter_employers),
    path('ordonnance/', ordonnance_view, name='ordonnance'),
    path('ordonnance/generate/', ordonnance_generate, name='ordonnance_generate'),
    path('liste_ordonnances/', liste_ordonnances, name='liste_ordonnances'),
    path('ordonnances/<int:pk>/', ordonnance_modifier, name='ordonnances'),
    path('ordonnance/pdf/<int:pk>/', voire_ordonnance, name='ordonnance_terminer'),
    path('liste_ordonnances/chef/', chef, name='liste_ordonnances')
]