from ninja.errors import HttpError
from ninja.router import Router

from users.schemas import UserRead

router = Router()


@router.get(path="/me", response=UserRead)
def get_user(request):
    user = request.auth
    user.update_balance()
    return user


@router.post(path="/update_balance", response=UserRead)
def update_user_balance(request, balance: int):
    user = request.auth
    if balance > 0:
        user.balance += balance
    else:
        raise HttpError(status_code=400, message="Invalid balance")
    user.save()
    return user
