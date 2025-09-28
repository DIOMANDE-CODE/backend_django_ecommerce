from django.urls import path
from .views import creation_utilisateur

urlpatterns = [
    path('create/', creation_utilisateur,name='creation_utilisateur'),
]