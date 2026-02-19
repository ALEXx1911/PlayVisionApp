from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse , OpenApiParameter, OpenApiExample, inline_serializer
from ..models import Player, Team, Competition
from ..serializer import PlayerSerializer, TeamSerializer, CompetitionSerializer

#Return search results for players, teams, and competitions
@extend_schema(
    description="Return search results for players, teams, and competitions based on the provided search term." \
    "The search will look for exact matches first and then partial matches if no exact matches are found.",
    parameters=[
        OpenApiParameter(
            name="searchTerm",
            type=str,
            location=OpenApiParameter.QUERY,
            description="The term to search for in players, teams, and competitions.",
            required=True,
            examples=[OpenApiExample("search-term-example", value="Lamine")]
        )
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name='SearchResultsResponse',
                fields={
                    'search_results': inline_serializer(
                        name='SearchResults',
                        fields={
                            'field': serializers.CharField(),
                            'players_data': PlayerSerializer(many=True),
                            'teams_data': TeamSerializer(many=True),
                            'competitions_data': CompetitionSerializer(many=True)
                        }
                    )
                }
            ),
            description="Successful search results for players, teams, and competitions",
            examples=[
                OpenApiExample(
                'Successful Search',
                value={
                    "search_results": [
                        {
                            "field": "Players Results",
                            "players_data": [
                                {
                                    "id": 1,
                                    "pname": "Lamine Yamal",
                                    "slug": "lamine-yamal",
                                    "position": "Attacking Midfielder",
                                    "age": 17,
                                }
                            ],
                        },
                        {
                            "field": "Teams Results",
                            "teams_data": [
                                {
                                    "id": 1,
                                    "title": "Barcelona",
                                    "slug": "barcelona",
                                    "country": "Spain",
                                }
                            ],
                        },
                        {
                            "field": "Competitions Results",
                            "competitions_data": [
                                {
                                    "id": 1,
                                    "title": "La Liga",
                                    "slug": "la-liga",
                                    "country": "Spain",
                                }
                            ],
                        },
                    ]
            },
            description="Successful search with results for players, teams, and competitions"
            )
            ]
        ),
        400: OpenApiResponse(
            response=inline_serializer(
                name='SearchErrorResponse',
                fields={
                    'detail': serializers.CharField()
                }
            ),
            description="Bad request due to missing or empty search term",
            examples=[
                OpenApiExample(
                    'Empty Search Term',
                    value={"detail":"The search term cannot be empty."},
                    status_codes=[400]
                )
            ]
        )
    },
    auth=None,
    tags=["Search and Compare"]
)
@api_view (["GET"])
def search_page(request):
    
    if not request.query_params.get("searchTerm"):
        return Response({"detail":"The search term cannot be empty."},status=400)
    
    searchParam = request.query_params.get("searchTerm").strip()
    

    if searchParam.strip() == "":
        return Response({"detail":"The search term cannot be empty."},status=400)
    
    player_obj = Player.objects.filter(pname=searchParam)
    team_obj = Team.objects.filter(title=searchParam)
    competition_obj = Competition.objects.filter(title=searchParam)

    if not player_obj.exists():
        player_obj = Player.objects.filter(pname__icontains=searchParam)
    if not team_obj.exists():
        team_obj = Team.objects.filter(title__icontains=searchParam)
    if not competition_obj.exists():
        competition_obj = Competition.objects.filter(title__icontains=searchParam)

    player_serializer = PlayerSerializer(player_obj,many=True)
    team_serializer = TeamSerializer(team_obj,many=True)
    competition_serializer = CompetitionSerializer(competition_obj,many=True)
    search_results = []
    if player_serializer.data:
        search_results.append(
            {
                "field":"Players Results",
                "players_data": player_serializer.data
            }
        )
    if team_serializer.data:
        search_results.append(
            {
                "field":"Teams Results",
                "teams_data": team_serializer.data
            },
        )
    if competition_serializer.data:
        search_results.append(
            {
                "field":"Competitions Results",
                "competitions_data": competition_serializer.data
            }
        )

    return Response({
        "search_results" : search_results,
    })