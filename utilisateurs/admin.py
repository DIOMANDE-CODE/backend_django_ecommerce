from django.contrib import admin
from .models import Utilisateur

# Register your models here.
@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('email','nom_utilisateur','prenoms_utilisateur','numero_tel_utilisateur','photo_utilisateur','est_client','est_vendeur','is_active','is_superuser','created_at', 'updated_at',)
    search_fields = ('email','nom_utilisateur')
    ordering = ['nom_utilisateur']
