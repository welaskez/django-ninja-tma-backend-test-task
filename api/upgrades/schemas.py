from ninja import ModelSchema, Schema

from .models import Upgrade


class UpgradeRead(ModelSchema):
    class Meta:
        model = Upgrade
        fields = ["id", "name", "photo", "price", "boost"]


class BuyUpgradeResponse(Schema):
    success: bool
    upgrade: UpgradeRead
    message: str
