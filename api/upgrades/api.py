from django.shortcuts import get_object_or_404
from ninja.router import Router
from users.models import User

from .models import Upgrade
from .schemas import UpgradeRead

router = Router()


@router.get(path="", response=list[UpgradeRead])
def get_upgrades(request):
    return Upgrade.objects.all()


@router.post(path="/buy/{upgrade_id}", response=UpgradeRead)
def buy_upgrade(request, upgrade_id: int):
    upgrade = get_object_or_404(Upgrade, id=upgrade_id)
    user = get_object_or_404(User, id=request.auth.id)
    user.upgrades.add(upgrade)
    user.save()

    return upgrade
