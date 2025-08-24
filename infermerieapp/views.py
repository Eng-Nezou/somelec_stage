import json
import pandas as pd
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from .models import Analyse, Consultation, Employer, Examen, Institution,Ordonnance,Medicament, Reference
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Q
import datetime
def index(request):
    # df = pd.read_excel('acte.xlsx')
    
    # for _, row in df.iterrows():
    #     val = row['montant']   # valeur venant du DataFrame
    #     val = str(val).replace('\xa0', '').replace(' ', '')  # on enlève les espaces spéciaux
    #     val = int(val)  # conversion en entier
    #     row['montant'] = val  # on met à jour la valeur dans le DataFrame
    #     if row['ACTE']== 'HOSPITALISATION ':
    #         Hospitalisation.objects.create(
    #             nom=row['ACTE'],
    #             service=row['SERVICE'],
    #             detail=row['detail'],
    #             drg=row['DRG'],
    #             montant=row['montant'],
                
    #         )
            
    

    return render(request, 'index.html')
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
        gfu = request.POST.get('gfu')
        whatsap = request.POST.get('whatsap')
        medicaments_json = request.POST.get('medicaments')
        inam_assurer = request.POST.get('inam_assurer')
        employer = Employer.objects.get(inam=inam_assurer)
        prescription = request.POST.get('prescription')
        diagnostic = request.POST.get('diagnostic')
        
        ordonnance = Ordonnance(employe=employer, gfu=gfu, whatsap=whatsap,prescription=prescription, diagnostic=diagnostic)
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
        debut = request.POST.get('debut')
        fin = request.POST.get('fin')
        if matricule_inam:
            employers = Employer.objects.filter(
                Q(inam=matricule_inam) | Q(matricule=matricule_inam)
            )
            ordonnances = ordonnances.filter(employe__in=employers)

        if debut and fin:
            debut = request.POST['debut']
            fin = request.POST['fin']
            ordonnances = ordonnances.filter(date__range=[debut, fin])
            

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
    total_quantite = 0
    reference = Reference.objects.last()
    employer = Ordonnance.objects.get(pk=pk).employe
    ordonnance = Ordonnance.objects.get(pk=pk)
    medicaments = Medicament.objects.filter(ordonnance=ordonnance)
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    for medicament in medicaments:
        total_quantite += medicament.quantite
    return render(request, 'ordonnance_generate.html', {'employer': employer, 'medicaments': medicaments,'date': today_date, 'ordonnance': ordonnance, 'reference':reference, 'total_quantite': total_quantite})
        
        
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


def institution_view(request):
    institutions = Institution.objects.all()
    return render(request, 'institution.html', {'institutions': institutions})
def institution_ajouter(request):
    if request.method == 'POST':
        form = InstitutionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/liste_bon/')
    else:
        form = InstitutionForm()
    return render(request, 'institution_ajouter.html', {'form': form})
def institution_supprimer(request, pk):
    institution = Institution.objects.get(pk=pk)
    
    institution.delete()
    return redirect('/liste_bon/')
def consultation_view(request):
    consultations = Consultation.objects.all()
    return render(request, 'consultation.html', {'consultations': consultations})
def consultation_ajouter(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/liste_bon/')
    else:
        form = ConsultationForm()
    return render(request, 'consultation_ajouter.html', {'form': form})
def consultation_supprimer(request, pk):
    consultation = Consultation.objects.get(pk=pk)
    
    consultation.delete()
    return redirect('/liste_bon/')
    
def analyse_view(request):
    analyses = Analyse.objects.all()
    return render(request, 'analyse.html', {'analyses': analyses})
def analyse_ajouter(request):
    if request.method == 'POST':
        form = AnalyseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/liste_bon/')
    else:
        form = AnalyseForm()
    return render(request, 'analyse_ajouter.html', {'form': form})
def analyse_supprimer(request, pk):
    analyse = Analyse.objects.get(pk=pk)
    
    analyse.delete()
    return redirect('/liste_bon/')    
def examen_view(request):
    examens = Examen.objects.all()
    return render(request, 'examen.html', {'examens': examens})
def examen_ajouter(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/liste_bon/')
    else:
        form = ExamenForm()
    return render(request, 'examen_ajouter.html', {'form': form})
def examen_supprimer(request, pk):
    examen = Examen.objects.get(pk=pk)
    
    examen.delete()
    return redirect('/liste_bon/')
def hospitalisation_view(request):
    hospitalisations = Hospitalisation.objects.all()
    return render(request, 'hospitalisation.html', {'hospitalisations': hospitalisations})
def hospitalisation_ajouter(request):
    if request.method == 'POST':
        form = HospitalisationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/liste_bon/')
    else:
        form = HospitalisationForm()
    return render(request, 'hospitalisation_ajouter.html', {'form': form})
def hospitalisation_supprimer(request, pk):
    hospitalisation = Hospitalisation.objects.get(pk=pk)
    
    hospitalisation.delete()
    return redirect('/liste_bon/')
def irm_view(request):
    irms = Scanner.objects.all()
    return render(request, 'irm.html', {'irms': irms})
def irm_ajouter(request):
    if request.method == 'POST':
        form = ScannerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/liste_bon/')
    else:
        form = ScannerForm()
    return render(request, 'irm_ajouter.html', {'form': form})
def irm_supprimer(request, pk):
    irm = Scanner.objects.get(pk=pk)
    
    irm.delete()
    return redirect('/liste_bon/')
def echographie_view(request):
    echographies = Examen.objects.filter(nom__icontains='echographie')
    return render(request, 'echographie.html', {'echographies': echographies})  
def echographie_ajouter(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/liste_bon/')
    else:
        form = ExamenForm()
    return render(request, 'echographie_ajouter.html', {'form': form})
def echographie_supprimer(request, pk):
    echographie = Examen.objects.get(pk=pk)
    
    echographie.delete()
    return redirect('/liste_bon/')  
def radiographie_view(request):
    radiographies = Examen.objects.filter(nom__icontains='radiographie')
    return render(request, 'radiographie.html', {'radiographies': radiographies})   
def radiographie_ajouter(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/liste_bon/')
    else:
        form = ExamenForm()
    return render(request, 'radiographie_ajouter.html', {'form': form})
def radiographie_supprimer(request, pk):
    radiographie = Examen.objects.get(pk=pk)
    
    radiographie.delete()
    return redirect('/liste_bon/') 
def produit_view(request):
    produits = Produit.objects.all()
    return render(request, 'produit.html', {'produits': produits})      
def produit_ajouter(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/liste_bon/')
    else:
        form = ProduitForm()
    return render(request, 'produit_ajouter.html', {'form': form})  
def produit_supprimer(request, pk):
    produit = Produit.objects.get(pk=pk)
    produit.delete()
    return redirect('/liste_bon/')

def scanner_view(request):
    scanners = Scanner.objects.all()
    return render(request, 'scanner.html', {'scanners': scanners})  
def scanner_ajouter(request):
    if request.method == 'POST':
        form = ScannerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/liste_bon/')
    else:
        form = ScannerForm()
    return render(request, 'scanner_ajouter.html', {'form': form})
def scanner_supprimer(request, pk):
    scanner = Scanner.objects.get(pk=pk)
    scanner.delete()
    return redirect('/liste_bon/')

def ajouter(request):

    return render(request, 'ajouter.html')        

def liste_bon(request):
    institutions = Institution.objects.all()
    consultations = Consultation.objects.all()
    analyses = Analyse.objects.all()
    examens = Examen.objects.all()
    irm = Irm.objects.all()
    echographies = Echographie.objects.all()
    radiographies = Radiographie.objects.all()
    hospitalisations = Hospitalisation.objects.all()
    produits = Produit.objects.all()
    scanners = Scanner.objects.all()
    
    return render(request, 'liste_bon.html', {
        'institutions': institutions,   
        'consultations': consultations,
        'analyses': analyses,
        'examens': examens,
        'irm': irm,
        'echographies': echographies,
        'radiographies': radiographies,
        'hospitalisations': hospitalisations,
        'produits': produits,
        'scanners': scanners
    })
    
def ajouter_pris(request):
    reference = Reference.objects.last()
    if request.method == 'POST':
        employer_inam = request.POST.get('assurer_inam')
        employer = Employer.objects.get(inam=employer_inam)
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        institutions= Institution.objects.all()
        search= request.POST.get('search')
        if search:
            if search.lower() == 'consultation':
                consultations = Consultation.objects.all()
                return render(request, 'charge.html', {'data': consultations,'type':'consultation','reference':reference,'employer':employer, 'date':today_date, 'institutions': institutions})
            elif search.lower() == 'analyse':
                analyses= Analyse.objects.all()
                return render(request, 'charge.html', {'data': analyses,'type':'analyse','reference':reference,'employer':employer, 'date':today_date, 'institutions': institutions})
            elif search.lower() == 'examen':    
                examens= Examen.objects.all()
                return render(request, 'charge.html', {'data': examens,'type':'examen','reference':reference,'employer':employer, 'date':today_date, 'institutions': institutions})
            elif search.lower() == 'hospitalisation':
                hospitalisations= Hospitalisation.objects.all()
                return render(request, 'charge.html', {'data': hospitalisations,'type':'hospitalisation','reference':reference,'employer':employer, 'date':today_date, 'institutions': institutions})
            elif search.lower() == 'irm':
                irms= Irm.objects.all()
                return render(request, 'charge.html', {'data': irms,'type':'irm','reference':reference,'employer':employer, 'date':today_date, 'institutions': institutions})
            elif search.lower() == 'echographie':
                echographies= Echographie.objects.all()
                return render(request, 'charge.html', {'data': echographies,'type':'echographie','reference':reference,'employer':employer, 'date':today_date, 'institutions': institutions})
            elif search.lower() == 'radiographie':
                radiographies= Radiographie.objects.all()
                return render(request, 'charge.html', {'data': radiographies,'type':'radiographie','reference':reference,'employer':employer, 'date':today_date, 'institutions': institutions})
            elif search.lower() == 'produit':
                produits= Produit.objects.all()
                return render(request, 'charge.html', {'data': produits,'type':'produit','reference':reference,'employer':employer, 'date':today_date, 'institutions': institutions})
            elif search.lower() == 'scanner':
                scanners= Scanner.objects.all()
                return render(request, 'charge.html', {'data': scanners,'type':'scanner','reference':reference,'employer':employer, 'date':today_date, 'institutions': institutions})
            
        return render(request, 'charge.html', {'data': [],'type':'', 'reference':reference,'employer':employer, 'date':today_date, 'institutions': institutions})        
    return render(request, 'charge.html') 

def generate_pris(request):
    reference = Reference.objects.last()

    if request.method == 'POST':
        inam = request.POST.get('assurer_inam')
        institution_id = request.POST.get('institution_id')
        institution = Institution.objects.get(id=institution_id)
        employer = Employer.objects.get(inam=inam)
        gfu = request.POST.get('gfu')
        whatsap = request.POST.get('whatsap')
        pris_en_charge = PrisEnCharge(employe=employer, institution=institution, gfu=gfu, whatsap=whatsap)
        pris_en_charge.save()
        
        # Récupérer les IDs des actes sélectionnés
        data_ids = request.POST.getlist('data')
        acte_type = request.POST.get('type')
        
        if acte_type == 'consultation':
            actes = Consultation.objects.filter(id__in=data_ids)
            pris_en_charge.consultations.set(actes)
        elif acte_type == 'analyse':
            actes = Analyse.objects.filter(id__in=data_ids)
            pris_en_charge.analyses.set(actes)
        elif acte_type == 'examen':
            actes = Examen.objects.filter(id__in=data_ids)
            pris_en_charge.examens.set(actes)
        elif acte_type == 'hospitalisation':
            actes = Hospitalisation.objects.filter(id__in=data_ids)
            pris_en_charge.hospitalisations.set(actes)
        elif acte_type == 'irm':
            actes = Irm.objects.filter(id__in=data_ids)
            pris_en_charge.irms.set(actes)
        elif acte_type == 'echographie':
            actes = Echographie.objects.filter(id__in=data_ids)
            pris_en_charge.echographies.set(actes)
        elif acte_type == 'radiographie':
            actes = Radiographie.objects.filter(id__in=data_ids)
            pris_en_charge.radiographies.set(actes)
        elif acte_type == 'produit':
            actes = Produit.objects.filter(id__in=data_ids)
            pris_en_charge.produits.set(actes)
        elif acte_type == 'scanner':
            actes = Scanner.objects.filter(id__in=data_ids)
            pris_en_charge.scanners.set(actes)
        pris_en_charge.save()
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        return render(request, 'generate_pris.html', {'pris_en_charge': pris_en_charge, 'employer': employer, 'institution': institution, 'date': today_date; 'reference':reference})
    
        
        # Ajouter les actes sélectionnés au PrisEnCharge
        