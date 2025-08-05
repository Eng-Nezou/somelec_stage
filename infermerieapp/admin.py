from django.contrib import admin
from .models import Employer
# Register your models here.


class EmployerAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'date_naissance', 'matricule', 'inam')
    search_fields = ('nom', 'prenom', 'matricule','inam')
admin.site.register(Employer, EmployerAdmin)