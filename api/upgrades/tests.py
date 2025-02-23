from core.auth.jwt import get_tokens
from django.test import TestCase
from ninja.testing import TestClient
from users.models import User

from upgrades.models import Upgrade

from .api import router
from .schemas import BuyUpgradeResponse


class UpgradesTest(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create(username="username", balance=150)

        self.upgrade_1 = Upgrade.objects.create(
            name="upgrade 1",
            photo="https://photos.com/some_photo_1",
            price=100,
            boost=1,
        )
        self.upgrade_2 = Upgrade.objects.create(
            name="upgrade 2",
            photo="https://photos.com/some_photo_2",
            price=200,
            boost=3,
        )

        tokens = get_tokens(str(self.user_1.id))
        self.client = TestClient(router, headers={"Authorization": f"Bearer {tokens.access_token}"})

    def test_get_upgrades(self):
        response = self.client.get("")

        expected_response = [
            {
                "id": upgrade["id"],
                "name": upgrade["name"],
                "photo": upgrade["photo"],
                "price": f"{upgrade['price']:.2f}",
                "boost": f"{upgrade['boost']:.2f}",
            }
            for upgrade in Upgrade.objects.values("id", "name", "photo", "price", "boost")
        ]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_buy_upgrade(self):
        response = self.client.post(f"/buy/{self.upgrade_1.id}")

        expected_response = BuyUpgradeResponse(
            success=True, upgrade=self.upgrade_1, message="Upgrade successfully bought"
        ).model_dump()
        expected_response["upgrade"]["price"] = f"{expected_response['upgrade']['price']:.2f}"
        expected_response["upgrade"]["boost"] = f"{expected_response['upgrade']['boost']:.2f}"

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_response)

    def test_buy_upgrade_not_enough_balance(self):
        response = self.client.post(f"/buy/{self.upgrade_2.id}")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Not enough balance")
