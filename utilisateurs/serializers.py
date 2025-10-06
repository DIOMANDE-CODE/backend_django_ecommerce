from rest_framework import serializers
from .models import Utilisateur

# Serialization de Utilisateur
class UtilisateurSerializer(serializers.ModelSerializer):
    identifiant = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    est_client = serializers.BooleanField(default=True)
    est_vendeur = serializers.BooleanField(default=False)

    class Meta :
        model = Utilisateur
        fields = ['id','identifiant','email','password','photo_utilisateur','nom_utilisateur','prenoms_utilisateur','numero_tel_utilisateur','est_client','est_vendeur','provider','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

    def create(self, validated_data):
        identifiant = validated_data.pop('identifiant')
        password = validated_data.pop('password')

        if '@' in str(identifiant):
            user = Utilisateur.objects.create_user(email=identifiant, password=password, **validated_data)
        else:
            user = Utilisateur.objects.create_user(numero_tel_utilisateur=identifiant, password=password, **validated_data)

        return user