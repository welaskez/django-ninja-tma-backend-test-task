from ninja import ModelSchema

from .models import User


class UserRead(ModelSchema):
    total_income_per_second: float

    class Meta:
        model = User
        fields = ["username", "photo", "balance", "upgrades"]

    @staticmethod
    def resolve_total_income_per_second(obj: User) -> float:
        return obj.total_income_per_second
