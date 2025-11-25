import pytest
from starminder.implementations.models import TempStar
from starminder.core.models import CustomUser


@pytest.mark.django_db
class TestTempStarPriority:
    @pytest.fixture
    def user(self):
        return CustomUser.objects.create_user(username="testuser")

    def test_temp_star_has_priority_score(self, user):
        """Test that TempStar has priority_score field"""
        temp_star = TempStar.objects.create(
            user=user,
            provider="github",
            provider_id="123",
            name="django",
            owner="django",
            owner_id="456",
            description="Web framework",
            star_count=50000,
            repo_url="https://github.com/django/django",
            priority_score=150000.0
        )

        assert temp_star.priority_score == 150000.0

    def test_priority_score_defaults_to_zero(self, user):
        """Test that priority_score defaults to 0.0"""
        temp_star = TempStar.objects.create(
            user=user,
            provider="github",
            provider_id="123",
            name="test",
            owner="owner",
            owner_id="456",
            description="Test",
            star_count=100,
            repo_url="https://github.com/owner/test"
        )

        assert temp_star.priority_score == 0.0

    def test_query_by_priority_score(self, user):
        """Test querying TempStars by priority score"""
        TempStar.objects.create(
            user=user, provider="github", provider_id="1",
            name="low", owner="owner", owner_id="123",
            star_count=100, repo_url="https://github.com/owner/low",
            priority_score=100.0
        )
        TempStar.objects.create(
            user=user, provider="github", provider_id="2",
            name="high", owner="owner", owner_id="123",
            star_count=10000, repo_url="https://github.com/owner/high",
            priority_score=30000.0
        )
        TempStar.objects.create(
            user=user, provider="github", provider_id="3",
            name="medium", owner="owner", owner_id="123",
            star_count=1000, repo_url="https://github.com/owner/medium",
            priority_score=2000.0
        )

        # Query by priority descending
        ordered = list(TempStar.objects.filter(user=user).order_by('-priority_score'))

        assert ordered[0].name == "high"
        assert ordered[1].name == "medium"
        assert ordered[2].name == "low"
