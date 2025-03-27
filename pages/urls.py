from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),

    # Authentification
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('inscription/', views.inscription, name='inscription'),

    # Blog
    path('blog/', include('pages.blog_urls')),

    path('profil-entreprise/', views.profil_entreprise, name='profil_entreprise'),
    path("creer-article/", views.creer_article, name="creer_article"),


]