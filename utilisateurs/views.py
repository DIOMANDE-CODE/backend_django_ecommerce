from django.shortcuts import render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Utilisateur
from .serializers import UtilisateurSerializer

# Create your views here.

# Fonction de creation de compte utilisateur

@api_view(['POST'])
@permission_classes([AllowAny])
def creation_utilisateur(request):

    # Recupération des données
    email = request.data.get('email')
    nom_utilisateur = request.data.get('nom_utilisateur')
    prenoms_utilisateur = request.data.get('prenoms_utilisateur')
    numero_tel_utilisateur = request.data.get('numero_tel_utilisateur')

    # Verifier la presence des information
    if not email :
        return Response({
            "message_erreur":"le champs email est obligatoire"
        }, status=status.HTTP_400_BAD_REQUEST)
    if not nom_utilisateur :
        return Response({
            "message_erreur":"le champs (nom utilisateur) est obliagatoire"
        }, status=status.HTTP_400_BAD_REQUEST)
    if not prenoms_utilisateur :
        return Response({
            "message_erreur":"le champs (prenoms utilisateur) est obliagatoire"
        }, status=status.HTTP_400_BAD_REQUEST)
    if not numero_tel_utilisateur :
        return Response({
            "message_erreur":"le champs (numero_tel_utilisateur) est obliagatoire"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verifier que l'email est valide
    try :
        validate_email(email)
    except ValidationError:
        return Response(
           {
            'message_erreur':'Email invalide'
           }, status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verifier que l'email n'existe pas
    if Utilisateur.objects.filter(email=email).exists():
        return Response({
            'message_erreur':'Cet email existe dejà'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Creation du compte
    try :
        serializer = UtilisateurSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message_success':'Votre compte a été crée avec succès',
                'information_utilisateur':serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message_erreur":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception :
        return Response({
            "message_erreur":"Une erreur interne est survenue. Veuillez ressayer plus tard."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)