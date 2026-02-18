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
        competition_setup()
        response = api_client.get(self.URL)

        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) >= {
            'competition_data',
            'team_competition_stats',
            'top_scorers', 
            'top_media_players',
            'most_yellow_cards',
            'top_goalkeepers'
        }

    def test_competition_include_top_scorers(
            self,
            api_client,
            create_players_with_competition_stats
        ):
        players_data = create_players_with_competition_stats(
            player1_name="Leo",
            player1_slug="leo",)
        season = 2024

        response = api_client.get(f"{self.URL}?season={season}")

        assert response.status_code == status.HTTP_200_OK
        assert 'top_scorers' in response.data
        assert len(response.data['top_scorers']) >= 1
        assert response.data['top_scorers'][0]['player']['pname'] == players_data['player1']['pname']

    def test_competition_include_top_media_players(
            self, 
            api_client,
            create_players_with_competition_stats
        ):
        season = 2024
        players_list = create_players_with_competition_stats(
            player1_name="Cristiano",
            player1_slug="cristiano",
            player2_name="Neymar",
            player2_slug="neymar",
        )

        response = api_client.get(f"{self.URL}?season={season}")

        assert response.status_code == status.HTTP_200_OK
        assert 'top_media_players' in response.data
        assert len(response.data['top_media_players']) >= 1
        assert float(response.data['top_media_players'][0]['media']) == float(players_list['player1']['competition_stats'].media)

    def test_competition_include_most_yellow_cards(
            self, 
            api_client,
            create_players_with_competition_stats
        ):
        season = 2024
        players_data = create_players_with_competition_stats(
            player1_name="Sergio",
            player1_slug="sergio",
            player2_name="Carlos",
            player2_slug="carlos",
        )

        response = api_client.get(f"{self.URL}?season={season}")

        assert response.status_code == status.HTTP_200_OK
        assert 'most_yellow_cards' in response.data
        assert len(response.data['most_yellow_cards']) >= 1
        assert response.data['most_yellow_cards'][0]['yellow_cards'] == players_data['player1']['competition_stats'].yellow_cards

    def test_competition_include_top_goalkeepers(
            self, 
            api_client, 
            competition_setup,
            create_players_with_competition_stats
            ):
        season = 2024
        players_list = create_players_with_competition_stats(
            player1_name="Manuel",
            player1_slug="manuel",
            player2_name="Jan",
            player2_slug="jan",
        )

        response = api_client.get(f"{self.URL}?season={season}")

        assert response.status_code == status.HTTP_200_OK
        assert 'top_goalkeepers' in response.data
        assert len(response.data['top_goalkeepers']) >= 1
        assert response.data['top_goalkeepers'][0]['cleansheets'] == players_list['player1']['competition_stats'].cleansheets

    def test_competition_not_found(self, api_client):
        url = reverse('competition-details', kwargs={'ctitle': 'non-existent-competition'})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.fixture
def create_players_with_competition_stats(
    player_factory,
    competition_setup,
    player_competition_stats_factory
):
    def _make(
            player1_name="Player One", 
            player1_slug="player-one",
            player2_name="Player Two", 
            player2_slug="player-two",
            season_year=2024
        ):
        competition = competition_setup()
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

        player1_competition_stats = player_competition_stats_factory(
            player=player1,
            competition=competition,
            season__year_start=season_year
        )
        
        player2_competition_stats = player_competition_stats_factory(
            player=player2,
            competition=competition, 
            season__year_start=season_year
        )
        players_results = {
            "player1": {
                "pname": player1.pname,
                "slug": player1.slug,
                "competition_stats": player1_competition_stats
            },
            "player2": {
                "pname": player2.pname,
                "slug": player2.slug,
                "competition_stats": player2_competition_stats
            }
        }
        return players_results
    return _make