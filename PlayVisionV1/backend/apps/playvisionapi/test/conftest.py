import pytest
from rest_framework.test import APIClient
from apps.playvisionapi.test.factories import season_factory, player_factory, team_factory, player_season_stats_factory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_season_object(season_factory):
    def _create_season(year=2024):
        return season_factory(year_start=int(year),year_end=int(year) + 1)
    return _create_season

@pytest.fixture
def create_players_with_stats(
    player_factory,
    team_factory,
    create_season_object, 
    player_season_stats_factory
    ):
    """
    This fixture creates two players with their season stats for a given season. 
    It returns a dictionary containing the players' information and their season stats.
    """
    players_results = {}
    def _make(
            player1_name="Player One", 
            player1_slug="player-one",
            player2_name="Player Two", 
            player2_slug="player-two",
            season_year=2024
        ):
        player1 = player_factory(
            pname=player1_name,
            slug=player1_slug,
            position="DC"
        )
        player2 = player_factory(
            pname=player2_name,
            slug=player2_slug,
            position="GK"
        )

        default_team = team_factory(title="Test Team", slug="test-team")
        default_season = create_season_object(season_year)
        player1_season_stats = player_season_stats_factory(
            player=player1,
            team=default_team,
            season=default_season
        )
        
        player2_season_stats = player_season_stats_factory(
            player=player2,
            team=default_team, 
            season=default_season
        )
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