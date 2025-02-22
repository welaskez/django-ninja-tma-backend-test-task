from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "balance", "income_per_second"]
    search_fields = ["tg_id", "username"]
