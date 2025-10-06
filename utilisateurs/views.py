from django.shortcuts import render
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Utilisateur
from .serializers import UtilisateurSerializer
import re

# Create your views here.

# Fonction de creation de compte utilisateur

@api_view(['POST'])
@permission_classes([AllowAny])
def creation_utilisateur(request):

    # Recupération des données
    identifiant = request.data.get('identifiant')
    password = request.data.get('password')

    # Verifier la presence des information
    if not identifiant :
        return Response({
            "message_erreur":"L'identifiant doit être soit un email ou un mot de passe'"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if not password :
        return Response({
            "message_erreur":"Mot de passe obligatoire"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verifier que l'email est valide
    if '@' in str(identifiant):
        try :
            validate_email(identifiant)
        except ValidationError:
            return Response(
           {
            'message_erreur':'Email invalide'
           }, status=status.HTTP_400_BAD_REQUEST
        )
    elif identifiant.isdigit():
        pattern = r'^(\+?\d{8,15})$'
        if not re.match(pattern,identifiant):
            return Response({
                "message_erreur":"Le numéro doit être au format : '+2250700000000' (entre 8 et 15 chiffres)."
            }, status=status.HTTP_400_BAD_REQUEST)
    else :
        return Response({
            "message_erreur":"Email ou numéro incorrect"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verifier que l'utilisateur n'existe pas
    if Utilisateur.objects.filter(email=identifiant).exists():
        return Response({
            'message_erreur':'Cet email existe dejà'
        }, status=status.HTTP_400_BAD_REQUEST)
    elif Utilisateur.objects.filter(numero_tel_utilisateur=identifiant).exists():
        return Response({
            'message_erreur':'Cet numéro existe dejà'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    # Creation du compte
    try :
        serializer = UtilisateurSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message_success':'Votre compte a été crée avec succès',
                'information_utilisateur':serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message_erreur":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({
            "message_erreur":"Une erreur interne est survenue. Veuillez ressayer plus tard."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Fonction pour accéder, modifer, supprimer l'utilisateur
@api_view(['GET','PUT','DELETE'])
def detail_utilsateur(request):

    # recupération de l'utilisateur connecté
    try :
        utilisateur = Utilisateur.objects.get(email=request.user)
    except Exception:
        return Response({
            "message_erreur":"Cet utilisateur n'existe pas."
        }, status=status.HTTP_400_BAD_REQUEST)

    # HTTP GET
    if request.method == 'GET':
        try:
            serializer = UtilisateurSerializer(utilisateur)
            return Response({
                "message_success":serializer.data
            }, status=status.HTTP_200_OK)
        except Exception :
            return Response({
                "message_erreur":serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception :
            return Response({
                "message_erreur":"Une erreur interne est surevenue. Veuillez ressayer plus tard"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # HTTP DELETE
    if request.method == 'DELETE':
        try :
            utilisateur.delete()
            return Response({
                "message_success":"Utilisateur supprimé"
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "message_erreur":"Une erreur interne est surevenue. Veuillez ressayer plus tard"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # HTTP PUT
    if request.method == 'PUT':
        try :
            serializer = UtilisateurSerializer(utilisateur,request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message_success":"Utilisateur modifié avec succès"
                }, status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response({
                "message_erreur":serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({
                "message_erreur":"Une erreur interne est surevenue. Veuillez ressayer plus tard"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)