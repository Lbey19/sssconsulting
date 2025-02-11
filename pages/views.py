from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')  # Assurez-vous que le fichier est bien dans templates/pages/

def services(request):
    return render(request, 'pages/services.html')  # Assurez-vous du bon chemin !

from django.core.mail import send_mail
from django.http import HttpResponse

def test_email(request):
    subject = "Test d'envoi d'email"
    message = "Ceci est un test d'email envoyé depuis Django."
    from_email = "mohamed.benadrouche@gmail.com"  # Mon email
    recipient_list = ["y.benadrouche@ecoles-epsi.net"]  # l'email qui recevra le test

    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse("Email envoyé avec succès !")
    except Exception as e:
        return HttpResponse(f"Erreur lors de l'envoi de l'email : {e}")


# Create your views here.
