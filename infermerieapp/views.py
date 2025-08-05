import pandas as pd
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login
from .models import Employer
from django.db.models import Q
# Create your views here.

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
    


# @login_required(login_url='login') 
def gestionnaire(request):
    return render(request, 'dashbord.html')

def filter_employers(request):
    employers = []

    if request.method == 'POST':
        matricule_inam = request.POST.get('matricule')
        employers = Employer.objects.filter(Q(matricule=matricule_inam) | Q(inam=matricule_inam))
        

    return render(request, 'filter.html', {'employers': employers})
