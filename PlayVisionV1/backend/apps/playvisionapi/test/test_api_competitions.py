import pytest
from django.urls import reverse
from rest_framework import status
from apps.playvisionapi.test.factories import competition_factory

@pytest.mark.django_db
class TestCompetitionListAPI:
    URL = reverse('competitions-list')
    def test_competition_list_success(
            self, 
            api_client, 
            competition_setup
        ):
        test_competiton_1 = competition_setup()

        response = api_client.get(self.URL)
        assert response.status_code == status.HTTP_200_OK
        countries = response.data.get('countries', [])

        assert isinstance(countries, list)
        assert len(countries) >= 1

    def test_competition_list_multiple_competitions(
            self, 
            api_client, 
            competition_setup
        ):

        test_competiton_1 = competition_setup(title="La Liga", slug="la-liga")
        test_competiton_2 = competition_setup(title="Premier League", slug="premier-league")
        
        response = api_client.get(self.URL)
        countries = response.data.get('countries', [])

        country1_competitions = countries[0].get('competitions', [])
        assert isinstance(country1_competitions, list)
        assert len(country1_competitions) >= 1

        country2_competitions = countries[1].get('competitions', [])
        assert isinstance(country2_competitions, list)
        assert len(country2_competitions) >= 1
        
        assert isinstance(country1_competitions[0],dict)
        assert isinstance(country2_competitions[0],dict)

        assert test_competiton_1.title in country1_competitions[0].get('title')
        assert test_competiton_1.slug in country1_competitions[0].get('slug')
        assert test_competiton_2.title in country2_competitions[0].get('title') 
        assert test_competiton_2.slug in country2_competitions[0].get('slug')