from ninja import ModelSchema, Schema

from .models import User


class UserRead(ModelSchema):
    total_income_per_second: float

    class Meta:
        model = User
        fields = ["username", "photo", "balance", "upgrades"]

    @staticmethod
    def resolve_total_income_per_second(obj: User) -> float:
        return obj.total_income_per_second


class UserUpdate(Schema):
    balance: int | None = None
    income_per_second: int | None = None
