from django import forms
from .models import Article, Commentaire

class ContactForm(forms.Form):
    name = forms.CharField(label="Nom", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Votre Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label="Sujet", max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu']  # On ne permet pas de modifier le statut ou l'auteur ici
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control'}),
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