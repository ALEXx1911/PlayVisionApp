import pytest
from django.urls import reverse
from rest_framework import status
from apps.playvisionapi.models import Team , Season
from apps.playvisionapi.test.factories import team_factory, season_factory

@pytest.mark.django_db
class TestTeamAPI:
    def test_team_details_success(self, api_client, team_factory, season_factory):
        team = team_factory(title = "Test Team", slug = "test-team")
        season = season_factory(year_start="2024", year_end="2025")

        url = reverse('team-details', kwargs={'title': team.slug})
        response = api_client.get(f"{url}?season={season.year_start}")

        assert response.status_code == status.HTTP_200_OK
        assert response.data['team']['title'] == "Test Team"

    def test_team_details_not_found(self, api_client):
        url = reverse('team-details', kwargs={'title': 'non-existent-team'})
        response = api_client.get(f"{url}?season=2024")

        assert response.status_code == status.HTTP_404_NOT_FOUND