from core.auth.jwt import get_tokens
from django.test import TestCase
from ninja.testing import TestClient

from .api import router
from .models import User


class UsersTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="username")
        tokens = get_tokens(str(self.user_1.id))

        self.client = TestClient(router, headers={"Authorization": f"Bearer {tokens.access_token}"})

    def test_get_user(self):
        response = self.client.get("/me")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], self.user_1.username)
        self.assertEqual(response.json()["balance"], "0.00")

    def test_update_balance_success(self):
        response = self.client.post(path="/update_balance?balance=50")

        self.assertEqual(response.status_code, 200)
        self.user_1.refresh_from_db()
        self.assertEqual(float(self.user_1.balance), 50.0)

    def test_update_balance_invalid(self):
        response = self.client.post(path="/update_balance?balance=-10")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Invalid balance")
