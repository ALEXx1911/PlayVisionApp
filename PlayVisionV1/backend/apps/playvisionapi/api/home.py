from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes, inline_serializer
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db.models import Prefetch
from ..models import PlayerSeasonStats, Season, Match, Competition
from ..serializer import PlayerSeasonStatsSerializer, HomeCompetitionsMatchesSerializer, PlayerLineupSerializer
from ..utils.utils import FORMATION_POSITIONS

#Return homepage data which includes top season players, competitions and matches of the day
@extend_schema(
    description="Return homepage data which includes top season players," \
    "a list of matches of the day from different competitions. ",
    parameters= [
        OpenApiParameter(
             name="date",
             type=str,
             location= OpenApiParameter.QUERY,
             description="The date to get homepage data for (format: YYYY-MM-DD)." \
             " If not provided, it will return data for the current date.",
             required=False,
             examples=[OpenApiExample("date-example", value="2024-08-17")]

        )
    ],
    responses={
         200: inline_serializer(
              name = 'HomePageResponse',
              fields={
                    'competitions': HomeCompetitionsMatchesSerializer(many=True),
                    'top_scorers': PlayerSeasonStatsSerializer(many=True),
                    'top_media': PlayerSeasonStatsSerializer(many=True),
                    'most_yellow_cards': PlayerSeasonStatsSerializer(many=True),
                    'top_goalkeepers': PlayerSeasonStatsSerializer(many=True),
                    'top_player_lineup': PlayerLineupSerializer(many=True)
              }
         ),
         400: OpenApiTypes.OBJECT
    },
    examples=[
         OpenApiExample(
              'Invalid Date Format',
              value={"detail":"Invalid format"},
              status_codes=[400]
         )
    ],
    auth=None,
    tags=["Home"]
)
@api_view(["GET"])
def homepage(request):

    try:
        date_str = request.query_params.get("date")

        if not date_str:
            target_date = timezone.localdate()
            actual_season = 2024 #datetime.now().year

        else:
            target_date = parse_date(date_str)
            actual_season = target_date.year
        
    except Exception as e:
            return Response({"detail":"Invalid format"},status=400)

    players_positions_in_lineup = FORMATION_POSITIONS.get("4-3-3",[])
    top_player_lineup = []
        
    for position in players_positions_in_lineup:
        player_obj = (
            PlayerSeasonStats.objects
            .filter(player__position=position, season__year_start=actual_season)
            .order_by("-media")
            .select_related("player","team")
            .first()
        )
        if player_obj:
            top_player_lineup.append(player_obj)

    season_obj = Season.objects.filter(year_start=actual_season).first()
    top_goals_player_qs = PlayerSeasonStats.objects.filter(season = season_obj).order_by("-goals")[:5]
    top_media_player_qs = PlayerSeasonStats.objects.filter(season = season_obj).order_by("-media")[:5]
    most_yellow_card_qs = PlayerSeasonStats.objects.filter(season = season_obj).order_by("-yellow_cards")[:5]
    top_goalkeepers_qs = PlayerSeasonStats.objects.filter(season = season_obj).order_by("-cleansheets")[:5]
    matches_qs = Match.objects.filter(match_date="2024-08-17").select_related("home_team","away_team")
    
    competition_qs = Competition.objects.all().prefetch_related(
        Prefetch("match_competition",queryset=matches_qs.order_by("start_time"),to_attr="competition_matches")
    )
    competition_qs = competition_qs.filter(match_competition__match_date="2024-08-17").distinct()
    competitions_matches_serializer = HomeCompetitionsMatchesSerializer(
         competition_qs, 
         many=True, 
         context ={
              "request":request
        })
    top_goals_player_serializer = PlayerSeasonStatsSerializer(top_goals_player_qs,many=True)
    top_media_player_serializer = PlayerSeasonStatsSerializer(top_media_player_qs,many=True)
    most_yellow_card_serializer = PlayerSeasonStatsSerializer(most_yellow_card_qs,many=True)
    top_goalkeepers_serializer = PlayerSeasonStatsSerializer(top_goalkeepers_qs,many=True)
    top_player_lineup_serializer = PlayerLineupSerializer(top_player_lineup,many=True)
    
    return Response({
        "competitions" : competitions_matches_serializer.data,
        "top_scorers" : top_goals_player_serializer.data,
        "top_media_players" : top_media_player_serializer.data,
        "most_yellow_cards" : most_yellow_card_serializer.data,
        "top_goalkeepers" : top_goalkeepers_serializer.data,
        "top_players_lineup": top_player_lineup_serializer.data
    })