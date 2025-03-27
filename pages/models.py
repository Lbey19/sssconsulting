from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Article(models.Model):
    STATUS_CHOICES = [
        ('publie', 'Publié'),
        ('attente', 'En attente'),
    ]

    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_publication = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='attente')
    likes = models.ManyToManyField(User, related_name='likes_articles', blank=True)        
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre

class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.auteur.username} sur {self.article.titre}"

class Notation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name="notations", on_delete=models.CASCADE)
    note = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.article.titre}: {self.note}/5"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Profil de {self.user.username}"

class EntrepriseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='entreprise_profile')
    company_name = models.CharField("Nom de l'entreprise", max_length=100)
    siret = models.CharField("SIRET", max_length=14, blank=True)
    phone = models.CharField("Téléphone", max_length=20, blank=True)
    address = models.CharField("Adresse", max_length=255, blank=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"

# ✅ Signal unifié pour créer/mettre à jour les deux profils
@receiver(post_save, sender=User)
def create_or_update_profiles(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        EntrepriseProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
        if hasattr(instance, 'entreprise_profile'):
            instance.entreprise_profile.save()
