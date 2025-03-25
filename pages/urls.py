from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),

    # Authentification
    path('login/', auth_views.LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('inscription/', views.inscription, name='inscription'),

    # Blog
    path('blog/', views.liste_articles, name='liste_articles'),
    path('blog/creer/', views.creer_article, name='creer_article'),
    path('blog/<slug:slug>/', views.detail_article, name='detail_article'),
    path('blog/<slug:slug>/commenter/', views.ajouter_commentaire, name='ajouter_commentaire'),
    path('blog/<slug:slug>/aimer/', views.aimer_article, name='aimer_article'),
    path('blog/<slug:slug>/noter/', views.noter_article, name='noter_article'),
    path('valider_article/<int:article_id>/', views.valider_article, name='valider_article'),
]
