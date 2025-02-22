from django.shortcuts import get_object_or_404
from ninja.router import Router

from users.schemas import UserRead, UserUpdate

from .models import User

router = Router()


@router.get(path="/me", response=UserRead)
def get_user(request):
    return request.auth


@router.post(path="/update", response=UserRead)
def update_user(request, user_update: UserUpdate):
    user = get_object_or_404(User, id=request.auth.id)
    for k, v in user_update.model_dump().items():
        setattr(user, k, v)
    user.save()
    return user
