from django.urls import path
from . import views  # Importez le module views ici

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.liste_articles, name='liste_articles'),
    path('blog/creer/', views.creer_article, name='creer_article'),
    path('blog/<slug:slug>/', views.detail_article, name='detail_article'),
    path('blog/<slug:slug>/commenter/', views.ajouter_commentaire, name='ajouter_commentaire'),
    path('blog/<slug:slug>/aimer/', views.aimer_article, name='aimer_article'),
    path('blog/<slug:slug>/noter/', views.noter_article, name='noter_article'),
    path('valider_article/<int:article_id>/', views.valider_article, name='valider_article'),  # Ajout de l'URL de validation
]   