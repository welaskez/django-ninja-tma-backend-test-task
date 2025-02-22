from ninja import ModelSchema

from .models import Upgrade


class UpgradeRead(ModelSchema):
    class Meta:
        model = Upgrade
        fields = ["id", "name", "photo", "price", "boost"]
