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
            create_season_object,
            team_setup
            ):
        team = team_setup()
        season = create_season_object(2024)

        team_response = api_client.get(
            f"{self.URL}?season={season.year_start}"
            )
        assert team_response.status_code == status.HTTP_200_OK
        assert set(team_response.data.keys()) >= {
            'team', 
            'insights', 
            'player_stats', 
            'matches',
            'last_five_results'
            }
        assert team_response.data['team']['title'] == team.title

    def test_team_details_include_insights(
            self, 
            api_client,
            create_season_object , 
            team_insights_factory,
            team_setup
            ):
        team = team_setup()
        season = create_season_object(2024)
        team_insights_factory(
            team=team, season=season, 
            title="Insight Title", 
            description="Insight Description"
            )
        team_response = api_client.get(f"{self.URL}?season={season.year_start}")

        assert team_response.status_code == status.HTTP_200_OK
        assert 'insights' in team_response.data
        assert len(team_response.data['insights']) >= 1
        assert team_response.data['insights'][0]['title'] == team.team_insights.first().title

    def test_team_details_include_matches(
            self, 
            api_client, 
            team_setup, 
            create_season_object, 
            competition_factory, 
            match_factory,
            ):
        test_team_1 = team_setup()
        test_team_2 = team_setup(title="Away Team", slug="away-team")
        season = create_season_object(2024)
        competition1 = competition_factory(title="Test Competition", slug="test-competition")
        match_factory(home_team=test_team_1, 
                      away_team=test_team_2,
                      competition=competition1,
                      season=season
                      )
        match_factory(home_team=test_team_2,
                      away_team=test_team_1, 
                      competition=competition1, 
                      season=season
                      )
        team_response = api_client.get(f"{self.URL}?season={season.year_start}")

        assert team_response.status_code == status.HTTP_200_OK
        assert 'matches' in team_response.data
        assert len(team_response.data['matches']) >= 1
        assert team_response.data['matches'][0]['competition']['title'] == competition1.title
        assert isinstance(team_response.data['last_five_results'], list)
        assert len(team_response.data['last_five_results']) >= 1

    def test_team_details_include_player_stats(
            self, 
            api_client,
            create_players_with_stats,
            ):
        season = 2024
        
        players_list =  create_players_with_stats()
        team = players_list['player1']['team']

        url = reverse('team-details', kwargs={'title': team.slug})
        team_response = api_client.get(f"{url}?season={season}")

        assert team_response.status_code == status.HTTP_200_OK
        assert 'player_stats' in team_response.data
        assert len(team_response.data['player_stats']) == len(players_list)
        assert team_response.data['player_stats'][0]['player']['pname'] == players_list['player1']['pname']
    
    def test_team_details_not_found(
            self, 
            api_client,
            ):
        team_response = api_client.get(
            f"{self.URL}?season=2024"
            )
        assert team_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.fixture
def team_setup(team_factory):
    def _make(title="Test Team", slug="test-team"):
        return team_factory(title=title, slug=slug)
    return _make