import pytest
from django.urls import reverse
from rest_framework import status
from apps.playvisionapi.test.factories import team_factory, player_factory, player_season_stats_factory , competition_factory, season_factory , match_factory , team_insights_factory

@pytest.mark.django_db
class TestTeamAPI:
    URL = reverse('team-details', kwargs={'title': 'test-team'})
    def test_team_details_success(
            self, 
            api_client, 
            team_factory, 
            season_factory,
            ):
        team = team_factory(title = "Test Team", slug = "test-team")
        season = season_factory(year_start="2024", year_end="2025")

        team_response = api_client.get(
            f"{self.URL}?season={season.year_start}"
            )
        assert team_response.status_code == status.HTTP_200_OK
        assert set(team_response.data.keys()) >= {'team', 'insights', 'player_stats', 'matches','last_five_results'}
        assert team_response.data['team']['title'] == "Test Team"

    def test_team_details_include_insights(
            self, 
            api_client, 
            team_factory, 
            season_factory , 
            team_insights_factory,
            ):
        team = team_factory(title = "Test Team", slug = "test-team")
        season = season_factory(year_start="2024", year_end="2025")
        team_insights_factory(team=team, season=season, title="Insight Title", description="Insight Description")

        team_response = api_client.get(f"{self.URL}?season={season.year_start}")

        assert team_response.status_code == status.HTTP_200_OK
        assert 'insights' in team_response.data
        assert len(team_response.data['insights']) >= 1
        assert team_response.data['insights'][0]['title'] == "Insight Title"

    def test_team_details_include_matches(
            self, 
            api_client, 
            team_factory, 
            season_factory, 
            competition_factory, 
            match_factory,
            ):
        team = team_factory(title = "Test Team", slug = "test-team")
        season = season_factory(year_start="2024", year_end="2025")
        competition1 = competition_factory(title="Test Competition", slug="test-competition")
        match_factory(home_team=team, away_team=team_factory(), competition=competition1, season=season)
        match_factory(home_team=team_factory(), away_team=team, competition=competition1, season=season)

        team_response = api_client.get(f"{self.URL}?season={season.year_start}")

        assert team_response.status_code == status.HTTP_200_OK
        assert 'matches' in team_response.data
        assert len(team_response.data['matches']) >= 1
        assert team_response.data['matches'][0]['competition']['title'] == "Test Competition"
        assert isinstance(team_response.data['last_five_results'], list)
        assert len(team_response.data['last_five_results']) >= 1

    def test_team_details_include_player_stats(
            self, 
            api_client, 
            team_factory, 
            season_factory,
            player_factory, 
            player_season_stats_factory,
            ):
        team = team_factory(title = "Test Team", slug = "test-team")
        season = season_factory(year_start="2024", year_end="2025")
        
        player1 = player_factory(pname="John")
        player2 = player_factory(pname="Alan")
        player_season_stats_factory(player=player1, team=team, season=season, goals=7, assists=2)
        player_season_stats_factory(player=player2, team=team, season=season, goals=4, assists=5)

        team_response = api_client.get(f"{self.URL}?season={season.year_start}")

        assert team_response.status_code == status.HTTP_200_OK
        assert 'player_stats' in team_response.data
        assert len(team_response.data['player_stats']) == 2

        player_names = {stat['player']['pname'] for stat in team_response.data['player_stats']}
        assert player_names == {"John", "Alan"}

    def test_team_details_not_found(
            self, 
            api_client,
            ):
        team_response = api_client.get(
            f"{self.URL}?season=2024"
            )
        assert team_response.status_code == status.HTTP_404_NOT_FOUND