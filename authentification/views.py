from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from utilisateurs.models import Utilisateur
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from google.oauth2 import id_token
from google.auth.transport import requests

# Create your views here.


# Implementation du Json Web Token (login, refresh token, deconnexion )
@api_view(['POST'])
@permission_classes([AllowAny])
def connexion_utilisateur(request):
    # Récupération des données
    identifiant = request.data.get('identifiant')
    password = request.data.get('password')

    # Verification de la presence des données
    if identifiant is None:
        return Response({
            "message_erreur":"Email ou numéro de téléphone obligatoire"
        }, status=status.HTTP_400_BAD_REQUEST)
    if password is None:
        return Response({
            "message_erreur":"Saisissez votre mot de passe"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Vérifier que le compte existe
    try :
        if '@' in str(identifiant):
            user = Utilisateur.objects.get(email=identifiant)
        else :
            user = Utilisateur.objects.get(numero_tel_utilisateur=identifiant)
    except Utilisateur.DoesNotExist:
        return Response({
            "message_erreur":"Ce compte est introuvable"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    # Authentification du compte
    if not user.check_password(password):
        return Response({
            "message_erreur":"Mot de passe incorrecte"
        }, status=status.HTTP_400_BAD_REQUEST)
    try :
        
        if user.is_active == False :
            return Response({
                "message_erreur":"Compte inactif"
            }, status=status.HTTP_403_FORBIDDEN)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh_token":str(refresh),
            "access_token":str(refresh.access_token)
        }, status=status.HTTP_200_OK)

    except Exception :
        return Response({
            "message_erreur":"Une erreur interne est survenue. Veuillez ressayer plus tard."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def renouvelation_token(request):
    
    # Recupérer le refresh token
    refresh_token = request.data.get('refresh_token')

    if not refresh_token :
        return Response({
            "message_erreur":"Refresh Token Manquant"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try :
        refresh = RefreshToken(refresh_token)
        nouveau_token = str(refresh.access_token)
        return Response({
            "access_token":nouveau_token
        }, status=status.HTTP_200_OK)
    except Exception :
        return Response({
            "message_erreur":"Token invalide"
        }, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
def deconnexion_utilisateur(request):
    try :
        refresh_token = request.data.get("refresh_token")
        if refresh_token :
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({
            "message_success":"Vous êtes deconnecté"
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "message_erreur":"Erreur de deconnexion"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Implémentation de la fonctionnalité de rénitialisation de mot de passe
@api_view(['POST'])
@permission_classes([AllowAny])
def renitialisation_password(request):
    
    # Recupérer l'adresse email de l'utilisateur
    user_email = request.data.get("email")

    # Verifier que email n'est pas vide
    if not user_email :
        return Response({
            "message_erreur":"Le champs email est obligatoire"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verifier la validatité du mail
    try :
        validate_email(user_email)
    except Exception:
        return Response({
            "message_erreur":"email invalide"
        }, status=status.HTTP_400_BAD_REQUEST)
    

    # Verifier que l'utilisateur existe
    if not Utilisateur.objects.filter(email=user_email).exists():
        return Response({
            "message_erreur":"Compte inexistant"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Renitialisation du mot de passe
    try :
        user = Utilisateur.objects.get(email=user_email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f"{settings.RESET_PAGE}/auth/password-reset-confirm/{uid}/{token}/"

        send_mail(
        subject="Renitialisation de mot de passe",
        message=f"Renitialiser votre mot de passe {reset_url}",
        from_email= settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email]
    )
        return Response({
                "message_success":"Veuillez consulter votre email pour rénitialiser "
            }, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({
            "message_erreur":"Une erreur interne est survenue. Veuillez ressayer plus tard."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def changement_du_password(request, uid, token):
    # Recupération le nouveau mot de passe
    new_password = request.data.get("new_password")

    # Verifier que le champs email est vide
    if not new_password:
        return Response({"message_erreur":"Le champs new_password est obligatoire"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Décoder l’uid
        uid_decoded = force_str(urlsafe_base64_decode(uid))
        user = Utilisateur.objects.get(pk=uid_decoded)

        # Vérifier le token
        if not default_token_generator.check_token(user, token):
            return Response({"message_erreur":"Token invalide ou expiré"}, status=status.HTTP_400_BAD_REQUEST)

        # Appliquer le nouveau mot de passe
        user.set_password(new_password)
        user.save()

        return Response({"message_success":"Mot de passe réinitialisé avec succès"}, status=status.HTTP_200_OK)

    except Utilisateur.DoesNotExist:
        return Response({"message_erreur":"Utilisateur introuvable"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("Erreur changement password:", e)
        return Response({"message_erreur":"Erreur interne, veuillez réessayer"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Authentification avec GOOGLE OAUTH 2
@api_view(['POST'])
@permission_classes([AllowAny])
def connexion_avec_googleAPI(request):

    # Verification de l'existence du Token
    token = request.data.get('token')
    if not token:
        return Response({
            "message_erreur":"Token manquant"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Creation de l'utilisateur par le token de google
    try :
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.CLIENT_ID_GOOGLE)
        email = idinfo.get("email")
        nom = idinfo.get("name")
        image = idinfo.get("picture")

        user,created = Utilisateur.objects.get_or_create(
            email=email,
            defaults={
                "photo_utilisateur":image,
                "nom_utilisateur":nom.split()[-1],
                "prenoms_utilisateur":" ".join(nom.split()[:-1]),
                "provider":"google"
            }
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "email": user.email,
            "nom": user.nom_utilisateur,
            "prenoms": user.prenoms_utilisateur,
            "photo_profil": image,
            "nouvel_utilisateur": created
        })
    except Exception:
        return Response({
            "message_erreur":"Token Invalide"
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception :
        return Response({
            "message_erreur":"Erreur interne, veuillez réessayer"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)