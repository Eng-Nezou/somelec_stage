import json
import pandas as pd
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from .models import Analyse, Consultation, Employer, Examen, Institution,Ordonnance,Medicament, Reference
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime

def auth_login(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user= authenticate(request, username=email, password=password) 
        if user is not None:
            login(request, user)
            return redirect('/dashbord/')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')
    
def auth_logout(request):
    logout(request)
    return redirect('/login/')

def gestionnaire(request):
    return render(request, 'dashbord.html')

def filter_employers(request):
    employers = []
    
    # df = pd.read_excel('employers.xlsx')
    # for _, row in df.iterrows():
    #     Employer.objects.create(
    #         nom=row['NOM'],
    #         ur=row['UR'],
    #         date_naissance=row['DATE NAISS'],
    #         matricule=row['MATRICULE'],
    #         inam=row['INAM']
    #     )


    if request.method == 'POST':
        matricule_inam = request.POST.get('matricule')
        employers = Employer.objects.filter(Q(matricule=matricule_inam) | Q(inam=matricule_inam))
        

    return render(request, 'filter.html', {'employers': employers})


def pris_en_charge(request):
    employers = []
    if request.method == 'POST':
        matricule_inam = request.POST.get('matricule')
        employers = Employer.objects.filter(Q(matricule=matricule_inam) | Q(inam=matricule_inam))
        
    return render(request, 'pris_charge.html', {'employers': employers})


def ordonnance_view(request):
    reference = Reference.objects.last()
    if request.method == 'POST':
        inam = request.POST.get('inam_assurer')
        employer = Employer.objects.get(inam=inam)

        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        if employer:

            return render(request, 'ordonnance.html', {'employer': employer,'date': today_date ,'reference':reference})
        else:
            return render(request, 'ordonnance.html', {'error': 'Employer not found' ,'reference':reference})


    return render(request, 'ordonnance.html',{'reference':reference})



@csrf_exempt
def ordonnance_generate(request):
    reference = Reference.objects.last()
    if request.method == 'POST':
        total_quantite = 0
        gfu_whatsap = request.POST.get('gfu_whatsap')
        medicaments_json = request.POST.get('medicaments')
        inam_assurer = request.POST.get('inam_assurer')
        employer = Employer.objects.get(inam=inam_assurer)
        prescription = request.POST.get('prescription')
        diagnostic = request.POST.get('diagnostic')
        
        ordonnance = Ordonnance(employe=employer, gfu_whatsap=gfu_whatsap,prescription=prescription, diagnostic=diagnostic)
        ordonnance.save()
        
        medicaments = json.loads(medicaments_json) if medicaments_json else []
        for medicament in medicaments:
            total_quantite+= int(medicament.get('quantity', 0))
            name = medicament.get('name')
            quantity = medicament.get('quantity')
            utilisation = medicament.get('utilisation')
            dosage = medicament.get('dosage')
            duree = medicament.get('duree')
            type_duree = medicament.get('type_duree')
            if name and quantity:
                med = Medicament(nom=name, quantite=quantity, ordonnance=ordonnance,utilisation=utilisation , dosage=dosage, duree=duree, type_duree=type_duree)
                med.save()
        medicaments = Medicament.objects.filter(ordonnance=ordonnance)
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        return render(request, 'ordonnance_generate.html', {'employer': employer, 'medicaments': medicaments,'date': today_date, 'ordonnance': ordonnance , 'reference': reference ,'total_quantite': total_quantite})
        
    return render(request, 'ordonnance_generate.html',{'ordonnance': None, 'employer': None, 'medicaments': [], 'date': datetime.datetime.now().strftime("%Y-%m-%d"),'reference': reference ,'total_quantite': 0})





from django.db.models import Q

def liste_ordonnances(request):
    ordonnances = Ordonnance.objects.all().order_by('-date')  # start with all
    medicaments = Medicament.objects.none()
    
    if request.method == 'POST':
        matricule_inam = request.POST.get('matricule_inam')
        filter_date = request.POST.get('filter_date')
        if matricule_inam:
            employers = Employer.objects.filter(
                Q(inam=matricule_inam) | Q(matricule=matricule_inam)
            )
            ordonnances = ordonnances.filter(employe__in=employers)

        if filter_date:
            ordonnances = ordonnances.filter(date=filter_date)

        medicaments = Medicament.objects.filter(ordonnance__in=ordonnances)
        
        return render(request, 'liste_ordonnances.html', {
        'ordonnances': ordonnances,
        'medicaments': medicaments
        })
    return render(request, 'liste_ordonnances.html', {
        'ordonnances': Ordonnance.objects.none(),
        'medicaments': medicaments
    })


def ordonnance_modifier(request, pk):
    ordonnance = Ordonnance.objects.get(pk=pk)
    ordonnance.statut = 'terminée'
    ordonnance.save()
    return redirect('liste_ordonnances')

def voire_ordonnance(request, pk):
    
    reference = Reference.objects.last()
    employer = Ordonnance.objects.get(pk=pk).employe
    ordonnance = Ordonnance.objects.get(pk=pk)
    medicaments = Medicament.objects.filter(ordonnance=ordonnance)
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return render(request, 'ordonnance_generate.html', {'employer': employer, 'medicaments': medicaments,'date': today_date, 'ordonnance': ordonnance, 'reference':reference})
        
        
def medecin(request):
    
    reference = Reference.objects.last()
    if request.user.role!='medecin':
        return redirect('/dashbord/')
    ordonnances = Ordonnance.objects.filter(statut='en attente').order_by('-date')
    ordonnances = ordonnances.filter(validate_medecin=False)
    medicaments = Medicament.objects.none()
    
    if request.method == 'POST':
        ordonnance_id=request.POST.get('ordonnance_id')
        statut=request.POST.get('statut')
        ordonnance=Ordonnance.objects.get(id=ordonnance_id)
        if statut == 'validée':
            ordonnance.validate_medecin = True
        else:
            ordonnance.validate_medecin = False
        
        
        

        ordonnance.nom_medecin=reference.nom_medecin

        
        ordonnance.save()
        
        ordonnances = Ordonnance.objects.filter(statut='en attente').order_by('-date')
        medicaments = Medicament.objects.none()
        ordonnances = ordonnances.filter(validate_medecin=False)
        
        
        return render(request, 'medecin.html', {
        'ordonnances': ordonnances,
        'medicaments': medicaments
        })

    return render(request,'medecin.html',{
        'ordonnances': ordonnances,
        'medicaments': medicaments
    })
def chef(request):
    reference = Reference.objects.last()
    if request.user.role != 'chef service':
        return redirect('/dashbord/')
    ordonnances = Ordonnance.objects.filter(statut='en attente').order_by('-date')
    medicaments = Medicament.objects.none()
    
    if request.method == 'POST':
        ordonnance_id=request.POST.get('ordonnance_id')
        statut=request.POST.get('statut')
        ordonnance=Ordonnance.objects.get(id=ordonnance_id)
        ordonnance.statut=statut

        ordonnance.nom_chef=reference.nom_chef
        if statut == 'validée':
            ordonnance.validate_chef = True
        
        ordonnance.save()
        ordonnances = Ordonnance.objects.filter(statut='en attente').order_by('-date')
        medicaments = Medicament.objects.none()
        return render(request, 'chef.html', {
        'ordonnances': ordonnances,
        'medicaments': medicaments
        })
    return render(request, 'chef.html', {
        'ordonnances': ordonnances,
        'medicaments': medicaments
    })

def tableau_referencer(request):
    reference = Reference.objects.last()
    if request.method=='POST':
        nom_chef=request.POST.get('nom_chef')
        nom_medecin=request.POST.get('nom_medecin')
        nom_technicien=request.POST.get('nom_technicien')
        quantite_medicament=request.POST.get('quantite_medicament')
        
        reference.nom_chef = nom_chef
        reference.nom_medecin = nom_medecin
        reference.nom_technicien = nom_technicien
        reference.quantite_medicament = quantite_medicament
        
        reference.save()
    return render(request,'tableau_References.html',{'reference':reference})
    
def referencer_pris_en_charge(request):
    
    if request.method == 'POST':
        consultation= request.POST.get('consultation')
        institution = request.POST.get('institution')
        analyse = request.POST.get('analyse')
        examen = request.POST.get('examen')
        if consultation:
            Consultation.objects.create(nom=consultation)
        if institution:
            Institution.objects.create(nom=institution)
        if analyse :
            Analyse.objects.create(nom=analyse)
        if examen:
            Examen.objects.create(nom=examen)
    
        
    return render(request, 'referencer_pris_en_charge.html')   

def supprimer(request):
    if request.method == 'POST':
        consultation = request.POST.get('consultation')
        institution = request.POST.get('institution')
        analyse = request.POST.get('analyse')
        examen = request.POST.get('examen')
        if consultation:
            Consultation.objects.filter(nom=consultation).delete()
        if institution:
            Institution.objects.filter(nom=institution).delete()
        if analyse:
            Analyse.objects.filter(nom=analyse).delete()
        if examen:
            Examen.objects.filter(nom=examen).delete()
    return render(request, 'supprimer.html')         