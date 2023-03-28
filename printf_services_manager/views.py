from django.shortcuts import render

def accueil(request):
    return render(request, 'accueil.html')

def services(request):
    return render(request, 'services.html')