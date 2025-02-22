from django.db import models
from django.utils.translation import gettext_lazy as _


class Upgrade(models.Model):
    name = models.CharField(verbose_name=_("Upgrade name"), max_length=150)
    photo = models.URLField(verbose_name=_("Upgrade photo"))
    price = models.DecimalField(
        verbose_name=_("Upgrade price"),
        max_digits=10,
        decimal_places=2,
    )
    boost = models.DecimalField(
        verbose_name=_("Balance per hour boost"),
        max_digits=10,
        decimal_places=2,
        default=1.0,
    )

    def __str__(self):
        return self.name
