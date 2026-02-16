import pytest
from django.urls import reverse
from rest_framework import status
from apps.playvisionapi.test.factories import player_factory,team_factory, player_season_stats_factory, season_factory, competition_factory, player_competition_stats_factory

@pytest.mark.django_db
class TestPlayerAPI:
    URL = reverse('player-details', kwargs={'pname': 'test-player'})
    def test_player_details_success(
            self, 
            api_client, 
            player_setup,
            ):
        season,player,_, _ = player_setup()

        player_response = api_client.get(
            f"{self.URL}?season={season.year_start}"
        )
        assert player_response.status_code == status.HTTP_200_OK
        assert set(player_response.data.keys()) >= {'player_data', 'season_stats', 'competition_stats'}
        assert player_response.data['player_data']['pname'] == "Test Player"

    def test_player_details_include_season_stats(
            self, 
            api_client, 
            player_setup
            ):
        season, player, _, player_season_stats = player_setup()

        player_response = api_client.get(
            f"{self.URL}?season={season.year_start}"
        )
        assert player_response.status_code == status.HTTP_200_OK
        assert 'season_stats' in player_response.data
        assert player_response.data['season_stats'][0]['goals'] == player_season_stats.goals and \
        isinstance(player_response.data['season_stats'][0]['goals'], int)
        assert player_response.data['season_stats'][0]['assists'] == player_season_stats.assists

    def test_player_details_include_competitions_stats(
            self, 
            api_client, 
            player_setup
            ):
        season, player, player_competition_stats, _ = player_setup()

        player_response = api_client.get(
            f"{self.URL}?season={season.year_start}"
            )
        assert player_response.status_code == status.HTTP_200_OK
        assert 'competition_stats' in player_response.data
        assert len(player_response.data['competition_stats']) >= 1
        assert player_response.data['competition_stats'][0]['goals'] == player_competition_stats.goals and \
        isinstance(player_response.data['competition_stats'][0]['goals'], int)
        assert player_response.data['competition_stats'][0]['assists'] == player_competition_stats.assists

    def test_player_not_found(
            self, 
            api_client
            ):
        url = reverse('player-details', kwargs={'pname': 'non-existent-player'})
        player_response = api_client.get(url)

        assert player_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.fixture
def player_setup(player_factory, season_factory,competition_factory,team_factory,player_competition_stats_factory,player_season_stats_factory):
    def _make(player_name="Test Player",player_slug="test-player", season_year=2024, goals_data=10, assists_data=5, media_data=8.5, yellow_cards_data=2, cleansheets_data=5):
        
        default_season = season_factory(year_start=season_year, year_end=season_year + 1)
        default_player = player_factory(pname=player_name, slug=player_slug)
        default_team = team_factory(title="Test Team", slug="test-team")
        default_competition = competition_factory(title="Test Competition", slug="test-competition")
        default_player_competition_stats = player_competition_stats_factory(player=default_player, competition=default_competition, season=default_season, goals=goals_data , assists=assists_data, media=media_data, yellow_cards=yellow_cards_data, cleansheets=cleansheets_data)
        default_player_season_stats = player_season_stats_factory(player=default_player, team=default_team, season=default_season, goals=goals_data, assists=assists_data)
        return default_season , default_player , default_player_competition_stats , default_player_season_stats
    
    return _make
