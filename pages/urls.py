from django.urls import path
from .views import home, services, contact, test_email  # Importation des vues

urlpatterns = [
    path('', home, name='home'),  # http://127.0.0.1:8000/
    path('services/', services, name='services'),  # http://127.0.0.1:8000/services/
    path('contact/', contact, name='contact'),  # Page de contact
    path('test-email/', test_email, name='test_email'),  # Test d'envoi d'email
]

