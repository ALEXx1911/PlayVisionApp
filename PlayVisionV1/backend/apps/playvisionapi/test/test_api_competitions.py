import pytest
from django.urls import reverse
from rest_framework import status
from apps.playvisionapi.test.factories import competition_factory

@pytest.mark.django_db
class TestCompetitionAPI:
    def test_competition_list_success(self, api_client, competition_factory):
        competition1 = competition_factory(title="La Liga", slug="la-liga")
        competition2 = competition_factory(title="Premier League", slug="premier-league")

        url = reverse('competition-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data['countries'][0]['competitions'], list)
        assert response.data['countries'][0]['competitions'][0]['title'] in ["La Liga", "Premier League"]
        assert len(response.data['countries'][0]['competitions']) >= 0

