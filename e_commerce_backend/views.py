from rest_framework.decorators import api_view
from django.http import JsonResponse

@api_view(['GET'])
def acceuil(request):
    return JsonResponse({
        "message":"Bienvenue sur mon serveur django"
    })