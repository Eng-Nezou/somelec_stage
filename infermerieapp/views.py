import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from .models import Employer,Ordonnance,Medicament
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
    


def gestionnaire(request):
    return render(request, 'dashbord.html')

def filter_employers(request):
    employers = []

    if request.method == 'POST':
        matricule_inam = request.POST.get('matricule')
        employers = Employer.objects.filter(Q(matricule=matricule_inam) | Q(inam=matricule_inam))
        

    return render(request, 'filter.html', {'employers': employers})


def ordonnance_view(request):
    if request.method == 'POST':
        inam = request.POST.get('inam_assurer')
        employer = Employer.objects.get(inam=inam)

        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        if employer:

            return render(request, 'ordonnance.html', {'employer': employer,'date': today_date})
        else:
            return render(request, 'ordonnance.html', {'error': 'Employer not found'})


    return render(request, 'ordonnance.html')



@csrf_exempt
def ordonnance_generate(request):
    if request.method == 'POST':
        medicaments_json = request.POST.get('medicaments')
        inam_assurer = request.POST.get('inam_assurer')
        employer = Employer.objects.get(inam=inam_assurer)
        ordonnance = Ordonnance(employe=employer)
        ordonnance.save()
        
        medicaments = json.loads(medicaments_json) if medicaments_json else []
        for medicament in medicaments:
            name = medicament.get('name')
            quantity = medicament.get('quantity')
            if name and quantity:
                med = Medicament(nom=name, quantite=quantity, ordonnance=ordonnance)
                med.save()
        medicaments = Medicament.objects.filter(ordonnance=ordonnance)
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")
        return render(request, 'ordonnance_generate.html', {'employer': employer, 'medicaments': medicaments,'date': today_date, 'ordonnance': ordonnance})
        
    return render(request, 'ordonnance_generate.html',{'ordonnance': None, 'employer': None, 'medicaments': [], 'date': datetime.datetime.now().strftime("%Y-%m-%d")})



def liste_ordonnances(request):
    ordonnances=[]
    medicaments = []
    if request.method == 'POST':
        ordonnances = Ordonnance.objects.all().order_by('-date')
        medicaments = Medicament.objects.none()  # Initialisation vide
    
        matricule_inam = request.POST.get('matricule_inam')
        employers = Employer.objects.filter(Q(inam=matricule_inam) | Q(matricule=matricule_inam))

        # Filtrer les ordonnances par employé
        ordonnances = Ordonnance.objects.filter(employe__in=employers).order_by('-date')

        # Récupérer les médicaments liés aux ordonnances filtrées
        medicaments = Medicament.objects.filter(ordonnance__in=ordonnances)

    return render(request, 'liste_ordonnances.html', {
        'ordonnances': ordonnances,
        'medicaments': medicaments
    })
def ordonnance_modifier(request, pk):
    ordonnance = Ordonnance.objects.get(pk=pk)
    ordonnance.statut = 'terminée'
    ordonnance.save()
    return redirect('liste_ordonnances')

def voire_ordonnance(request, pk):
    employer = Ordonnance.objects.get(pk=pk).employe
    ordonnance = Ordonnance.objects.get(pk=pk)
    medicaments = Medicament.objects.filter(ordonnance=ordonnance)
    today_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return render(request, 'ordonnance_generate.html', {'employer': employer, 'medicaments': medicaments,'date': today_date, 'ordonnance': ordonnance})
        
def chef(request):
    ordonnances = Ordonnance.objects.filter(statut='en attente').order_by('-date')
    medicaments = Medicament.objects.none()
    
    if request.method == 'POST':
        ordonnance_id=request.POST.get('ordonnance_id')
        statut=request.POST.get('statut')
        ordonnance=Ordonnance.objects.get(id=ordonnance_id)
        ordonnance.statut=statut
        ordonnance.save()
        ordonnances = Ordonnance.objects.filter(statut='en attente').order_by('-date')
        medicaments = Medicament.objects.none()  # Initialisation vide
        return render(request, 'chef.html', {
        'ordonnances': ordonnances,
        'medicaments': medicaments
        })
    return render(request, 'chef.html', {
        'ordonnances': ordonnances,
        'medicaments': medicaments
    })
    