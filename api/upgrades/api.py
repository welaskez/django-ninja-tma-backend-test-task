from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from ninja.router import Router
from users.models import User

from .models import Upgrade
from .schemas import BuyUpgradeResponse, UpgradeRead

router = Router()


@router.get(path="", response=list[UpgradeRead])
def get_upgrades(request):
    return Upgrade.objects.all()


@router.post(path="/buy/{upgrade_id}", response=BuyUpgradeResponse)
def buy_upgrade(request, upgrade_id: int):
    upgrade = get_object_or_404(Upgrade, id=upgrade_id)
    user = get_object_or_404(User, id=request.auth.id)

    if user.balance >= upgrade.price:
        user.balance -= upgrade.price
    else:
        raise HttpError(status_code=400, message="Not enough balance")

    user.upgrades.add(upgrade)
    user.save()

    return BuyUpgradeResponse(success=True, upgrade=upgrade, message="Upgrade successfully bought")
