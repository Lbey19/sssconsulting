from django.db import models
# blog/models.py
from django.contrib.auth.models import User
from django.utils.text import slugify

class Article(models.Model):
    STATUS_CHOICES = [
        ('publie', 'Publié'),
        ('attente', 'En attente'),
    ]
    
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='attente')
    likes = models.ManyToManyField(User, related_name='likes_articles', blank=True)
    date_publication = models.DateTimeField(null=True, blank=True)  # 🔹 Ajouté ici
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.auteur.username} sur {self.article.titre}"

class Notation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    note = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.article.titre}: {self.note}/5"