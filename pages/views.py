from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')  # Assurez-vous que le fichier est bien dans templates/pages/

def services(request):
    return render(request, 'pages/services.html')  # Assurez-vous du bon chemin !



# Create your views here.
