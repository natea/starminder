import pytest
from django.core.exceptions import ValidationError
from starminder.content.models import Tag


@pytest.mark.django_db
class TestTagModel:
    def test_tag_creation(self):
        """Test creating a tag with all fields"""
        tag = Tag.objects.create(
            name="python",
            category="language",
            usage_count=5
        )
        assert tag.name == "python"
        assert tag.category == "language"
        assert tag.usage_count == 5
        assert tag.created_at is not None

    def test_tag_name_unique(self):
        """Test that tag names must be unique"""
        Tag.objects.create(name="python", category="language")

        with pytest.raises(Exception):  # IntegrityError
            Tag.objects.create(name="python", category="framework")

    def test_tag_category_choices(self):
        """Test valid category choices"""
        valid_categories = ["language", "framework", "tool", "domain", "topic"]

        for category in valid_categories:
            tag = Tag.objects.create(
                name=f"test-{category}",
                category=category
            )
            assert tag.category == category

    def test_tag_str_representation(self):
        """Test string representation"""
        tag = Tag.objects.create(name="django", category="framework")
        assert str(tag) == "django"

    def test_tag_ordering(self):
        """Test tags ordered by usage_count desc, then name"""
        Tag.objects.create(name="alpha", category="language", usage_count=5)
        Tag.objects.create(name="beta", category="language", usage_count=10)
        Tag.objects.create(name="gamma", category="language", usage_count=5)

        tags = list(Tag.objects.all())
        assert tags[0].name == "beta"  # Highest usage_count
        assert tags[1].name == "alpha"  # Same usage, alphabetical
        assert tags[2].name == "gamma"
