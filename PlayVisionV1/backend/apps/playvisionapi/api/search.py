from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Player, Team, Competition , Season , PlayerSeasonStats
from ..serializer import PlayerSerializer, TeamSerializer, CompetitionSerializer , PlayerSeasonStatSerializerBasic

#Return search results for players, teams, and competitions
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
            "players_data": player_serializer.data}
        )
    if team_serializer.data:
        search_results.append(
        {
            "field":"Teams Results",
            "teams_data": team_serializer.data},
        )
    if competition_serializer.data:
        search_results.append(    
        {
            "field":"Competitions Results",
            "competitions_data": competition_serializer.data}
        )

    return Response({
        "search_results" : search_results,
    })

#Return comparison data for two players
@api_view (["GET"])
def compare_players(request):
    season_param = request.query_params.get("season")
    player1_slug = request.query_params.get("player1")
    player2_slug = request.query_params.get("player2")
    player_label = ""

    if not season_param:
        #season_param = datetime.now().year
        season_param = 2024
    
    season_obj = Season.objects.filter(year_start = season_param).first()

    if not player1_slug and not player2_slug:
        return Response({"detail":"The player name is required."},status=400)

    if (not player1_slug and player2_slug) or (player1_slug and not player2_slug):
        player_label = "player 1" if player1_slug else "player 2"
        player_qs = get_object_or_404(Player, slug = player1_slug.strip())
        player_season_stats_qs = get_object_or_404(PlayerSeasonStats, player = player_qs,season = season_obj)
        
        player_serializer = PlayerSerializer(player_qs,many=False)
        player_season_stat_serializer = PlayerSeasonStatSerializerBasic(player_season_stats_qs,many =False)
        return Response({
            "player_data" : player_serializer.data,
            "season_stats" : player_season_stat_serializer.data,
            "label": player_label
        })

    player1_qs = get_object_or_404(Player, slug = player1_slug.strip())
    player1_season_stats_qs = get_object_or_404(PlayerSeasonStats, player = player1_qs,season = season_obj)
    player2_qs = get_object_or_404(Player, slug = player2_slug.strip())
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