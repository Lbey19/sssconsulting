"""
URL configuration for sssconsulting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# sssconsulting/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from pages import views  # Ajout de cette ligne


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),  # Inclure les URLs de l'application pages
    path('accounts/login/', views.login_view, name='login'),
    
]



