# sssconsulting

## Présentation

Ce projet est la refonte complète du site web de SSS Consulting, réalisée dans le cadre de mon stage. L'objectif principal était de moderniser l'interface, d'améliorer l'expérience utilisateur et d'ajouter de nouvelles fonctionnalités adaptées aux besoins de l'entreprise.

## Fonctionnalités principales et détails techniques

### Blog d’articles
- **Gestion des articles** : création, modification, suppression et affichage via les modèles et vues Django (`pages/models.py`, `pages/views.py`).
- **Commentaires** : ajout et affichage de commentaires sur chaque article grâce au modèle `Commentaire` et au formulaire associé.
- **Notation** : système de notes (1 à 5) pour chaque article, géré par le modèle `Notation`.

### Système d’authentification et profils
- **Inscription et connexion** : gestion des utilisateurs avec le système d’authentification Django, formulaires personnalisés et profils entreprise.
- **Sécurité** : accès protégé à certaines pages via les décorateurs Django.

### Formulaire de contact
- **Envoi d’e-mails** : formulaire de contact permettant l’envoi d’e-mails, géré côté backend avec Django (`pages/forms.py`, `pages/views.py`).

### Interface d’administration
- **Gestion des contenus** : interface d’administration personnalisée pour gérer articles, commentaires et notations via Django admin (`pages/admin.py`).

### Design moderne et responsive
- **Frontend** : utilisation de Bootstrap 5, CSS personnalisé et animations avec AOS.js pour une expérience utilisateur fluide et moderne.
- **Templates** : organisation claire des fichiers HTML et intégration de scripts pour les notifications et effets visuels.

## Technologies utilisées

- Django (backend)
- Bootstrap 5 (frontend)
- HTML/CSS/JS
- SQLite (base de données)
- AOS.js pour les animations

## Installation

1. Cloner le dépôt
2. Installer les dépendances Python (`pip install -r requirements.txt`)
3. Configurer les variables d'environnement dans `.env`
4. Lancer les migrations Django
5. Démarrer le serveur de développement

## Auteur

Projet réalisé par Benadrouche Yanis lors de mon stage chez SSS Consulting.
