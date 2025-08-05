from django.contrib import admin
from .models import Employer
# Register your models here.


class EmployerAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'date_naissance', 'matricule', 'Inam')
    search_fields = ('nom', 'prenom', 'matricule')
admin.site.register(Employer, EmployerAdmin)