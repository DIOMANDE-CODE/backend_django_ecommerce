from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

class UtilisateurTestAPI(APITestCase):

    def setUp(self):
        self.url = reverse('creation_utilisateur')
        

    def test_creation_utilisateur(self):
        data = {
            "email": "testapi@gmail.com",
            "password": "1234",
            "nom_utilisateur": "test",
            "prenoms_utilisateur": "api",
            "numero_tel_utilisateur": "0711399567",
            "est_client": True,
            "est_vendeur": False
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        User = get_user_model()
        user = User.objects.get(email="testapi@gmail.com")
        self.assertTrue(user.check_password("1234"))
        self.assertEqual(user.nom_utilisateur, "test")
        self.assertEqual(user.prenoms_utilisateur, "api")
        self.assertEqual(user.numero_tel_utilisateur, "0711399567")
        self.assertTrue(user.est_client)
        self.assertFalse(user.est_vendeur)

    def test_champs_obligatoire(self):
        data = {
            "email": "",
            "password": "",
            "nom_utilisateur": "",
            "prenoms_utilisateur": "",
            "numero_tel_utilisateur": "",
            "est_client": True,
            "est_vendeur": False
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
