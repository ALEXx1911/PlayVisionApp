import pytest
from django.urls import reverse
from rest_framework import status
from apps.playvisionapi.test.factories import player_factory , team_factory, season_factory, competition_factory, player_season_stats_factory

@pytest.mark.django_db
class TestComparePageAPI:
    def test_compare_page_success(self, api_client, players_setup):
        players_list = players_setup()
        url = reverse('compare-players')
        response = api_client.get(f"{url}?player1={players_list['player1']['slug']}&player2={players_list['player2']['slug']}")

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) >= {'player1_data', 'player1_season_stats', 'player2_data', 'player2_season_stats'}

    def test_compare_page_player_not_found(self, api_client):
        url = reverse('compare-players')
        response = api_client.get(f"{url}?player1=non-existent-player&player2=another-non-existent-player")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "No Player matches the given query."

    def test_compare_page_missing_both_parameters(self, api_client):
        url = reverse('compare-players')
        response = api_client.get(f"{url}")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "The names of both players are required."

    def test_compare_page_missing_first_parameter(self, api_client, players_setup):
        players_list = players_setup()
        url = reverse('compare-players')
        response = api_client.get(f"{url}?player2={players_list['player2']['slug']}")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "The names of both players are required."
    
    def test_compare_page_missing_second_parameter(self, api_client, players_setup):
        players_list = players_setup()
        url = reverse('compare-players')
        response = api_client.get(f"{url}?player1={players_list['player1']['slug']}")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "The names of both players are required."
    
    def test_compare_page_same_players(self, api_client, players_setup):
        players_list = players_setup()
        url = reverse('compare-players')
        response = api_client.get(f"{url}?player1={players_list['player1']['slug']}&player2={players_list['player1']['slug']}")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "The names of the two players cannot be the same."


@pytest.fixture
def players_setup(player_factory,team_factory,season_factory, player_season_stats_factory):
    players_results = {}
    def _make(player1_name="Player One", player1_slug="player-one",
                player2_name="Player Two", player2_slug="player-two",
                season_year=2024):
        player1 = player_factory(pname=player1_name, slug=player1_slug)
        player2 = player_factory(pname=player2_name, slug=player2_slug)

        default_team = team_factory(title="Test Team", slug="test-team")
        default_season = season_factory(year_start=season_year, year_end=season_year + 1)
        player1_season_stats = player_season_stats_factory(player=player1, team=default_team, season=default_season)
        player2_season_stats = player_season_stats_factory(player=player2, team=default_team, season=default_season)

        players_results.update({
            "player1": {
                "pname": player1.pname,
                "slug": player1.slug,
                "season_stats": player1_season_stats
            },
            "player2": {
                "pname": player2.pname,
                "slug": player2.slug,
                "season_stats": player2_season_stats
            }
        })
        return players_results
    return _make
