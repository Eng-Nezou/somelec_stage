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

class Employer(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    matricule = models.CharField(max_length=100)
    inam = models.CharField(max_length=16)
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
class Ordonnance(models.Model):
    date = models.DateField()
    heure = models.TimeField()
    employe = models.ForeignKey(Employer, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='ordonnances')
    
    def __str__(self):
        return f"Ordonnance de {self.employe} par {self.medecin} le {self.date} à {self.heure}"

class Medicament(models.Model):
    nom = models.CharField(max_length=100)
    ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE, related_name='medicaments')
    quantite = models.IntegerField()
    
    def __str__(self):
        return f"{self.nom} - {self.quantite} "