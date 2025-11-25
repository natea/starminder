from django.conf import settings
from django.db.models import CASCADE, FloatField, ForeignKey, Manager
from django.db import models

from starminder.core.models import StarFieldsBase, TimestampedModel


class TempStar(TimestampedModel, StarFieldsBase):
    objects: "Manager[TempStar]"

    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    priority_score = FloatField(default=0.0, db_index=True)

    class Meta:
        verbose_name = "Temporary Star"
        indexes = [
            models.Index(fields=['-priority_score']),
        ]

    def __str__(self) -> str:
        return f"tmp: {self.owner}/{self.name}, {self.provider}, {self.user.username}"
