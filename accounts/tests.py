from django.test import TestCase
from django.urls import reverse

from .models import User


class RegisterTests(TestCase):
    def test_register_creates_user_with_chosen_role(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "shopowner",
                "email": "owner@example.com",
                "phone": "",
                "role": User.Role.OWNER,
                "password1": "SuperSecret123!",
                "password2": "SuperSecret123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username="shopowner")
        self.assertEqual(user.role, User.Role.OWNER)
        self.assertTrue(user.is_authenticated)

    def test_register_rejects_duplicate_email(self):
        User.objects.create_user(
            username="existing", email="dup@example.com", password="pw12345678"
        )
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "email": "dup@example.com",
                "phone": "",
                "role": User.Role.CUSTOMER,
                "password1": "SuperSecret123!",
                "password2": "SuperSecret123!",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())


class SuperuserRoleTests(TestCase):
    def test_superuser_is_always_admin_role(self):
        user = User.objects.create_superuser(
            username="root", email="root@example.com", password="pw12345678"
        )
        self.assertEqual(user.role, User.Role.ADMIN)
