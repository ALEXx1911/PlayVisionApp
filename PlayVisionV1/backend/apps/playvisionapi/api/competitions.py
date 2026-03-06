from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer, OpenApiResponse
from django.db.models import Prefetch
from rest_framework import serializers
from ..models import Competition, Country, Season, TeamCompetitionStats, Match, PlayerCompetitionStats
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..serializer import CompetitionSerializer, TeamCompetitionStatSerializer, \
    PlayerTopScorerSerializer, PlayerTopMediaSerializer , PlayerMostYellowCardsSerializer,\
    PlayerTopGoalkeepersSerializer, CountryCompetitionSerializer, CompetitionMatchesListSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#Return list of competitions grouped by country
@extend_schema(
    operation_id="competition_list",
    description="Return a list of competitions grouped by country.",
    responses={
        200: inline_serializer(
            name='CompetitionListResponse',
            fields={
                'countries': CountryCompetitionSerializer(many=True)
            }
        )
    },
    auth=None,
    tags=["Competitions"]
)
@api_view(["GET"])
def competition_list(request):
    competition_qs = Competition.objects.filter(competition_type = 'league').order_by('title')
    countries_qs = Country.objects.prefetch_related(Prefetch("competition_country",queryset=competition_qs))
    serializer = CountryCompetitionSerializer(countries_qs,many=True)
    return Response({
        "countries" : serializer.data
    })

#Return competition details including top players and last matches by team
@extend_schema(
    operation_id="competition_details",
    description="Return competition details including last matches and top players "
    "(like: top scorers, top media players, most yellow cards, top goalkeepers) by team. "
    "Season parameter is optional, if not provided it will return the current season details.",
    parameters=[
        OpenApiParameter(
            name="ctitle",
            type=str,
            location=OpenApiParameter.PATH,
            description="The slug of the competition to get details for",
            required=True,
            examples=[OpenApiExample("competition-slug", value="la-liga")]
        ),
        OpenApiParameter(
            name="season",
            type=int,
            location=OpenApiParameter.QUERY,
            description="The season to get competition details for (e.g., 2024)",
            required=False,
            examples=[OpenApiExample("season-year", value=2024)]
        )
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name='CompetitionDetailsResponse',
                fields={
                    'competition_data': CompetitionSerializer(),
                    'team_competition_stats': TeamCompetitionStatSerializer(many=True),
                    'top_scorers': PlayerTopScorerSerializer(many=True),
                    'top_media_players': PlayerTopMediaSerializer(many=True),
                    'most_yellow_cards': PlayerMostYellowCardsSerializer(many=True),
                    'top_goalkeepers': PlayerTopGoalkeepersSerializer(many=True),
                }
            ),
            description="Successful retrieval of competition details with team stats and top players"
        ),
        404: OpenApiResponse(
            response=inline_serializer(
                name='CompetitionNotFoundResponse',
                fields={
                    'detail': serializers.CharField()
                }
            ),
            description="Competition not found",
            examples=[
                OpenApiExample(
                    'Competition Not Found',
                    value={"detail": "No Competition matches the given query."},
                    description="The competition with the provided slug does not exist"
                )
            ]
        )
    },
    auth=None,
    tags=["Competitions"]
)
@api_view(["GET"])
def competition_details(request,ctitle):
    season_param = request.query_params.get("season")
    if not season_param:
        #season_param = datetime.now().year
        season_param = 2024
        #return Response({"detail":"Formato no válido"},status=400)
    
    season_obj = Season.objects.filter(year_start=season_param).first()
    competition_qs = get_object_or_404(Competition, slug=ctitle)
    stats_qs = TeamCompetitionStats.objects.filter(competition=competition_qs,season=season_obj).select_related("team")

    team_ids = list(stats_qs.values_list("id",flat=True))
    matches_qs = Match.objects.filter(competition=competition_qs,season=season_obj,status="Finished").filter(
        Q(home_team__id__in=team_ids) | Q(away_team__id__in=team_ids)
    ).select_related("home_team","away_team").order_by("-match_date")
    last_matches_by_team = {team_id: [] for team_id in team_ids}
    remaining  ={team_id: 5 for team_id in team_ids}

    for match in matches_qs:
        if not any(v > 0 for v in remaining.values()):
            break
        home_team_id = match.home_team.id
        away_team_id = match.away_team.id
        
        if remaining.get(home_team_id,0) > 0:
            last_matches_by_team[home_team_id].append(match)
            remaining[home_team_id] -= 1

        if remaining.get(away_team_id,0) > 0:
            last_matches_by_team[away_team_id].append(match)
            remaining[away_team_id] -= 1

    top_goals_player_qs = PlayerCompetitionStats.objects.filter(season = season_obj).order_by("-goals")[:5]
    top_media_player_qs = PlayerCompetitionStats.objects.filter(season = season_obj).order_by("-media")[:5]
    most_yellow_card_qs = PlayerCompetitionStats.objects.filter(season = season_obj).order_by("-yellow_cards")[:5]
    top_goalkeepers_qs = PlayerCompetitionStats.objects.filter(season = season_obj).order_by("-cleansheets")[:5]

    team_competition_stats_serializer = TeamCompetitionStatSerializer(stats_qs,many=True,context={
        "last_matches_by_team": last_matches_by_team
    })
    competition_serializer = CompetitionSerializer(competition_qs)
    top_goals_player_serializer = PlayerTopScorerSerializer(top_goals_player_qs,many=True)
    top_media_player_serializer = PlayerTopMediaSerializer(top_media_player_qs,many=True)
    most_yellow_card_serializer = PlayerMostYellowCardsSerializer(most_yellow_card_qs,many=True)
    top_goalkeepers_serializer = PlayerTopGoalkeepersSerializer(top_goalkeepers_qs,many=True)
    
    return Response({
        "competition_data": competition_serializer.data,
        "team_competition_stats": team_competition_stats_serializer.data,
        "top_scorers" : top_goals_player_serializer.data,
        "top_media_players" : top_media_player_serializer.data,
        "most_yellow_cards" : most_yellow_card_serializer.data,
        "top_goalkeepers" : top_goalkeepers_serializer.data,
    })

#Return competition matches with pagination
@extend_schema(
    operation_id="competition_matches",
    description="Return paginated  matches of a specific competition for a season.",
    parameters=[
        OpenApiParameter(
            name="ctitle",
            type=str,
            location=OpenApiParameter.PATH,
            description="The slug of the competition",
            required=True,
            examples=[OpenApiExample("competition-slug", value="la-liga")]
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
        OpenApiParameter(
            name="season",
            type=int,
            location=OpenApiParameter.QUERY,
            description="Season year",
            required=False,
        )
    ],
    responses={
        200: OpenApiResponse(
            response=inline_serializer(
                name='CompetitionMatchesResponse',
                fields={
                    'matches': CompetitionMatchesListSerializer(many=True),
                    'total': serializers.IntegerField(),
                    'offset': serializers.IntegerField(),
                    'limit': serializers.IntegerField(),
                    'has_more': serializers.BooleanField(),
                }
            ),
            description="Paginated list of competition matches"
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
                name='CompetitionMatchesNotFoundResponse',
                fields={
                    'detail': serializers.CharField()
                }
            ),
            description="Competition not found",
            examples=[
                OpenApiExample(
                    'Competition Not Found',
                    value={"detail": "No Competition matches the given query."},
                    description="The competition with the provided slug does not exist"
                )
            ]
        )
    },
    auth=None,
    tags=["Competitions"],
)
@api_view(["GET"])
def competition_matches(request,ctitle):
    season_param = request.query_params.get("season")
    offset_param = request.query_params.get("offset",0)
    limit_param = request.query_params.get("limit",20)
    
    if not season_param:
        #season_param = datetime.now().year
        season_param = 2024
        #return Response({"detail":"Formato no válido"},status=400)
    
    try:
        offset = int(offset_param)
        limit = int(limit_param)
    except (TypeError, ValueError):
        return Response({"detail": "Invalid pagination params"}, status=400)

    if offset < 0 or limit <= 0:
        return Response({"detail": "Invalid pagination params"}, status=400)
    
    season_obj = Season.objects.filter(year_start=season_param).first()
    competition_qs = get_object_or_404(Competition, slug=ctitle)
    matches_qs = Match.objects.filter(
        season=season_obj,competition=competition_qs
        ).order_by("description")
    
    total_matches = matches_qs.count()
    paginated_matches = matches_qs[offset:offset + limit]


    matches_cmpt_serializer = CompetitionMatchesListSerializer(paginated_matches,many=True)
    return Response({
        "matches": matches_cmpt_serializer.data,
        "total": total_matches,
        "offset": offset,
        "limit": limit,
        "has_more": offset + limit < total_matches,
    })