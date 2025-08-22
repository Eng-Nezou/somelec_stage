from django.contrib import admin
from .models import Employer,Ordonnance,Medicament, Produit, Reference, Utilisateur
from .models import Institution, Consultation, Analyse, Examen, Hospitalisation, Scanner, Echographie, Radiographie, Irm
# Register your models here.


class EmployerAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'date_naissance', 'matricule', 'inam')
    search_fields = ('nom', 'prenom', 'matricule','inam')
admin.site.register(Employer, EmployerAdmin)

admin.site.register(Ordonnance)
admin.site.register(Medicament)
admin.site.register(Utilisateur)
admin.site.register(Reference)
admin.site.register(Institution)
admin.site.register(Consultation)   
admin.site.register(Analyse)
admin.site.register(Examen)
admin.site.register(Hospitalisation)
admin.site.register(Scanner)
admin.site.register(Echographie)
admin.site.register(Radiographie)
admin.site.register(Irm)
admin.site.register(Produit)