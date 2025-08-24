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
    
class Institution(models.Model):
    nom = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.nom

class Consultation(models.Model):
    nom= models.CharField(max_length=100) 
    
    def __str__(self):
        return self.nom
    
class Analyse(models.Model):
    nom = models.CharField(max_length=100)
    service = models.CharField(max_length=100, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    drg= models.CharField(max_length=100, null=True, blank=True)
    montant = models.IntegerField(null=True, blank=True)
    tarif_chn = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nom     
    
class Examen(models.Model):
    nom = models.CharField(max_length=100)
    service = models.CharField(max_length=100, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    drg= models.CharField(max_length=100, null=True, blank=True)
    montant = models.IntegerField(null=True, blank=True)
    tarif_chn = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nom     
    
class Hospitalisation(models.Model):
    nom = models.CharField(max_length=100)
    service = models.CharField(max_length=100, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    drg= models.CharField(max_length=100, null=True, blank=True)
    montant = models.IntegerField(null=True, blank=True)
    tarif_chn = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nom
    
class Scanner(models.Model):
    nom = models.CharField(max_length=100)
    service = models.CharField(max_length=100, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    drg= models.CharField(max_length=100, null=True, blank=True)
    montant = models.IntegerField(null=True, blank=True)
    tarif_chn = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nom
    
class Irm(models.Model):
    nom = models.CharField(max_length=100)
    service = models.CharField(max_length=100, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    drg= models.CharField(max_length=100, null=True, blank=True)
    montant = models.IntegerField(null=True, blank=True)
    tarif_chn = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nom
    
class Echographie(models.Model):
    nom = models.CharField(max_length=100)
    service = models.CharField(max_length=100, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    drg= models.CharField(max_length=100, null=True, blank=True)
    montant = models.IntegerField(null=True, blank=True)
    tarif_chn = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nom
    
class Produit(models.Model):
    nom = models.CharField(max_length=100)
    service = models.CharField(max_length=100, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    drg= models.CharField(max_length=100, null=True, blank=True)
    montant = models.IntegerField(null=True, blank=True)
    tarif_chn = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nom
    
    
class Radiographie(models.Model):
    nom = models.CharField(max_length=100)
    service = models.CharField(max_length=100, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    drg= models.CharField(max_length=100, null=True, blank=True)
    montant = models.IntegerField(null=True, blank=True)
    tarif_chn = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.nom
    

class Employer(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    matricule = models.CharField(max_length=100)
    inam = models.CharField(max_length=16)
    ur = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
class Ordonnance(models.Model):
    date = models.DateField(auto_now_add=True)
    employe = models.ForeignKey(Employer, on_delete=models.CASCADE)
    gfu = models.CharField(max_length=20, null=True, blank=True)
    whatsap = models.CharField(max_length=20, null=True, blank=True)
    prescription = models.CharField(max_length=20, null=True, blank=True, choices=[
        ('Normale', 'Normale'), 
        ('Urgent', 'Urgent'),
        ('Chronique', 'Chronique'),
    ])
    diagnostic = models.CharField(max_length=200, null=True, blank=True)
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

class PrisEnCharge(models.Model):
    employe = models.ForeignKey(Employer, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    consultations = models.ManyToManyField(Consultation, blank=True, related_name='consultations')
    analyses = models.ManyToManyField(Analyse, blank=True, related_name='analyses')
    examens = models.ManyToManyField(Examen, blank=True, related_name='examens')
    hospitalisations = models.ManyToManyField(Hospitalisation, blank=True, related_name='hospitalisations')
    scanners = models.ManyToManyField(Scanner, blank=True, related_name='scanners')
    irms = models.ManyToManyField(Irm, blank=True, related_name='irms')
    echographies = models.ManyToManyField(Echographie, blank=True, related_name='echographies')
    radiographies = models.ManyToManyField(Radiographie, blank=True, related_name='radiographies')
    produits = models.ManyToManyField(Produit, blank=True, related_name='produits')
    date = models.DateField(auto_now_add=True)
    gfu = models.CharField(max_length=20, null=True, blank=True)
    whatsap = models.CharField(max_length=20, null=True, blank=True)
    statut = models.CharField(max_length=20, default='en attente' , choices=[
        ('en attente', 'En attente'),   
        ('validée', 'Validée'),
        ('annulée', 'Annulée'),
        ('terminée', 'Terminée'),
    ])
    validate_chef = models.BooleanField(default=False)
    validate_medecin = models.BooleanField(default=False)
    validate_technicien = models.BooleanField(default=False)
    
    nom_chef = models.CharField(max_length=200,null=True)
    nom_medecin = models.CharField(max_length=200,null=True)
    nom_technicien = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return f"Pris en charge de {self.employe} par {self.institution} pour {self.consultation}"    
    
    


class Medicament(models.Model):
    nom = models.CharField(max_length=100)
    ordonnance = models.ForeignKey(Ordonnance, on_delete=models.CASCADE, related_name='medicaments')
    quantite = models.IntegerField()
    utilisation = models.IntegerField(null=True)
    dosage = models.CharField(max_length=50, null=True, blank=True, choices=[
        ('cp', 'CP'),
        ('sirop', 'SIROP'),
        ('gel', 'GEL'),
        ('sachet', 'SACHET'),
        ('creme', 'CREME'),
        ('injectable', 'INJECTABLE'),
    ])
    duree = models.IntegerField(null=True, blank=True)
    type_duree = models.CharField(max_length=20, null=True, blank=True, choices=[
        ('jour', 'Jour'),
        ('semaine', 'Semaine'),
        ('mois', 'Mois'),
    ])
    def __str__(self):
        return f"{self.nom} - {self.quantite} "
    
    