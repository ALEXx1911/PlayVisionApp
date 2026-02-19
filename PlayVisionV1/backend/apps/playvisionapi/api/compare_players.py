from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer, OpenApiResponse
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from ..models import Player, Season , PlayerSeasonStats
from ..serializer import PlayerSerializer, PlayerSeasonStatSerializerBasic

#Return comparison data for two players
@extend_schema(
    description="Return comparison data for two players based on their season stats. " \
    "The season parameter is optional, if not provided it will compare the players based on the current season stats.",
    parameters=[
        OpenApiParameter(
            name="player1",
            type=str,
            location=OpenApiParameter.QUERY,
            description="The slug of the first player to compare (e.g., lamine-yamal).",
            required=True,
            examples=[OpenApiExample("player1-slug", value="lamine-yamal")]
        ),
        OpenApiParameter(
            name="player2",
            type=str,
            location=OpenApiParameter.QUERY,
            description="The slug of the second player to compare (e.g., pedri-gonzalez).",
            required=True,
            examples=[OpenApiExample("player2-slug", value="pedri-gonzalez")]
        ),
        OpenApiParameter(
            name="season",
            type=int,
            location=OpenApiParameter.QUERY,
            description="The season to compare the players for (e.g., 2024). If not provided, it will compare based on the current season stats.",
            required=False,
            examples=[OpenApiExample("season-year", value=2024)]
        )
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name='ComparePlayersResponse',
                fields={
                    'player1_data': PlayerSerializer(),
                    'player1_season_stats': PlayerSeasonStatSerializerBasic(),
                    'player2_data': PlayerSerializer(),
                    'player2_season_stats': PlayerSeasonStatSerializerBasic()
                }
            ),
            description="Successful comparison of two players",
            examples=[
                OpenApiExample(
                    'Successful Comparison',
                    value={
                        "player1_data": {
                            "pname": "Lamine",
                            "lastname": "Yamal",
                            "common_name": "Lamine Yamal",
                            "position": "Forward"
                        },
                        "player1_season_stats": {
                            "goals": 15,
                            "assists": 10,
                            "matches_played": 30
                        },
                        "player2_data": {
                            "pname": "Pedri",
                            "lastname": "González",
                            "common_name": "Pedri",
                            "position": "Midfielder"
                        },
                        "player2_season_stats": {
                            "goals": 5,
                            "assists": 18,
                            "matches_played": 28
                        }
                    },
                    description="Example of successful player comparison"
                )
            ]
        ),
        400: OpenApiResponse(
            response=inline_serializer(
                name='ComparePlayersErrorResponse',
                fields={
                    'detail': serializers.CharField()
                }
            ),
            description="Bad request - validation errors",
            examples=[
                OpenApiExample(
                    'Missing Player Parameters',
                    value={"detail": "The names of both players are required."},
                    description="One or both player slugs are missing"
                ),
                OpenApiExample(
                    'Same Player',
                    value={"detail": "The names of the two players cannot be the same."},
                    description="Both player slugs are identical"
                )
            ]
        ),
        404: OpenApiResponse(
            response=inline_serializer(
                name='ComparePlayersPlayerNotFoundResponse',
                fields={
                    'detail': serializers.CharField()
                }
            ),
            description="Player or season not found",
            examples=[
                OpenApiExample(
                    'Player Not Found',
                    value={"detail": "No Player matches the given query."},
                    description="One or both players do not exist in the database"
                )
            ]
        )
    },
    auth=None,
    tags=["Search and Compare"]
)
@api_view (["GET"])
def compare_players(request):
    season_param = request.query_params.get("season")
    player1_slug = request.query_params.get("player1").strip().lower() if request.query_params.get("player1") else ""
    player2_slug = request.query_params.get("player2").strip().lower() if request.query_params.get("player2") else ""

    if not season_param:
        #season_param = datetime.now().year
        season_param = 2024
    
    season_obj = Season.objects.filter(year_start = season_param).first()

    if not player1_slug or not player2_slug:
        return Response({"detail":"The names of both players are required."}, status=400)

    if player1_slug == player2_slug:
        return Response({"detail":"The names of the two players cannot be the same."},status=400)

    player1_qs = get_object_or_404(Player, slug = player1_slug.strip().lower())
    player1_season_stats_qs = get_object_or_404(PlayerSeasonStats, player = player1_qs,season = season_obj)
    player2_qs = get_object_or_404(Player, slug = player2_slug.strip().lower())
    player2_season_stats_qs = get_object_or_404(PlayerSeasonStats, player = player2_qs,season = season_obj)

    player_serializer = PlayerSerializer(player1_qs,many=False)
    player_season_stat_serializer = PlayerSeasonStatSerializerBasic(player1_season_stats_qs,many =False)
    player2_serializer = PlayerSerializer(player2_qs,many=False)
    player2_season_stat_serializer = PlayerSeasonStatSerializerBasic(player2_season_stats_qs,many =False)

    return Response({
        "player1_data" : player_serializer.data,
        "player1_season_stats" : player_season_stat_serializer.data,
        "player2_data" : player2_serializer.data,
        "player2_season_stats" : player2_season_stat_serializer.data
    })