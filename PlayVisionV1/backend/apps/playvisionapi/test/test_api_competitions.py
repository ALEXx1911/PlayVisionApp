import pytest
from django.urls import reverse
from rest_framework import status
from apps.playvisionapi.test.factories import competition_factory

@pytest.mark.django_db
class TestCompetitionListAPI:
    def test_competition_list_success(self, api_client, competition_factory):
        competition_factory(title="La Liga", slug="la-liga")
        competition_factory(title="Premier League", slug="premier-league")

        url = reverse('competition-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        countries = response.data.get('countries', [])

        assert isinstance(countries, list)
        assert len(countries) >= 1

        country1_competitions = countries[0].get('competitions', [])
        assert isinstance(country1_competitions, list)
        assert len(country1_competitions) >= 1

        country2_competitions = countries[1].get('competitions', [])
        assert isinstance(country2_competitions, list)
        assert len(country2_competitions) >= 1
        
        assert isinstance(country1_competitions[0],dict)
        assert isinstance(country2_competitions[0],dict)

        assert "La Liga" in country1_competitions[0].get('title') and "la-liga" in country1_competitions[0].get('slug')
        assert "Premier League" in country2_competitions[0].get('title') and "premier-league" in country2_competitions[0].get('slug')