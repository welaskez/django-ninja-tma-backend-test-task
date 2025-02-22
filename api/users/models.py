from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from upgrades.models import Upgrade


class User(AbstractUser):
    tg_id = models.BigIntegerField(
        null=True,
        blank=True,
        unique=True,
        verbose_name=_("Telegram ID"),
    )
    photo = models.URLField(verbose_name=_("Profile photo"), null=True, blank=True)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        verbose_name=_("Balance"),
    )
    income_per_second = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1.0,
        verbose_name=_("Income per second"),
    )
    upgrades = models.ManyToManyField(Upgrade, related_name="users")

    @property
    def total_income_per_second(self):
        base_income = self.income_per_second
        upgrade_bonus = sum(self.upgrades.values_list("boost", flat=True))
        return base_income + upgrade_bonus

    def __str__(self) -> str:
        return self.username
