from django import forms
from .models import Article, Commentaire
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ContactForm(forms.Form):
    name = forms.CharField(label="Nom", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Votre Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label="Sujet", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'image']  # PAS 'auteur' ici
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }



class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ['contenu']
        widgets = {
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class NotationForm(forms.Form):  # Un simple formulaire pour la note
    note = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 6)],  # Choix de 1 à 5
        widget=forms.RadioSelect,  # Affichage en boutons radio
        label="Note"
    )

class UserProfileCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=False, label="Téléphone")
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Bio")

    class Meta:
        model = User
        fields = ["username", "email", "phone", "bio", "password1", "password2"]


class EntrepriseCreationForm(UserCreationForm):
    company_name = forms.CharField(label="Nom de l'entreprise", max_length=100, required=True)
    siret = forms.CharField(label="SIRET", max_length=14, required=False)
    phone = forms.CharField(label="Téléphone", max_length=20, required=False)
    address = forms.CharField(label="Adresse", max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'company_name', 'siret', 'phone', 'address', 'password1', 'password2']


