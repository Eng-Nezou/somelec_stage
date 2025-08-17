from django.contrib import admin
from .models import Employer,Ordonnance,Medicament, Reference, Utilisateur
# Register your models here.


class EmployerAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'date_naissance', 'matricule', 'inam')
    search_fields = ('nom', 'prenom', 'matricule','inam')
admin.site.register(Employer, EmployerAdmin)

admin.site.register(Ordonnance)
admin.site.register(Medicament)
admin.site.register(Utilisateur)
admin.site.register(Reference)