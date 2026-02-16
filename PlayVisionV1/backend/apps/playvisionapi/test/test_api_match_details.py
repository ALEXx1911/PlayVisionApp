import pytest
from django.urls import reverse
from rest_framework import status
from apps.playvisionapi.test.factories import match_factory, team_factory, competition_factory, season_factory, player_factory , match_stats_factory, match_event_factory


@pytest.mark.django_db
class TestMatchDetailsAPI:
    URL = reverse('match-details', kwargs={'matchid': 1})
    def test_match_details_success(
            self, 
            api_client, 
            match_setup, 
            ):
        _, _, match = match_setup()

        response = api_client.get(self.URL)

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) >= {'data', 'match_stats', 'match_events'}

    def test_match_details_include_stats(
            self, 
            api_client, 
            match_setup
            ):
        _, _, match = match_setup()

        response = api_client.get(self.URL)

        assert response.status_code == status.HTTP_200_OK
        assert 'match_stats' in response.data
        assert len(response.data['match_stats']) >= 1
        assert isinstance(response.data['match_stats'][0]['home_data'], int)

    def test_match_details_include_events(
            self, 
            api_client, 
            match_setup
            ):
        _, _, match = match_setup()

        response = api_client.get(self.URL)

        assert response.status_code == status.HTTP_200_OK
        assert 'match_events' in response.data
        assert len(response.data['match_events']) >= 1
        assert response.data['match_events'][0]['event_type'] == "Goal"

    def test_match_not_found(
            self, 
            api_client
            ):
        url = reverse('match-details', kwargs={'matchid': 9999})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        

@pytest.fixture
def match_setup(player_factory, season_factory,competition_factory,team_factory, match_factory, match_stats_factory, match_event_factory):
    def _make(player_name="Test Player",player_slug="test-player", season_year=2024 , home_goals_data=2, away_goals_data=1,status_data="FT",event_type_data="Goal"):
        default_team1 = team_factory(title="Test Team", slug="test-team")
        default_team2 = team_factory(title="Test Team 2", slug="test-team-2")
        default_season = season_factory(year_start=season_year, year_end=season_year + 1)
        default_competition = competition_factory(title="Test Competition", slug="test-competition")
        default_match = match_factory(id=1,home_goals=home_goals_data, away_goals=away_goals_data,status=status_data, home_team=default_team1, away_team=default_team2, competition=default_competition, season=default_season)
        
        default_player = player_factory(pname=player_name, slug=player_slug)
        
        match_stats_factory(match=default_match)
        match_event_factory(match=default_match, event_type=event_type_data, player=default_player, minute=23)
        return default_season, default_player, default_match
    
    return _make

@pytest.fixture
def empty_match_setup(player_factory, season_factory,competition_factory,team_factory, match_factory):
    def _make(player_name="Test Player",player_slug="test-player", season_year=2024 , home_goals_data=2, away_goals_data=1,status_data="FT"):
        default_team1 = team_factory(title="Test Team", slug="test-team")
        default_team2 = team_factory(title="Test Team 2", slug="test-team-2")
        default_season = season_factory(year_start=season_year, year_end=season_year + 1)
        default_competition = competition_factory(title="Test Competition", slug="test-competition")
        default_match = match_factory(id=2,home_goals=home_goals_data, away_goals=away_goals_data,status=status_data, home_team=default_team1, away_team=default_team2, competition=default_competition, season=default_season)
        
        default_player = player_factory(pname=player_name, slug=player_slug)
        
        return default_season, default_player, default_match
    
    return _make