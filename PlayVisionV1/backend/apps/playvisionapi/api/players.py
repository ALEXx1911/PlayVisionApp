from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Player, Season, PlayerSeasonStats, PlayerCompetitionStats
from ..serializer import PlayerSerializer, PlayerSeasonStatsSerializer, PlayerCompetitionStatsSerializer

#Return detailed information about a specific player
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