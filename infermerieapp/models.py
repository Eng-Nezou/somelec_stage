from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Utilisateur(AbstractUser):
    ROLE_CHOICES = (
        ('medecin', 'Médecin'),
        ('gestionnaire', 'Gestionnaire'),
        ('technicien', 'Technicien'),
        ('chef service', 'Chef service'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='gestionnaire')
    
    def __str__(self):
        return self.username
class Reference(models.Model):
    quantite_medicament = models.IntegerField()
    nom_chef = models.CharField(max_length=200) 
    nom_medecin = models.CharField(max_length=200)
    nom_technicien = models.CharField(max_length=200)
    

class Employer(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    matricule = models.CharField(max_length=100)
    inam = models.CharField(max_length=16)
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
class Ordonnance(models.Model):
    date = models.DateField(auto_now_add=True)
    employe = models.ForeignKey(Employer, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, default='en attente' , choices=[
        ('en attente', 'En attente'),
        ('validée', 'Validée'),
        ('annulée', 'Annulée'),
        ('terminée', 'Terminée'),
    ])
    validate_chef = models.BooleanField(default=False)
    validate_medecin = models.BooleanField(default=False)
    
    nom_chef = models.CharField(max_length=200,null=True)
    nom_medecin = models.CharField(max_length=200,null=True)
    nom_technicien = models.CharField(max_length=200,null=True)
    def __str__(self):
        return f"Ordonnance de {self.employe} par"
    
    
    
    


class Medicament(models.Model):
    nom = models.CharField(max_length=100)
    ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE, related_name='medicaments')
    quantite = models.IntegerField()
    utilisation = models.IntegerField(null=True)
    
    def __str__(self):
        return f"{self.nom} - {self.quantite} "
    
    