from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Prefetch
from ..models import Competition, Country , Season, TeamCompetitionStats, Match, PlayerCompetitionStats
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..serializer import CompetitonTeamStatSerializer, PlayerCompetitionStatsSerializer, CountryCompetitionSerializer, CompetitionMatchesListSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#Return list of competitions grouped by country
@api_view(["GET"])
def competition_list(request):
    competition_qs = Competition.objects.filter(competition_type = 'league').order_by('title')
    countries_qs = Country.objects.prefetch_related(Prefetch("competition_country",queryset=competition_qs))
    serializer = CountryCompetitionSerializer(countries_qs,many=True)
    return Response({
        "countries" : serializer.data
    })

#Return competition details including top players and last matches by team
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
    matches_qs = Match.objects.filter(competition=competition_qs,season=season_obj).filter(
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

    competition_serializer = CompetitonTeamStatSerializer(competition_qs,many=False,context={
        "last_matches_by_team": last_matches_by_team
    })
    top_goals_player_serializer = PlayerCompetitionStatsSerializer(top_goals_player_qs,many=True)
    top_media_player_serializer = PlayerCompetitionStatsSerializer(top_media_player_qs,many=True)
    most_yellow_card_serializer = PlayerCompetitionStatsSerializer(most_yellow_card_qs,many=True)
    top_goalkeepers_serializer = PlayerCompetitionStatsSerializer(top_goalkeepers_qs,many=True)
    
    return Response({
        "competition": competition_serializer.data,
        "top_scorers" : top_goals_player_serializer.data,
        "top_media_players" : top_media_player_serializer.data,
        "most_yellow_cards" : most_yellow_card_serializer.data,
        "top_goalkeepers" : top_goalkeepers_serializer.data,
    })

#Return competition matches with pagination
@api_view(["GET"])
def competition_matches(request,ctitle):
    start = int(request.query_params.get("start",0))
    limit = int(request.query_params.get("limit",20))
    season_param = request.query_params.get("season")
    
    if not season_param:
        #season_param = datetime.now().year
        season_param = 2024
        #return Response({"detail":"Formato no válido"},status=400)
    
    season_obj = Season.objects.filter(year_start=season_param).first()
    competition_qs = get_object_or_404(Competition, slug=ctitle)
    matches_qs = Match.objects.filter(season=season_obj,competition=competition_qs).order_by("description")
    paginator = Paginator(matches_qs, limit)
    page_number = (start // limit) + 1

    try:
        page = paginator.page(page_number)
        page_qs = page.object_list
    except PageNotAnInteger:
        page_qs = paginator.page(1).object_list
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
        page_qs = page.object_list

    matches_cmpt_serializer = CompetitionMatchesListSerializer(page_qs,many=True)
    return Response({
        "matches": matches_cmpt_serializer.data,
        "total": paginator.count
    })