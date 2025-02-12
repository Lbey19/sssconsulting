from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib import messages
from .forms import ContactForm  # Assurez-vous d'importer le formulaire

# Vue pour la page d'accueil
def home(request):
    return render(request, 'pages/home.html')  # Assurez-vous que le fichier est bien dans templates/pages/

# Vue pour la page services
def services(request):
    return render(request, 'pages/services.html')  # Assurez-vous du bon chemin !

# Vue pour tester l'envoi d'email
def test_email(request):
    subject = "Test d'envoi d'email"
    message = "Ceci est un test d'email envoyé depuis Django."
    from_email = "mohamed.benadrouche@gmail.com"  # Ton email
    recipient_list = ["y.benadrouche@ecoles-epsi.net"]  # L'email de destination

    try:
        send_mail(subject, message, from_email, recipient_list)
        return HttpResponse("Email envoyé avec succès !")
    except Exception as e:
        return HttpResponse(f"Erreur lors de l'envoi de l'email : {e}")

# Vue pour la page de contact avec formulaire
def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Envoyer l'email avec les données du formulaire
            try:
                send_mail(
                    subject=f"Contact : {subject}",
                    message=f"Nom: {name}\nEmail: {email}\n\nMessage:\n{message}",
                    from_email=email,  # L'expéditeur est l'email renseigné
                    recipient_list=['mohamed.benadrouche@gmail.com'],  # Ton email de réception
                    fail_silently=False
                )
                messages.success(request, "Votre message a bien été envoyé.")
                return redirect("contact")  # Redirection après envoi
            except Exception as e:
                messages.error(request, f"Erreur lors de l'envoi de l'email : {e}")
    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})
