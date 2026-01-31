import pytest
from django.urls import reverse
from rest_framework import status
from apps.playvisionapi.test.factories import team_factory, competition_factory, player_factory


@pytest.mark.django_db
class TestSearchPageAPI:
    def test_search_page_success(self, api_client, player_factory, team_factory, competition_factory):
        player_factory(pname="Player Example", slug="player-example")
        team_factory(title="Team Example", slug="team-example")
        competition_factory(title="Competition Example", slug="competition-example")

        url = reverse('search-page')
        response = api_client.get(f"{url}?searchTerm=Example")
        results = response.data["search_results"]

        assert response.status_code == status.HTTP_200_OK        
        fields = [r["field"] for r in results]
        assert fields == ["Players Results", "Teams Results", "Competitions Results"]

    def test_search_page_no_results(self, api_client):
        url = reverse('search-page')
        response = api_client.get(f"{url}?searchTerm=NonExistentTerm")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["search_results"] == []

    def test_search_page_case_insensitive(self, api_client, player_factory):
        player_factory(pname="Example player", slug="example-player")
        player_factory(pname="EXAMPLE soccer player", slug="example-soccer-player")

        url = reverse('search-page')
        response = api_client.get(f"{url}?searchTerm=example")
        results = response.data["search_results"]
        print(results)

        assert response.status_code == status.HTTP_200_OK
        assert results[0]["field"] == "Players Results"
        assert len(results[0]["players_data"])  > 1
        assert results[0]["players_data"][0]["pname"] == "Example player"

    def test_search_page_partial_match(self, api_client, team_factory):
        team_factory(title="Manchester United", slug="manchester-united")

        url = reverse('search-page')
        response = api_client.get(f"{url}?searchTerm=Manchester")
        results = response.data["search_results"]

        assert response.status_code == status.HTTP_200_OK
        assert len(results) == 1
        assert results[0]["field"] == "Teams Results"
        assert results[0]["teams_data"][0]["title"] == "Manchester United"
    
    def test_search_page_empty_term(self, api_client):
        url = reverse('search-page')
        response = api_client.get(f"{url}?searchTerm=")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "The search term cannot be empty."

    def test_search_page_missing_term(self, api_client):
        url = reverse('search-page')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "The search term cannot be empty."