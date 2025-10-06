from django.urls import path
from .views import connexion_utilisateur, deconnexion_utilisateur, renouvelation_token, renitialisation_password, changement_du_password, connexion_avec_googleAPI

urlpatterns = [
    path('login/', connexion_utilisateur,name='connexion_utilisateur'),
    path('logout/', deconnexion_utilisateur,name='deconnexion_utilisateur'),
    path('refresh/', renouvelation_token,name='renouvelation_token'),

    # Lien de rénitialisation de mot de passe
    path('password-reset/', renitialisation_password, name='renitialisation_password'),
    path('password-reset-confirm/<str:uid>/<str:token>/', changement_du_password, name='changement_du_password'),

    # Connexion avec Google API
    path('google/oauth2/', connexion_avec_googleAPI, name='google-oauth2'),

]