from django.contrib import admin
from .models import Article, Commentaire, Notation
from django.utils import timezone

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'status', 'date_publication')
    list_filter = ('status', 'auteur')
    search_fields = ('titre', 'contenu')
    prepopulated_fields = {'slug': ('titre',)}
    actions = ['publier_articles']

    @admin.action(description="Publier les articles sélectionnés")
    def publier_articles(modeladmin, request, queryset):
        queryset.update(status='publie', date_publication=timezone.now())

@admin.register(Commentaire)
class CommentaireAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'article', 'date_creation')
    list_filter = ('auteur', 'article')
    search_fields = ('contenu',)

@admin.register(Notation)
class NotationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'article', 'note')
    list_filter = ('utilisateur', 'article', 'note')