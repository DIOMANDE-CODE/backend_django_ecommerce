from django.urls import path
from .views import connexion_utilisateur, deconnexion_utilisateur, renouvelation_token, renitialisation_password, changement_du_password, connexion_avec_googleAPI, envoyer_otp, verifier_otp

urlpatterns = [
    path('login/', connexion_utilisateur,name='connexion_utilisateur'),
    path('logout/', deconnexion_utilisateur,name='deconnexion_utilisateur'),
    path('refresh/', renouvelation_token,name='renouvelation_token'),

    # Lien de rénitialisation de mot de passe
    path('password-reset/', renitialisation_password, name='renitialisation_password'),
    path('password-reset-confirm/<str:uid>/<str:token>/', changement_du_password, name='changement_du_password'),

    # Lien Connexion avec Google API
    path('google/oauth2/', connexion_avec_googleAPI, name='google-oauth2'),

    # Lien verification OTP
    path('otp/envoyer/', envoyer_otp, name='envoyer_otp'),
    path('otp/verifier/', verifier_otp, name='verifier_otp'),
    
]