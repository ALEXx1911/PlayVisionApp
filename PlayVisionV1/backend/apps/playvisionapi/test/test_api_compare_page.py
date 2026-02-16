import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestComparePageAPI:
    URL = reverse('compare-players')
    def test_compare_page_success(
            self,
            api_client, 
            create_players_with_stats,
        ):      
        players_list =  create_players_with_stats()
        response = api_client.get(
            f"{self.URL}?player1={players_list['player1']['slug']}"
            f"&player2={players_list['player2']['slug']}"
        )
        assert response.status_code == status.HTTP_200_OK
        assert set(response.data.keys()) >= {
            'player1_data', 
            'player1_season_stats', 
            'player2_data', 
            'player2_season_stats'
        }

    def test_compare_page_player_not_found(
            self, 
            api_client
            ):
        response = api_client.get(
            f"{self.URL}?player1=non-existent-player"
            f"&player2=another-non-existent-player"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "No Player matches the given query."

    def test_compare_page_missing_both_parameters(
            self, 
            api_client,
        ):
        response = api_client.get(f"{self.URL}")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "The names of both players are required."

    def test_compare_page_missing_first_parameter(
            self, 
            api_client, 
            create_players_with_stats, 
        ):
        players_list =  create_players_with_stats()
        response = api_client.get(
            f"{self.URL}?player2={players_list['player2']['slug']}"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "The names of both players are required."
    
    def test_compare_page_missing_second_parameter(
            self, 
            api_client, 
            create_players_with_stats,
        ):
        players_list =  create_players_with_stats()
        response = api_client.get(
            f"{self.URL}?player1={players_list['player1']['slug']}"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "The names of both players are required."
    
    def test_compare_page_same_players(
            self, 
            api_client, 
            create_players_with_stats,
        ):
        players_list =  create_players_with_stats()
        response = api_client.get(
            f"{self.URL}?player1={players_list['player1']['slug']}"
            f"&player2={players_list['player1']['slug']}"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "The names of the two players cannot be the same."
