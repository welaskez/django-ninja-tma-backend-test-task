from django.contrib import admin

from .models import Upgrade


@admin.register(Upgrade)
class UpgradeModel(admin.ModelAdmin):
    list_display = ["name", "photo", "price", "boost"]
    list_editable = ["photo"]
