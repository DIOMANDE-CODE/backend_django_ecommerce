from django.urls import path
from .views import creation_utilisateur, detail_utilsateur

urlpatterns = [
    path('create/', creation_utilisateur,name='creation_utilisateur'),
    path('detail/', detail_utilsateur,name='detail_utilsateur'),
]