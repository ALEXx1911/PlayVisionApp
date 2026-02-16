import pytest
from rest_framework import status
from django.urls import reverse
from apps.playvisionapi.test.factories import player_factory, team_factory,match_factory, competition_factory, player_season_stats_factory

@pytest.mark.django_db
class TestHomePageAPI:
    URL = reverse('home-page')
    def test_home_page_success_with_matches_data(
        self,
        api_client,
        home_setup,
    ):
        _, _, match = home_setup()
        response = api_client.get(self.URL)
        print("Response Data:")
        print(response.data)
        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) >= {
            "competitions",
            "top_scorers",
            "top_media_players",
            "most_yellow_cards",
            "top_goalkeepers",
            "top_players_lineup",
        }
        assert len(response.data["competitions"]) == 1
        assert len(response.data["competitions"][0]["competition_matches"]) >= 1
        assert response.data["competitions"][0]["competition_matches"][0]["id"] == match.id
        
        

    def test_home_page_success_with_players_data(
        self,
        api_client,
        create_players_with_stats,
    ):
        
        create_players_with_stats(
            player1_name="Top Scorer",
            player1_slug="top-scorer",
            player2_name="Second Scorer",
            player2_slug="second-scorer",
        )

        response = api_client.get(self.URL)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["top_scorers"]) >= 1
        assert len(response.data["top_media_players"]) >= 1
        assert len(response.data["most_yellow_cards"]) >= 1
        assert len(response.data["top_goalkeepers"]) >= 1
        assert len(response.data["top_players_lineup"]) >= 1

    def test_home_page_empty_results(self, api_client):
        response = api_client.get(self.URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["competitions"] == []
        assert response.data["top_scorers"] == []
        assert response.data["top_media_players"] == []
        assert response.data["most_yellow_cards"] == []
        assert response.data["top_goalkeepers"] == []
        assert response.data["top_players_lineup"] == []

    def test_home_page_invalid_date_format(self, api_client):
        response = api_client.get(f"{self.URL}?date=2024-13-40")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Invalid format"

    def test_home_page_filters_by_date_season(
        self,
        api_client,
        create_players_with_stats,
    ):
        season = 2023

        create_players_with_stats(
            player1_name="Player One",
            player2_name="Player Two",
            season_year=season
        )
        response = api_client.get(f"{self.URL}?date=2023-08-17")

        assert response.status_code == status.HTTP_200_OK

@pytest.fixture
def home_setup(team_factory, competition_factory, create_season_object, match_factory):
    def _make(season_year=2024, match_date="2024-08-17"):
        season = create_season_object(season_year)
        competition = competition_factory(title="Test Competition", slug="test-competition")
        home_team = team_factory(title="Home Team", slug="home-team")
        away_team = team_factory(title="Away Team", slug="away-team")
        match = match_factory(
            match_date=match_date,
            home_team=home_team,
            away_team=away_team,
            competition=competition,
            season=season,
        )
        return season, competition, match

    return _make