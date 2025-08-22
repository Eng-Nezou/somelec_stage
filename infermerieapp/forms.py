from django import forms

from infermerieapp.models import *


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
        
        }
class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
        }       

class AnalyseForm(forms.ModelForm):
    class Meta:
        model = Analyse
        fields = ['nom', 'service', 'detail', 'drg', 'montant']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'}),
            'drg': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }
        
class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['nom', 'service', 'detail', 'drg', 'montant']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'}),
            'drg': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }       
class HospitalisationForm(forms.ModelForm):     
    class Meta:
        model = Hospitalisation
        fields = ['nom', 'service', 'detail', 'drg', 'montant']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'}),
            'drg': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }       
        
class ScannerForm(forms.ModelForm):
    class Meta:
        model = Scanner
        fields = ['nom', 'service', 'detail', 'drg', 'montant']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'}),
            'drg': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }   
        
class IrmForm(forms.ModelForm):         
    class Meta:
        model = Irm
        fields = ['nom', 'service', 'detail', 'drg', 'montant']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'}),
            'drg': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }
        
class EchographieForm(forms.ModelForm):
    class Meta:
        model = Echographie
        fields = ['nom', 'service', 'detail', 'drg', 'montant']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'}),
            'drg': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }
        
        
class RadiograpthieForm(forms.ModelForm):
    class Meta:
        model = Radiographie
        fields = ['nom', 'service', 'detail', 'drg', 'montant']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'}),
            'drg': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }
        
class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'service', 'detail', 'drg', 'montant']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'service': forms.TextInput(attrs={'class': 'form-control'}),
            'detail': forms.Textarea(attrs={'class': 'form-control'}),
            'drg': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }
        
        
                         