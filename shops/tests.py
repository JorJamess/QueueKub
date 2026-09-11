import datetime

from django.test import TestCase
from django.urls import reverse

from accounts.models import User

from .models import Shop


def make_shop(owner, **overrides):
    defaults = {
        "name": "Test Shop",
        "address": "1 Test Street",
        "open_time": datetime.time(9, 0),
        "close_time": datetime.time(18, 0),
    }
    defaults.update(overrides)
    return Shop.objects.create(owner=owner, **defaults)


class ShopPermissionTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner", password="pw12345678", role=User.Role.OWNER
        )
        self.other_owner = User.objects.create_user(
            username="owner2", password="pw12345678", role=User.Role.OWNER
        )
        self.customer = User.objects.create_user(
            username="cust", password="pw12345678", role=User.Role.CUSTOMER
        )

    def test_customer_cannot_create_shop(self):
        self.client.login(username="cust", password="pw12345678")
        response = self.client.get(reverse("shops:create"))
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(Shop.objects.count(), 0)

    def test_owner_can_create_shop(self):
        self.client.login(username="owner", password="pw12345678")
        response = self.client.post(
            reverse("shops:create"),
            {
                "name": "ABC Noodles",
                "description": "",
                "address": "123 Main St",
                "phone": "",
                "open_time": "09:00",
                "close_time": "21:00",
                "is_active": "on",
            },
        )
        shop = Shop.objects.get(name="ABC Noodles")
        self.assertRedirects(response, reverse("shops:detail", args=[shop.pk]))
        self.assertEqual(shop.owner, self.owner)

    def test_owner_cannot_edit_another_owners_shop(self):
        shop = make_shop(self.other_owner)
        self.client.login(username="owner", password="pw12345678")
        response = self.client.get(reverse("shops:edit", args=[shop.pk]))
        self.assertEqual(response.status_code, 404)


class ShopListTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner", password="pw12345678", role=User.Role.OWNER
        )

    def test_inactive_shops_are_hidden_from_list(self):
        make_shop(self.owner, name="Visible Shop", is_active=True)
        make_shop(self.owner, name="Hidden Shop", is_active=False)

        response = self.client.get(reverse("shops:list"))

        self.assertContains(response, "Visible Shop")
        self.assertNotContains(response, "Hidden Shop")

    def test_search_filters_by_name(self):
        make_shop(self.owner, name="Coffee Corner")
        make_shop(self.owner, name="Noodle House")

        response = self.client.get(reverse("shops:list"), {"q": "Coffee"})

        self.assertContains(response, "Coffee Corner")
        self.assertNotContains(response, "Noodle House")
