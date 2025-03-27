from django.urls import path, include
from pages import views

from .views import (
    liste_articles, detail_article, creer_article,
    ajouter_commentaire, aimer_article, noter_article
)

urlpatterns = [
    path('', liste_articles, name='liste_articles'),
    path('creer/', creer_article, name='creer_article'),
    path('blog/<slug:slug>/', views.detail_article, name='detail_article'),
    path('<slug:slug>/commenter/', ajouter_commentaire, name='ajouter_commentaire'),
    path('<slug:slug>/aimer/', aimer_article, name='aimer_article'),
    path('<slug:slug>/noter/', noter_article, name='noter_article'),
    path('article/<int:article_id>/supprimer/', views.supprimer_article, name='supprimer_article'),


]
