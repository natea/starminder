import pytest
import numpy as np
from django.core.exceptions import ValidationError
from starminder.content.models import Star, StarAnalysis, Tag, Reminder
from starminder.core.models import CustomUser


@pytest.mark.django_db
class TestStarAnalysisModel:
    @pytest.fixture
    def user(self):
        return CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com"
        )

    @pytest.fixture
    def star(self, user):
        reminder = Reminder.objects.create(user=user)
        return Star.objects.create(
            reminder=reminder,
            provider="github",
            provider_id="123",
            name="django",
            owner="django",
            owner_id="456",
            description="The Web framework",
            star_count=50000,
            repo_url="https://github.com/django/django"
        )

    def test_star_analysis_creation(self, star):
        """Test creating StarAnalysis with all fields"""
        analysis = StarAnalysis.objects.create(
            star=star,
            readme_content="# Django\nThe web framework",
            priority_score=150000.0,
            language="Python",
            health_score=0.9
        )

        assert analysis.star == star
        assert analysis.readme_content == "# Django\nThe web framework"
        assert analysis.priority_score == 150000.0
        assert analysis.language == "Python"
        assert analysis.health_score == 0.9

    def test_one_to_one_relationship(self, star):
        """Test that each Star can have only one StarAnalysis"""
        StarAnalysis.objects.create(star=star)

        with pytest.raises(Exception):  # IntegrityError
            StarAnalysis.objects.create(star=star)

    def test_embedding_storage(self, star):
        """Test storing and retrieving numpy embeddings"""
        # Create embedding (3072-dimensional vector)
        embedding = np.random.random(3072).astype(np.float32)

        analysis = StarAnalysis.objects.create(
            star=star,
            readme_embedding=embedding.tobytes()
        )

        # Retrieve and verify
        retrieved = StarAnalysis.objects.get(star=star)
        retrieved_embedding = np.frombuffer(retrieved.readme_embedding, dtype=np.float32)

        assert retrieved_embedding.shape == (3072,)
        np.testing.assert_array_almost_equal(embedding, retrieved_embedding)

    def test_tag_relationship(self, star):
        """Test ManyToMany relationship with tags"""
        analysis = StarAnalysis.objects.create(star=star)

        tag1 = Tag.objects.create(name="python", category="language")
        tag2 = Tag.objects.create(name="web", category="framework")

        analysis.tags.add(tag1, tag2)

        assert analysis.tags.count() == 2
        assert tag1 in analysis.tags.all()
        assert tag2 in analysis.tags.all()

    def test_analysis_tracking_fields(self, star):
        """Test tracking fields for job status"""
        analysis = StarAnalysis.objects.create(
            star=star,
            fetch_attempted=True,
            fetch_error="Rate limit exceeded",
            analysis_attempted=True,
            analysis_error=None
        )

        assert analysis.fetch_attempted is True
        assert analysis.fetch_error == "Rate limit exceeded"
        assert analysis.analysis_attempted is True
        assert analysis.analysis_error is None
