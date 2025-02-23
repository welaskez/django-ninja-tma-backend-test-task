from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from tasks.models import Task
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
    tasks = models.ManyToManyField(Task, related_name="users")

    def update_balance(self):
        current_time = now()

        time_difference = Decimal((current_time - (self.last_login or current_time)).total_seconds())
        earned_tokens = self.income_per_second * time_difference

        self.balance += earned_tokens
        self.last_login = current_time
        self.save()

    @property
    def total_income_per_second(self):
        upgrade_bonus = sum(Decimal(value) for value in self.upgrades.values_list("boost", flat=True))
        return self.income_per_second + upgrade_bonus

    def __str__(self) -> str:
        return self.username
