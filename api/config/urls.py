from core.auth.api import router as auth_router
from core.auth.http_bearer import TelegramAuthBearer
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI, Router
from tasks.api import router as tasks_router
from upgrades.api import router as upgrades_router
from users.api import router as users_router

api = NinjaAPI(csrf=True)

auth_protected_router = Router(auth=TelegramAuthBearer())
auth_protected_router.add_router(prefix="users/", tags=["Users"], router=users_router)
auth_protected_router.add_router(prefix="upgrades/", tags=["Upgrades"], router=upgrades_router)
auth_protected_router.add_router(prefix="tasks/", tags=["Tasks"], router=tasks_router)

api.add_router(prefix="auth/", tags=["Authentication"], router=auth_router)
api.add_router(prefix="", router=auth_protected_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
]
