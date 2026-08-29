from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class LoginTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="StrongPassword123!"
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_uses_correct_template(self):
        response = self.client.get(reverse("login"))
        self.assertTemplateUsed(response, "expenses/login.html")

    def test_user_can_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "StrongPassword123!",
            }
        )

        self.assertEqual(response.status_code, 302)

    def test_login_fails_with_wrong_password(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "WrongPassword123!",
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_login_fails_with_unknown_username(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "unknownuser",
                "password": "StrongPassword123!",
            }
        )

        self.assertEqual(response.status_code, 200)