import pytest
from django.urls import reverse
from rest_framework import status
from apps.playvisionapi.test.factories import competition_factory , season_factory , player_factory , player_competition_stats_factory

@pytest.mark.django_db
class TestCompetitionAPI:
    URL = reverse('competition-details', kwargs={'ctitle': 'la-liga'})
    def test_competition_success(
            self, 
            api_client,
            competition_setup,
        ):
        competition, season = competition_setup()
        response = api_client.get(self.URL)

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) >= {
            'competition', 
            'top_scorers', 
            'top_media_players',
            'most_yellow_cards',
            'top_goalkeepers'
        }

    def test_competition_include_top_scorers(
            self,
            competition_setup, 
            api_client, 
            player_factory, 
            player_competition_stats_factory
        ):
        competition, season = competition_setup()
        player = player_factory(pname="Leo")
        player_competition_stats_factory(player=player, competition=competition, season=season, goals=10)
        response = api_client.get(f"{self.URL}?season={season.year_start}")

        assert response.status_code == status.HTTP_200_OK
        assert 'top_scorers' in response.data
        assert len(response.data['top_scorers']) >= 1
        assert response.data['top_scorers'][0]['player']['pname'] == "Leo" and response.data['top_scorers'][0]['goals'] == 10

    def test_competition_include_top_media_players(
            self, 
            api_client,
            competition_setup, 
            player_factory, 
            player_competition_stats_factory
        ):
        competition, season = competition_setup()
        player1 = player_factory(pname="Paul")
        player2 = player_factory(pname="Marco Polo")
        player_competition_stats_factory(player=player1, competition=competition, season=season, media=9.0)
        player_competition_stats_factory(player=player2, competition=competition, season=season, media=9.5)

        response = api_client.get(f"{self.URL}?season={season.year_start}")
        print(response.status_code)

        assert response.status_code == status.HTTP_200_OK
        assert 'top_media_players' in response.data
        assert len(response.data['top_media_players']) >= 1
        assert response.data['top_media_players'][0]['media'] == '9.50'

    def test_competition_include_most_yellow_cards(
            self, 
            api_client, 
            competition_setup, 
            player_factory, 
            player_competition_stats_factory
        ):
        competition, season = competition_setup()
        player1 = player_factory(pname="Carlitos")
        player2 = player_factory(pname="Rafael")
        player_competition_stats_factory(player=player1, competition=competition, season=season, yellow_cards=4)
        player_competition_stats_factory(player=player2, competition=competition, season=season, yellow_cards=8)

        response = api_client.get(f"{self.URL}?season={season.year_start}")

        assert response.status_code == status.HTTP_200_OK
        assert 'most_yellow_cards' in response.data
        assert len(response.data['most_yellow_cards']) >= 1
        assert response.data['most_yellow_cards'][0]['yellow_cards'] == 8

    def test_competition_include_top_goalkeepers(
            self, 
            api_client, 
            competition_setup, 
            player_factory, 
            player_competition_stats_factory
            ):
        competition, season = competition_setup()
        player1 = player_factory(pname="Tek")
        player2 = player_factory(pname="Andre")
        player_competition_stats_factory(player=player1, competition=competition, season=season, cleansheets=6)
        player_competition_stats_factory(player=player2, competition=competition, season=season, cleansheets=10)

        response = api_client.get(f"{self.URL}?season={season.year_start}")

        assert response.status_code == status.HTTP_200_OK
        assert 'top_goalkeepers' in response.data
        assert len(response.data['top_goalkeepers']) >= 1
        assert response.data['top_goalkeepers'][0]['cleansheets'] == 10

    def test_competition_not_found(self, api_client):
        url = reverse('competition-details', kwargs={'ctitle': 'non-existent-competition'})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.fixture
def competition_setup(competition_factory, create_season_object):
    def _make(title="La Liga", slug="la-liga",season_year=2024):
        default_competition = competition_factory(title=title, slug=slug)
        default_season = create_season_object(season_year)
        return default_competition , default_season
    return _make
