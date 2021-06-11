from django.test import TestCase
from ..models import User


class GetModelTest(TestCase):

    def setUp(self):
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

    def test_user_username(self):
        user_kirill = User.objects.get(username='Kirill')
        user_petr = User.objects.get(username='Petr')
        self.assertEqual(
            str(user_kirill), "Kirill")
        self.assertEqual(
            str(user_petr), "Petr")
