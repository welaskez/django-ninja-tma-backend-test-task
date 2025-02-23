from core.auth.jwt import get_tokens
from django.test import TestCase
from ninja.testing import TestClient

from .api import router
from .models import User
from .schemas import UserRead


class UsersTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="username")
        tokens = get_tokens(str(self.user_1.id))

        self.client = TestClient(router, headers={"Authorization": f"Bearer {tokens.access_token}"})

    def test_me(self):
        response = self.client.get("/me")

        expected_response = UserRead.from_orm(self.user_1).model_dump()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)
