import pytest
from django.urls import reverse
from rest_framework import status
from apps.playvisionapi.test.factories import team_factory, competition_factory, player_factory


@pytest.mark.django_db
class TestSearchPageAPI:
    URL = reverse('search-page')
    def test_search_page_success(
            self, 
            api_client, 
            player_factory, 
            team_factory, 
            competition_factory,
        ):
        player_factory(pname="Player Example", slug="player-example")
        team_factory(title="Team Example", slug="team-example")
        competition_factory(title="Competition Example", slug="competition-example")

        response = api_client.get(
            f"{self.URL}?searchTerm=Example"
            )
        results = response.data["search_results"]

        assert response.status_code == status.HTTP_200_OK        
        fields = [r["field"] for r in results]
        assert fields == ["Players Results", "Teams Results", "Competitions Results"]

    def test_search_page_no_results(
            self, 
            api_client,
            ):
        response = api_client.get(
            f"{self.URL}?searchTerm=NonExistentTerm"
            )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["search_results"] == []

    def test_search_page_case_insensitive(
            self, 
            api_client, 
            player_factory,
            ):
        player_1 = player_factory(pname="Example player", slug="example-player")
        player_factory(pname="EXAMPLE soccer player", slug="example-soccer-player")

        response = api_client.get(
            f"{self.URL}?searchTerm=example"
            )
        results = response.data["search_results"]

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["field"] == "Players Results"
        assert len(results[0]["players_data"])  > 1
        assert results[0]["players_data"][0]["pname"] == player_1.pname

    def test_search_page_partial_match(
            self, 
            api_client, 
            team_factory,
        ):
        test_team = team_factory(title="Manchester United", slug="manchester-united")

        response = api_client.get(
            f"{self.URL}?searchTerm=Manchester"
            )
        results = response.data["search_results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["field"] == "Teams Results"
        assert results[0]["teams_data"][0]["title"] == test_team.title
    
    def test_search_page_empty_term(
            self, 
            api_client,
            ):
        response = api_client.get(
            f"{self.URL}?searchTerm="
            )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "The search term cannot be empty."

    def test_search_page_missing_term(
            self,
            api_client,
            ):
        response = api_client.get(self.URL)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "The search term cannot be empty."
