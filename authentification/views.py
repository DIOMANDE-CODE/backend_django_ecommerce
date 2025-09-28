from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

# Create your views here.


# Implementation du Json Web Token (login, refresh token, deconnexion )
@api_view(['POST'])
@permission_classes([AllowAny])
def connexion_utilisateur(request):
    # Récupération des données
    email = request.data.get('email')
    password = request.data.get('password')

    # Vérifier que les champs sont vides
    if not email :
        return Response({
            "message_erreur":"champs email obligatoire"
        }, status=status.HTTP_400_BAD_REQUEST)
    if not password :
        return Response({
            "message_erreur":"champs mot de passe obligatoire"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    # Authentification du compte
    try :
        user = authenticate(username=email, password=password)

        if not user :
            return Response({
                "message_erreur":"Email ou mot de passe incorrecte"
            }, status=status.HTTP_401_UNAUTHORIZED)
        
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
    except Exception:
        return Response({
            "message_erreur":"Erreur de deconnexion"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)