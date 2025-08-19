from django.urls import path

from infermerieapp.views import *

urlpatterns = [
    path('login/',auth_login),
    path('logout/',auth_logout),
    path('dashbord/',gestionnaire),
    path('filtre/', filter_employers),
    path('pris_charge/', pris_en_charge, name='pris_en_charge'),
    path('referencer/pris_en_charge', referencer_pris_en_charge, name='referencer'),
    path('referencer/supprimer', supprimer, name='supprimer'),
    path('ordonnance/', ordonnance_view, name='ordonnance'),
    path('ordonnance/generate/', ordonnance_generate, name='ordonnance_generate'),
    path('liste_ordonnances/', liste_ordonnances, name='liste_ordonnances'),
    path('ordonnances/<int:pk>/', ordonnance_modifier, name='ordonnances'),
    path('ordonnance/pdf/<int:pk>/', voire_ordonnance, name='ordonnance_terminer'),
    path('liste_ordonnances/chef/', chef, name='liste_ordonnances'),
    path('liste_ordonnances/medecin/', medecin, name='liste_ordonnances_medecin'),
    path('tableau_referencer/' , tableau_referencer)
]