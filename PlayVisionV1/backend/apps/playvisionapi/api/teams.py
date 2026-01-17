from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..models import Team, Season, PlayerSeasonStats, TeamInsights, Match
from ..serializer import TeamSerializer, TeamInsightsSerializer, PlayerSeasonStatsSerializer, CompetitionMatchesListSerializer
from ..utils.utils import get_last_matches_results

#Return detailed information about a specific team
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
    team_matches_obj = Match.objects.filter(Q(away_team = team_obj) | Q(home_team = team_obj),season = season_obj)
    last_five_results_obj = Match.objects.filter(Q(away_team = team_obj) | Q(home_team = team_obj),season = season_obj).order_by("-match_date")[:5]

    last_five_results = get_last_matches_results(last_five_results_obj,team_obj)

    team_serializer = TeamSerializer(team_obj)
    team_insights_serializer = TeamInsightsSerializer(team_insights_obj,many=True)
    player_season_serializer = PlayerSeasonStatsSerializer(player_season_stats_obj,many=True)
    team_matches_serializer = CompetitionMatchesListSerializer(team_matches_obj,many=True)
    return Response({
        "team" : team_serializer.data,
        "insights" : team_insights_serializer.data,
        "player_stats" : player_season_serializer.data,
        "matches" : team_matches_serializer.data,
        "last_five_results": last_five_results
    })
