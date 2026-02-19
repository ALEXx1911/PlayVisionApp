from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, inline_serializer
from django.shortcuts import get_object_or_404
from ..models import Player, Season, PlayerSeasonStats, PlayerCompetitionStats
from ..serializer import PlayerSerializer, PlayerSeasonStatsSerializer, PlayerCompetitionStatsSerializer

#Return detailed information about a specific player
@extend_schema(
    description="Return detailed information about a specific player" \
    " including season stats and competition stats. " \
    "Season parameter is optional, if not provided it will return the current season stats.",
    parameters=[
        OpenApiParameter(
            name="pname",
            type=str,
            location=OpenApiParameter.PATH,
            description="The slug of the player to get details for",
            required=True,
            examples=[OpenApiExample("player-slug", value="lamine-yamal")]
        ),
        OpenApiParameter(
            name="season",
            type=int,
            location=OpenApiParameter.QUERY,
            description="The season to get player stats for (e.g., 2024)",
            required=False,
            examples=[OpenApiExample("season-year", value=2024)]
        )
    ],
    responses={
        200: inline_serializer(
            name='PlayerDetailsResponse',
            fields={
                'player_data': PlayerSerializer(),
                'season_stats': PlayerSeasonStatsSerializer(many=True),
                'competition_stats': PlayerCompetitionStatsSerializer(many=True)
            }
        ),
        404: OpenApiResponse(
            response=inline_serializer(
                name='PlayerNotFoundResponse',
                fields={
                    'detail': serializers.CharField()
                }
            ),
            description="Player not found with the provided slug",
            examples = [
                OpenApiExample(
                    'Player Not Found',
                    value={"detail":"No Player matches the given query."},
                    description="Player not found with the provided slug"
                )
            ]
        )
    },
    auth=None,
    tags=["Players"]
)
@api_view(["GET"])
def player_details(request,pname):
    season_param = request.query_params.get("season")
    if not season_param:
        #season_param = datetime.now().year
        season_param = 2024
        #return Response({"detail":"Formato no válido"},status=400)

    season_obj = Season.objects.filter(year_start = season_param).first()
    player_qs = get_object_or_404(Player, slug = pname)
    player_season_stats_qs = PlayerSeasonStats.objects.filter(player = player_qs,season = season_obj)
    player_competition_stats_qs = PlayerCompetitionStats.objects.filter(player = player_qs, season = season_obj)
    
    player_serializer = PlayerSerializer(player_qs,many=False)
    player_season_stat_serializer = PlayerSeasonStatsSerializer(player_season_stats_qs,many =True)
    player_competition_stats_serializer = PlayerCompetitionStatsSerializer(player_competition_stats_qs,many = True)
    return Response({
        "player_data" : player_serializer.data,
        "season_stats" : player_season_stat_serializer.data,
        "competition_stats" : player_competition_stats_serializer.data
    })