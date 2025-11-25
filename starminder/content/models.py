from django.conf import settings
from django.db.models import CASCADE, CharField, ForeignKey, IntegerField, Manager
import emoji

from starminder.core.models import StarFieldsBase, TimestampedModel


TIMESTAMP_FORMAT = "%A %Y-%m-%d %H:%M:%S"


class Reminder(TimestampedModel):
    objects: "Manager[Reminder]"
    star_set: "Manager[Star]"

    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    class Meta:
        verbose_name = "Reminder"

    def __str__(self) -> str:
        return f"{self.user.username}, {self.created_at.date()}"

    @property
    def title(self) -> str:
        return f"Reminder: {self.created_at.strftime(TIMESTAMP_FORMAT)}"


class Star(TimestampedModel, StarFieldsBase):
    objects: "Manager[Star]"

    reminder = ForeignKey(Reminder, on_delete=CASCADE)

    class Meta:
        verbose_name = "Star"

    def __str__(self) -> str:
        return f"{self.owner}/{self.name}, {self.provider}, {self.reminder}"

    @property
    def description_pretty(self) -> str:
        return emoji.emojize(self.description, language="alias")


class Tag(TimestampedModel):
    """Categorized tags for repository classification."""

    objects: "Manager[Tag]"

    CATEGORY_CHOICES = [
        ('language', 'Programming Language'),
        ('framework', 'Framework'),
        ('tool', 'Tool'),
        ('domain', 'Domain/Field'),
        ('topic', 'Topic'),
    ]

    name = CharField(max_length=100, unique=True, db_index=True)
    category = CharField(max_length=50, choices=CATEGORY_CHOICES)
    usage_count = IntegerField(default=0)

    class Meta:
        ordering = ['-usage_count', 'name']
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self) -> str:
        return self.name
