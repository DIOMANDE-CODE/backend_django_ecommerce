from django.db import models
from django.utils import timezone
import random

# Create your models here.

# Creation de la classe OTP

def generate_otp(self):
    return str(random.randint(100000,999999))

class OTP(models.Model):
    numero_telephone = models.CharField(max_length=20)
    code_otp = models.CharField(max_length=6, default=generate_otp)
    date_envoi = models.DateTimeField(default=timezone.now)
    est_verifie = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numero_telephone} - {self.code_otp}"

