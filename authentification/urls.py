from django.urls import path
from .views import connexion_utilisateur, deconnexion_utilisateur, renouvelation_token

urlpatterns = [
    path('login/', connexion_utilisateur,name='connexion_utilisateur'),
    path('logout/', deconnexion_utilisateur,name='deconnexion_utilisateur'),
    path('refresh/', renouvelation_token,name='renouvelation_token'),
]