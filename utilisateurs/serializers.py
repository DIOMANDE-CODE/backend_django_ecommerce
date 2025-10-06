from rest_framework import serializers
from .models import Utilisateur

# Serialization de Utilisateur
class UtilisateurSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    est_client = serializers.BooleanField(default=True)
    est_vendeur = serializers.BooleanField(default=False)

    class Meta :
        model = Utilisateur
        fields = ['id','email','password','photo_utilisateur','nom_utilisateur','prenoms_utilisateur','numero_tel_utilisateur','est_client','est_vendeur','provider','created_at','updated_at']
        read_only_fields = ['id','created_at','updated_at']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Utilisateur(**validated_data)
        user.set_password(password)
        user.save()
        return user