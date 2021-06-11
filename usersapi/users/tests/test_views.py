import json
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from ..models import User
from ..serializers import GetUsersSerializer


client = APIClient()


class GetAllUsersTest(APITestCase):

    def setUp(self):
        User.objects.create_superuser(
            username='admin', password='admin')
        User.objects.create(
            username='Kirill', password='Kirill@$%167',
            first_name='Kirill', last_name='Ivanov')
        User.objects.create(
            username='Petr', password='Petr@$%167',
            first_name='Petr', last_name='Petrov')
        User.objects.create(
            username='Konstantin', password='Konstantin@$%167',
            first_name='Kosty', last_name='Larin')
        User.objects.create(
            username='Aleksey', password='Aleksey@$%167',
            first_name='Alex', last_name='Sidorov')

    def token_auth(self):
        resp = self.client.post(reverse('get_token'),
                                {'username': 'admin', 'password': 'admin'},
                                format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        token = resp.data['token']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_get_all_users(self):
        self.token_auth()
        response = client.get(reverse('get_all_users'),
                              data={'format': 'json'})
        response_data = response.data
        for key, value in response_data.items():
            if key == 'results':
                temp = value
        for response_user in temp:
            user_id = response_user['id']
            user_temp = User.objects.filter(id=user_id).first()
            serializer = GetUsersSerializer(user_temp)
            self.assertEqual(response_user, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleUserTest(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', password='admin')
        self.kirill = User.objects.create(
            username='Kirill', password='Kirill@$%167',
            first_name='Kirill', last_name='Ivanov')
        self.petr = User.objects.create(
            username='Petr', password='Petr@$%167',
            first_name='Petr', last_name='Petrov')
        self.konstantin = User.objects.create(
            username='Konstantin', password='Konstantin@$%167',
            first_name='Kosty', last_name='Larin')
        self.aleksey = User.objects.create(
            username='Aleksey', password='Aleksey@$%167',
            first_name='Alex', last_name='Sidorov')

    def token_auth(self):
        resp = self.client.post(reverse('get_token'),
                                {'username': 'admin', 'password': 'admin'},
                                format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        token = resp.data['token']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_get_single_valid_user(self):
        self.token_auth()
        response = client.get(
            reverse('get_user', kwargs={'pk': self.petr.pk}))
        user = User.objects.get(pk=self.petr.pk)
        serializer = GetUsersSerializer(user)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_invalid_user(self):
        resp = self.client.post(reverse('get_token'),
                                {'username': 'admin', 'password': 'admin'},
                                format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        token = resp.data['token']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = client.get(
            reverse('get_user', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateUserTest(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', password='admin')

        self.valid_payload = {
            "username": "Batman",
            "password": "Batman@$%16745",
            "first_name": "Roman",
            "last_name": "Ivanov",
            "is_active": 1
        }
        self.invalid_payload = {
            'username': 'batman',
            'password': 'Batman',
            'first_name': 'Roman',
            'last_name': 'Ivanov',
            'is_active': True
        }

    def token_auth(self):
        resp = self.client.post(reverse('get_token'),
                                {'username': 'admin', 'password': 'admin'},
                                format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in resp.data)
        token = resp.data['token']
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_create_valid_user(self):
        self.token_auth()
        response = client.post(
            reverse('create_user'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_user(self):
        self.token_auth()
        response = client.post(
            reverse('create_user'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
