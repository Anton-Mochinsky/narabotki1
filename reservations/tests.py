from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        url = reverse('register_user')
        data = {
            'email': 'testuser@exampleq.com',
            'password': 'password123',
            'phone_number': '1234567897',
            'name': 'Test User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)


from rest_framework.test import APITestCase
from django.urls import reverse


class LoginTestCase(APITestCase):

    def test_login(self):
        url = reverse('login_user')
        data = {
            'email': 'testuser@exampleq.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)




class TableAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@exampleq.com', password='password123')

    def test_table_list_with_authentication(self):
        url = reverse('table_list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


