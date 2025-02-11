# pages/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),         # http://127.0.0.1:8000/
    path('services/', views.services, name='services'),  # http://127.0.0.1:8000/services/
]

from django.urls import path
from .views import test_email

urlpatterns = [
    path('test-email/', test_email, name='test_email'),
]
