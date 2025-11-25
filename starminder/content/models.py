from django.conf import settings
from django.db.models import (
    CASCADE, BinaryField, BooleanField, CharField, DateTimeField,
    FloatField, ForeignKey, IntegerField, ManyToManyField, Manager,
    OneToOneField, TextField
)
from django.db import models
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


class StarAnalysis(TimestampedModel):
    """AI analysis and embeddings for a starred repository."""

    objects: "Manager[StarAnalysis]"

    # Core relationships
    star = OneToOneField(Star, on_delete=CASCADE, related_name='analysis')
    tags = ManyToManyField(Tag, related_name='stars', blank=True)

    # Content and embeddings
    readme_content = TextField(null=True, blank=True)
    readme_embedding = BinaryField(null=True, blank=True)  # numpy array as bytes
    description_embedding = BinaryField(null=True, blank=True)

    # Analysis metadata
    analysis_date = DateTimeField(null=True, blank=True)
    analysis_version = CharField(max_length=50, blank=True)  # e.g., "gpt-4-turbo-2024-04"
    priority_score = FloatField(default=0.0, db_index=True)

    # Repository health metrics
    last_commit_date = DateTimeField(null=True, blank=True)
    language = CharField(max_length=50, null=True, blank=True)
    health_score = FloatField(default=0.5)  # 0 (stale) to 1 (very active)

    # Processing tracking
    fetch_attempted = BooleanField(default=False)
    fetch_error = TextField(null=True, blank=True)
    analysis_attempted = BooleanField(default=False)
    analysis_error = TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Star Analysis"
        verbose_name_plural = "Star Analyses"
        indexes = [
            models.Index(fields=['-priority_score']),
            models.Index(fields=['analysis_date']),
        ]

    def __str__(self) -> str:
        return f"Analysis for {self.star}"
