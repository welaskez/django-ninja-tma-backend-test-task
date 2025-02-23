from ninja.router import Router

from users.schemas import UserRead

router = Router()


@router.get(path="/me", response=UserRead)
def get_user(request):
    return request.auth
