from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
# Create your models here.

# Verification des numéros
verification_numero_tel = RegexValidator (
    regex=r'^\+?1?\d{9,15}$',
    message="Le numéro doit être au format : '+2250700000000' (jusqu'à 15 chiffres)."
)

# Attribution d'une photo de profil par defaut
def photo_profil_par_defaut():
    return 'photo-profil-defaut.jpg'

class UtilisateurManager(BaseUserManager):
    
    # Creation de la fonction de creation d'un utilisateur
    def create_user(self, email, nom_utilisateur, prenoms_utilisateur, numero_tel_utilisateur, password=None, **extra_fields):

        # Verification que tous les champs sont remplis
        if not email :
            raise ValueError("Le champs (email) est obligatoire")
        if not nom_utilisateur :
            raise ValueError("Le champs (nom_utilisateur) est obligatoire")
        if not prenoms_utilisateur :
            raise ValueError("Le champs (prenoms_utilisateur) est obligatoire")
        if not numero_tel_utilisateur :
            raise ValueError("Le champs (numero_tel_utilisateur) est obligatoire")
        
        # Definir des valeurs par defaut
        extra_fields.setdefault('est_client', True)
        extra_fields.setdefault('est_vendeur', False)
        
        # Creation du compte
        email = self.normalize_email(email)
        user = self.model(email=email, nom_utilisateur=nom_utilisateur, prenoms_utilisateur=prenoms_utilisateur, numero_tel_utilisateur=numero_tel_utilisateur, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, nom_utilisateur, prenoms_utilisateur, numero_tel_utilisateur, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if not password:
            raise ValueError("Le superutilisateur doit avoir un mot de passe")

        return self.create_user(
            email=email,
            nom_utilisateur=nom_utilisateur,
            prenoms_utilisateur=prenoms_utilisateur,
            numero_tel_utilisateur=numero_tel_utilisateur,
            password=password, 
            **extra_fields
        )
class Utilisateur(AbstractBaseUser, PermissionsMixin):
    
    # Creation des attributs de la tables utilisateur
    email = models.EmailField(unique=True, verbose_name="Adresse Email")
    nom_utilisateur = models.CharField(max_length=50, verbose_name="Nom")
    prenoms_utilisateur = models.CharField(max_length=200, verbose_name="Prenoms")
    numero_tel_utilisateur = models.CharField(max_length=30, verbose_name="Numero de téléphone", validators=[verification_numero_tel])
    photo_utilisateur = models.ImageField(upload_to='photo_profil_utilisateur/', default=photo_profil_par_defaut, blank=True, null=True, verbose_name="Photo de profil")
    est_client = models.BooleanField(default=True)
    est_vendeur = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Activer la connexion par Email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom_utilisateur','prenoms_utilisateur','numero_tel_utilisateur']

    objects = UtilisateurManager()

    def __str__(self):
        return self.email
