from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegistrationTests(TestCase):

    def test_register_page_loads(self):
        response = self.client.get(reverse("register"))

        self.assertEqual(response.status_code, 200)

    def test_register_page_uses_correct_template(self):
        response = self.client.get(reverse("register"))

        self.assertTemplateUsed(
            response,
            "expenses/register.html"
        )

    def test_user_can_register(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "StrongPassword123!",
                "confirm_password": "StrongPassword123!",
            }
        )

        self.assertEqual(
            User.objects.filter(
                username="testuser"
            ).count(),
            1
        )

    def test_registration_rejects_password_mismatch(self):
        self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "StrongPassword123!",
                "confirm_password": "DifferentPassword123!",
            }
        )

        self.assertEqual(
            User.objects.filter(
                username="testuser"
            ).count(),
            0
        )

    def test_registration_rejects_duplicate_username(self):

        User.objects.create_user(
            username="testuser",
            password="StrongPassword123!"
        )

        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "email": "another@example.com",
                "password": "AnotherPassword123!",
                "confirm_password": "AnotherPassword123!",
            }
        )

        self.assertEqual(response.status_code, 200)