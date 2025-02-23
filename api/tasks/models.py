from django.db import models
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    class TaskType(models.TextChoices):
        TELEGRAM = "telegram"
        X = "x"
        INSTAGRAM = "instagram"
        YOUTUBE = "youtube"

    photo = models.URLField(verbose_name=_("Task photo"))
    name = models.CharField(verbose_name=_("Task name"), max_length=150)
    link = models.URLField(verbose_name=_("Task link"))
    reward = models.DecimalField(verbose_name=_("Task reward"), max_digits=10, decimal_places=2)
    type = models.CharField(verbose_name=_("Task type"), max_length=32, choices=TaskType)
