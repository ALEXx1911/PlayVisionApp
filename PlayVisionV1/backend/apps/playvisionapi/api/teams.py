from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, inline_serializer
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import serializers
from ..models import Team, Season, PlayerSeasonStats, TeamInsights, Match
from ..serializer import TeamSerializer, TeamInsightsSerializer ,PlayerSeasonStatsListWithCountryFlagSerializer, MatchSerializer, PlayerLineupSerializer
from ..utils.utils import get_last_matches_results, get_team_lineup , FORMATION_POSITIONS

#Return detailed information about a specific team
@extend_schema(
    description="Return detailed information about a specific team, " \
    "like its insights, player stats for a specific season, lineup and last five results.",
    parameters=[
        OpenApiParameter(
            name="title",
            type=str,
            location=OpenApiParameter.PATH,
            description="The slug of the team to get details for",
            required=True,
            examples=[OpenApiExample("team-title", value="real-madrid")]
        ),
        OpenApiParameter(
            name="season",
            type=str,
            location=OpenApiParameter.QUERY,
            description="The season to get team details for",
            required=False,
        )
    ],
    responses={
        200: inline_serializer(
            name='TeamDetailsResponse',
            fields={
                'team': TeamSerializer(),
                'insights': TeamInsightsSerializer(many=True),
                'player_stats': PlayerSeasonStatsListWithCountryFlagSerializer(many=True),
                'team_lineup': PlayerLineupSerializer(many=True),
                'last_five_results': ["W", "D", "L", "W", "W"]
            }
        ),
        404: OpenApiResponse(
            response=inline_serializer(
                name='TeamNotFoundResponse',
                fields={
                    'detail': serializers.CharField()
                }
            ),
            description="Team not found",
            examples=[
                OpenApiExample(
                    'Error Team Not Found',
                    value={"detail": "No Team matches the given query."},
                    description="Response when the specified team is not found in the database."
                )
            ]
        )
    },
    auth=None,
    tags=["Teams"]
)
@api_view(["GET"])
def team_details(request, title):
    season_param = request.query_params.get("season")
    last_five_results = []
    if not season_param:
        #season_param = datetime.now().year
        season_param = 2024
        #return Response({"detail":"Formato no válido"},status=400)
    
    season_obj = Season.objects.filter(year_start=season_param).first()
    team_obj = get_object_or_404(Team, slug=title)
    player_season_stats_obj = PlayerSeasonStats.objects.filter(team = team_obj, season = season_obj)
    team_insights_obj = TeamInsights.objects.filter(team=team_obj)
    last_five_results_obj = Match.objects.filter(Q(away_team = team_obj) | Q(home_team = team_obj),season = season_obj).order_by("-match_date")[:5]

    last_five_results = get_last_matches_results(last_five_results_obj,team_obj)

    team_lineup = get_team_lineup(FORMATION_POSITIONS["4-3-3"], season_param, team_obj)
    top_player_lineup_serializer = PlayerLineupSerializer(team_lineup, many=True)

    team_serializer = TeamSerializer(team_obj)
    team_insights_serializer = TeamInsightsSerializer(team_insights_obj,many=True)
    player_season_serializer = PlayerSeasonStatsListWithCountryFlagSerializer(player_season_stats_obj,many=True)
    return Response({
        "team" : team_serializer.data,
        "insights" : team_insights_serializer.data,
        "player_stats" : player_season_serializer.data,
        "team_lineup": top_player_lineup_serializer.data,
        "last_five_results": last_five_results
    })


@extend_schema(
    description="Return paginated matches of a specific team for a season.",
    parameters=[
        OpenApiParameter(
            name="title",
            type=str,
            location=OpenApiParameter.PATH,
            description="The slug of the team to get matches for",
            required=True,
            examples=[OpenApiExample("team-title", value="real-madrid")]
        ),
        OpenApiParameter(
            name="season",
            type=str,
            location=OpenApiParameter.QUERY,
            description="The season to get team matches for",
            required=False,
        ),
        OpenApiParameter(
            name="offset",
            type=int,
            location=OpenApiParameter.QUERY,
            description="Pagination offset (starts in 0)",
            required=False,
            examples=[OpenApiExample("offset-example", value=0)]
        ),
        OpenApiParameter(
            name="limit",
            type=int,
            location=OpenApiParameter.QUERY,
            description="Maximum matches to return per request",
            required=False,
            examples=[OpenApiExample("limit-example", value=10)]
        ),
    ],
    responses={
        200: inline_serializer(
            name='TeamMatchesResponse',
            fields={
                'matches': MatchSerializer(many=True),
                'total': serializers.IntegerField(),
                'offset': serializers.IntegerField(),
                'limit': serializers.IntegerField(),
                'has_more': serializers.BooleanField(),
            }
        ),
        400: OpenApiResponse(
            response=inline_serializer(
                name='InvalidPaginationResponse',
                fields={
                    'detail': serializers.CharField()
                }
            ),
            description="Invalid pagination parameters",
            examples=[
                OpenApiExample(
                    'Error Invalid Pagination',
                    value={"detail": "Invalid pagination params"},
                    description="Response when offset or limit are invalid."
                )
            ]
        ),
        404: OpenApiResponse(
            response=inline_serializer(
                name='TeamMatchesNotFoundResponse',
                fields={
                    'detail': serializers.CharField()
                }
            ),
            description="Team not found",
            examples=[
                OpenApiExample(
                    'Error Team Not Found',
                    value={"detail": "No Team matches the given query."},
                    description="Response when the specified team is not found in the database."
                )
            ]
        )
    },
    auth=None,
    tags=["Teams"]
)
@api_view(["GET"])
def team_matches(request, title):
    season_param = request.query_params.get("season")
    offset_param = request.query_params.get("offset", 0)
    limit_param = request.query_params.get("limit", 10)

    if not season_param:
        season_param = 2024

    try:
        offset = int(offset_param)
        limit = int(limit_param)
    except (TypeError, ValueError):
        return Response({"detail": "Invalid pagination params"}, status=400)

    if offset < 0 or limit <= 0:
        return Response({"detail": "Invalid pagination params"}, status=400)

    season_obj = Season.objects.filter(year_start=season_param).first()
    team_obj = get_object_or_404(Team, slug=title)

    team_matches_qs = Match.objects.filter(
        Q(away_team=team_obj) | Q(home_team=team_obj),
        season=season_obj,
    ).order_by("-match_date")

    total_matches = team_matches_qs.count()
    paginated_matches = team_matches_qs[offset:offset + limit]

    team_matches_serializer = MatchSerializer(paginated_matches, many=True)

    return Response({
        "matches": team_matches_serializer.data,
        "total": total_matches,
        "offset": offset,
        "limit": limit,
        "has_more": offset + limit < total_matches,
    })
