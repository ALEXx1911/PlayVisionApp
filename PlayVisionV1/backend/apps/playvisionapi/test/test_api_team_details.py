import pytest
from datetime import date, timedelta
from django.urls import reverse
from rest_framework import status
from apps.playvisionapi.test.factories import team_factory, player_factory, player_season_stats_factory , competition_factory, season_factory , match_factory , team_insights_factory

@pytest.mark.django_db
class TestTeamAPI:
    TEAM_DETAILS_URL = reverse('team-details', kwargs={'title': 'test-team'})
    TEAM_MATCHES_URL = reverse('team-matches', kwargs={'title': 'test-team'})

    def test_team_details_success(
            self, 
            api_client,
            create_season_object,
            team_setup
            ):
        team = team_setup()
        season = create_season_object(2024)

        team_response = api_client.get(
            f"{self.TEAM_DETAILS_URL}?season={season.year_start}"
            )
        assert team_response.status_code == status.HTTP_200_OK
        assert set(team_response.data.keys()) >= {
            'team', 
            'insights', 
            'player_stats', 
            'team_lineup',
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
        team_response = api_client.get(f"{self.TEAM_DETAILS_URL}?season={season.year_start}")

        assert team_response.status_code == status.HTTP_200_OK
        assert 'insights' in team_response.data
        assert len(team_response.data['insights']) >= 1
        assert team_response.data['insights'][0]['title'] == team.team_insights.first().title

    def test_team_matches_success_with_pagination(
            self, 
            api_client, 
            team_setup, 
            create_season_object, 
            competition_factory, 
            match_factory,
            ):
        test_team_1 = team_setup()
        test_team_2 = team_setup(title="Away Team", slug="away-team")
        test_team_3 = team_setup(title="Away Team 2", slug="away-team-2")
        season = create_season_object(2024)
        competition1 = competition_factory(title="Test Competition", slug="test-competition")
        base_date = date(2024, 1, 1)

        match_factory(home_team=test_team_1, 
                      away_team=test_team_2,
                      competition=competition1,
                      season=season,
                      match_date=base_date
                      )
        match_factory(home_team=test_team_2,
                      away_team=test_team_1, 
                      competition=competition1, 
                      season=season,
                      match_date=base_date + timedelta(days=1)
                      )
        match_factory(home_team=test_team_1,
                      away_team=test_team_3,
                      competition=competition1,
                      season=season,
                      match_date=base_date + timedelta(days=2)
                      )
        team_response = api_client.get(f"{self.TEAM_MATCHES_URL}?season={season.year_start}&offset=0&limit=2")

        assert team_response.status_code == status.HTTP_200_OK
        assert 'matches' in team_response.data
        assert len(team_response.data['matches']) == 2
        assert team_response.data['matches'][0]['competition']['title'] == competition1.title
        assert team_response.data['total'] == 3
        assert team_response.data['offset'] == 0
        assert team_response.data['limit'] == 2
        assert team_response.data['has_more'] is True

    def test_team_matches_invalid_pagination(
            self,
            api_client,
            create_season_object,
            team_setup,
    ):
        team_setup()
        season = create_season_object(2024)

        team_response = api_client.get(f"{self.TEAM_MATCHES_URL}?season={season.year_start}&offset=-1&limit=0")

        assert team_response.status_code == status.HTTP_400_BAD_REQUEST
        assert team_response.data['detail'] == "Invalid pagination params"

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
        assert team_response.data['player_stats'][0]['player_common_name'] == players_list['player1']['common_name']
    
    def test_team_details_not_found(
            self, 
            api_client,
            ):
        team_response = api_client.get(
            f"{self.TEAM_DETAILS_URL}?season=2024"
            )
        assert team_response.status_code == status.HTTP_404_NOT_FOUND

    def test_team_matches_not_found(
            self,
            api_client,
    ):
        team_response = api_client.get(f"{self.TEAM_MATCHES_URL}?season=2024")
        assert team_response.status_code == status.HTTP_404_NOT_FOUND

@pytest.fixture
def team_setup(team_factory):
    def _make(title="Test Team", slug="test-team"):
        return team_factory(title=title, slug=slug)
    return _make