from ninja import ModelSchema, Schema

from .models import User


class UserRead(ModelSchema):
    class Meta:
        model = User
        fields = ["username", "photo", "balance", "income_per_second", "upgrades"]


class UserUpdate(Schema):
    balance: int | None = None
    income_per_second: int | None = None
