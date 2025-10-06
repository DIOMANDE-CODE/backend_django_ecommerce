from django.contrib import admin
from .models import OTP

# Register your models here.
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('numero_telephone','code_otp','date_envoi','est_verifie',)
    search_fields = ('numero_telephone',)
    ordering = ['numero_telephone']
