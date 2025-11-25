import pytest
from django.core.exceptions import ValidationError
from starminder.content.models import ClusterAssignment, Star, Reminder
from starminder.core.models import CustomUser


@pytest.mark.django_db
class TestClusterAssignmentModel:
    @pytest.fixture
    def user(self):
        return CustomUser.objects.create_user(username="testuser")

    @pytest.fixture
    def stars(self, user):
        reminder = Reminder.objects.create(user=user)
        return [
            Star.objects.create(
                reminder=reminder,
                provider="github",
                provider_id=str(i),
                name=f"repo{i}",
                owner="owner",
                owner_id="123",
                description="Test repo",
                star_count=1000,
                repo_url=f"https://github.com/owner/repo{i}"
            )
            for i in range(3)
        ]

    def test_cluster_assignment_creation(self, stars):
        """Test creating cluster assignment"""
        assignment = ClusterAssignment.objects.create(
            cluster_id=5,
            star=stars[0],
            centroid_distance=0.25
        )

        assert assignment.cluster_id == 5
        assert assignment.star == stars[0]
        assert assignment.centroid_distance == 0.25
        assert assignment.generated_at is not None

    def test_unique_cluster_star_combination(self, stars):
        """Test that (cluster_id, star) must be unique"""
        ClusterAssignment.objects.create(
            cluster_id=5,
            star=stars[0],
            centroid_distance=0.25
        )

        with pytest.raises(Exception):  # IntegrityError
            ClusterAssignment.objects.create(
                cluster_id=5,
                star=stars[0],
                centroid_distance=0.30
            )

    def test_same_star_different_clusters(self, stars):
        """Test that a star can only be in one cluster at a time"""
        ClusterAssignment.objects.create(
            cluster_id=5,
            star=stars[0],
            centroid_distance=0.25
        )

        # Same star, different cluster - should fail with unique constraint
        with pytest.raises(Exception):
            ClusterAssignment.objects.create(
                cluster_id=10,
                star=stars[0],
                centroid_distance=0.30
            )

    def test_same_cluster_multiple_stars(self, stars):
        """Test that a cluster can contain multiple stars"""
        for star in stars:
            ClusterAssignment.objects.create(
                cluster_id=5,
                star=star,
                centroid_distance=0.25
            )

        cluster_5_assignments = ClusterAssignment.objects.filter(cluster_id=5)
        assert cluster_5_assignments.count() == 3

    def test_query_by_cluster(self, stars):
        """Test querying assignments by cluster"""
        # Cluster 5 has 2 stars
        ClusterAssignment.objects.create(cluster_id=5, star=stars[0], centroid_distance=0.1)
        ClusterAssignment.objects.create(cluster_id=5, star=stars[1], centroid_distance=0.2)

        # Cluster 10 has 1 star
        ClusterAssignment.objects.create(cluster_id=10, star=stars[2], centroid_distance=0.15)

        cluster_5 = ClusterAssignment.objects.filter(cluster_id=5).order_by('centroid_distance')
        assert cluster_5.count() == 2
        assert cluster_5[0].star == stars[0]  # Closest to centroid
        assert cluster_5[1].star == stars[1]
