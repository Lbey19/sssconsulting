from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
from .forms import ContactForm
import logging

# Importation du formulaire d'inscription et des modules nécessaires
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Count

from .models import Article, Commentaire, Notation
from .forms import ArticleForm, CommentaireForm, NotationForm


# Configuration du logger pour capturer les erreurs
logger = logging.getLogger(__name__)

# Vue pour la page d'accueil
def home(request):
    return render(request, 'pages/home.html')

# Vue pour la page services
def services(request):
    return render(request, 'pages/services.html')

# Vue pour la page de contact et l'envoi d'email
def contact(request):
    if request.method == "POST":
        print("✅ Données reçues:", request.POST)  # DEBUG : Affiche les données reçues

        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            full_message = f"Nom: {name}\nEmail: {email}\n\nMessage:\n{message}"

            try:
                send_mail(
                    subject=f"[Contact SSS Consulting] {subject}",
                    message=full_message,
                    from_email="mohamed.benadrouche@gmail.com",
                    recipient_list=["mohamed.benadrouche@gmail.com"],  # Réception
                    fail_silently=False,
                )
                messages.success(request, "Votre message a bien été envoyé.")
                return redirect("contact")
            except Exception as e:
                print(f"❌ Erreur d'envoi : {e}")  # DEBUG : Affiche l'erreur
                messages.error(request, f"Erreur d'envoi : {e}")

    else:
        form = ContactForm()

    return render(request, "pages/contact.html", {"form": form})

# Vue pour la page d'inscription
def inscription(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Le compte sera inactif, nécessite validation admin
            user.save()
            messages.success(request, "Votre compte a été créé. Un administrateur doit l'activer.")
            
            # Au lieu de rediriger vers 'login', on revient sur la page d'inscription
            return redirect('inscription')  
    else:
        form = UserCreationForm()
    
    return render(request, 'pages/inscription.html', {'form': form})


# ✅ Afficher la liste des articles publiés
def liste_articles(request):
    articles = Article.objects.filter(status='publie').order_by('-date_publication')
    return render(request, 'pages/liste_articles.html', {'articles': articles})

# ✅ Afficher un article en détail avec ses commentaires, likes et notations
def detail_article(request, slug):
    article = get_object_or_404(Article, slug=slug, status='publie')
    commentaires = article.commentaires.all().order_by('-date_creation')
    moyenne_notes = article.notations.aggregate(Avg('note'))['note__avg'] or 0
    form_commentaire = CommentaireForm()
    form_notation = NotationForm()

    return render(request, 'pages/detail_article.html', {
        'article': article,
        'commentaires': commentaires,
        'moyenne_notes': moyenne_notes,
        'form_commentaire': form_commentaire,
        'form_notation': form_notation,
    })

# ✅ Ajouter un nouvel article (nécessite d’être connecté)
@login_required
def creer_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user
            article.status = 'attente'
            article.save()
            return redirect('liste_articles')
    else:
        form = ArticleForm()
    return render(request, 'pages/creer_article.html', {'form': form})

# ✅ Valider un article (réservé à l'admin)
@login_required  # On garde la vérification de connexion
def valider_article(request, article_id):
    # Vérification manuelle si l'utilisateur est un membre du staff
    if not request.user.is_staff:
        raise PermissionDenied  # Lève une exception si l'utilisateur n'est pas autorisé

    article = get_object_or_404(Article, id=article_id, status='attente')
    article.status = 'publie'
    article.date_publication = timezone.now()
    article.save()
    return redirect('admin:pages_article_changelist')

# ✅ Ajouter un commentaire sur un article
@login_required
def ajouter_commentaire(request, slug):
    article = get_object_or_404(Article, slug=slug, status='publie')
    if request.method == 'POST':
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.article = article
            commentaire.auteur = request.user
            commentaire.save()
            return redirect('detail_article', slug=article.slug)
    else:
        form = CommentaireForm()
    return render(request, 'pages/ajouter_commentaire.html', {'form': form, 'article': article})

# ✅ Système de like pour un article
@login_required
def aimer_article(request, slug):
    article = get_object_or_404(Article, slug=slug, status='publie')
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect('detail_article', slug=article.slug)

# ✅ Ajouter une note à un article
@login_required
def noter_article(request, slug):
    article = get_object_or_404(Article, slug=slug, status='publie')
    if request.method == 'POST':
        form = NotationForm(request.POST)
        if form.is_valid():
            note = int(form.cleaned_data['note'])
            Notation.objects.update_or_create(
                utilisateur=request.user, article=article, defaults={'note': note}
            )
    return redirect('detail_article', slug=article.slug)

# -----------------------------------------------------------------------------
# Ajout de fonctions factices pour éviter les erreurs, à remplacer par
# l'implémentation réelle
# -----------------------------------------------------------------------------

@login_required
def ajouter_article(request):
    # TODO: Implementer la logique pour ajouter un article
    return render(request, 'pages/ajouter_article.html')

@login_required
def supprimer_article(request, article_id):
    # TODO: Implementer la logique pour supprimer un article
    return redirect('liste_articles')