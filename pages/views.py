from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Article, Commentaire, Notation
from .forms import ArticleForm, CommentaireForm, NotationForm, ContactForm, EntrepriseCreationForm

import logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'pages/home.html')

def services(request):
    return render(request, 'pages/services.html')

def contact(request):
    if request.method == "POST":
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
                    recipient_list=["mohamed.benadrouche@gmail.com"],
                    fail_silently=False,
                )
                messages.success(request, "Votre message a bien été envoyé.")
                return redirect("contact")
            except Exception as e:
                messages.error(request, f"Erreur d'envoi : {e}")
    else:
        form = ContactForm()
    return render(request, "pages/contact.html", {"form": form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Connexion réussie.'})
            else:
                return redirect('home')
        else:
            errors = form.errors.as_json()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': errors})
    else:
        form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})

def inscription(request):
    if request.method == "POST":
        form = EntrepriseCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            user.entreprise_profile.company_name = form.cleaned_data['company_name']
            user.entreprise_profile.siret = form.cleaned_data['siret']
            user.entreprise_profile.phone = form.cleaned_data['phone']
            user.entreprise_profile.address = form.cleaned_data['address']
            user.entreprise_profile.save()
            messages.success(request, "Votre compte a été créé. Un administrateur doit l'activer.")
            return redirect('inscription')
    else:
        form = EntrepriseCreationForm()
    return render(request, 'pages/inscription.html', {'form': form})

def liste_articles(request):
    articles = Article.objects.filter(status='publie').order_by('-date_publication')
    return render(request, 'pages/liste_articles.html', {'articles': articles})


def detail_article(request, slug):
    article = get_object_or_404(Article, slug=slug, status='publie')
    commentaires = article.commentaires.all().order_by('-date_creation')
    moyenne_notes = 0  # Supprimée plus tard si notation retirée
    form_commentaire = CommentaireForm()

    if request.method == 'POST':
        form_commentaire = CommentaireForm(request.POST)
        if form_commentaire.is_valid():
            commentaire = form_commentaire.save(commit=False)
            commentaire.article = article
            commentaire.auteur = request.user
            commentaire.save()
            return redirect('detail_article', slug=article.slug)

    return render(request, 'pages/detail_article.html', {
        'article': article,
        'commentaires': commentaires,
        'form_commentaire': form_commentaire,
    })

@login_required
def creer_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.auteur = request.user
            article.status = 'publie'  # <-- permet la publication directe
            article.save()
            return redirect('liste_articles')
    else:
        form = ArticleForm()
    return render(request, 'pages/creer_article.html', {'form': form})

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

@login_required
def aimer_article(request, slug):
    article = get_object_or_404(Article, slug=slug, status='publie')
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect('detail_article', slug=article.slug)

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

@login_required
def profil_entreprise(request):
    user = request.user
    entreprise = user.entreprise_profile
    articles = Article.objects.filter(auteur=user)
    return render(request, 'pages/profil_entreprise.html', {
        'user': user,
        'entreprise': entreprise,
        'articles': articles,
    })

@login_required
def supprimer_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if article.auteur != request.user:
        raise PermissionDenied
    article.delete()
    return redirect('liste_articles')  # ou 'blog'


