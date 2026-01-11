from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db.models import Prefetch , Q
from .models import Team,Season, PlayerSeasonStats, Match, Competition , Country , PlayerCompetitionStats
from .serializer import TeamSerializer, PlayerSeasonStatsSerializer, CompetitionsMatchesSerializer , CountryCompetitionSerializer , CompetitonTeamStatSerializer, PlayerCompetitionStatsSerializer , CompetitionMatchesListSerializer

#Get homepage data
@api_view(["GET"])
def homepage(request):
    date_str = request.query_params.get("date")
    if date_str :
        target_date = parse_date(date_str)
        actual_season = target_date.year
        if target_date is None:
            return Response({"detail":"Invalid date format"},status=400)
    else:
        target_date = timezone.localdate()
        actual_season = 2024 #datetime.now().year

    season_obj = Season.objects.filter(year_start=actual_season).first()
    top_goals_player_obj = PlayerSeasonStats.objects.filter(season = season_obj).order_by("-goals")[:5]
    top_media_player_obj = PlayerSeasonStats.objects.filter(season = season_obj).order_by("-media")[:5]
    most_yellow_card_obj = PlayerSeasonStats.objects.filter(season = season_obj).order_by("-yellow_cards")[:5]
    top_goalkeepers_obj = PlayerSeasonStats.objects.filter(season = season_obj).order_by("-cleansheets")[:5]
    matches_obj = Match.objects.filter(match_date="2024-08-17").select_related("home_team","away_team")
    competition_qs = Competition.objects.all().prefetch_related(
        Prefetch("match_competition",queryset=matches_obj.order_by("start_time"),to_attr="competition_matches")
    )
    competition_obj = competition_qs.filter(match_competition__match_date="2024-08-17").distinct()
    top_goals_player_serializer = PlayerSeasonStatsSerializer(top_goals_player_obj,many=True)
    top_media_player_serializer = PlayerSeasonStatsSerializer(top_media_player_obj,many=True)
    most_yellow_card_serializer = PlayerSeasonStatsSerializer(most_yellow_card_obj,many=True)
    top_goalkeepers_serializer = PlayerSeasonStatsSerializer(top_goalkeepers_obj,many=True)
    competitions_matches_serializer = CompetitionsMatchesSerializer(competition_obj, many=True, context ={"request":request})
    return Response({
        "competitions" : competitions_matches_serializer.data,
        "top_scorers" : top_goals_player_serializer.data,
        "top_media_players" : top_media_player_serializer.data,
        "most_yellow_cards" : most_yellow_card_serializer.data,
        "top_goalkeepers" : top_goalkeepers_serializer.data
    })

@api_view(["GET"])
def competition_list(request):
    comp_qs = Competition.objects.filter(competition_type = 'league').order_by('title')
    countries_qs = Country.objects.prefetch_related(Prefetch("competition_country",queryset=comp_qs))
    serializer = CountryCompetitionSerializer(countries_qs,many=True)
    return Response({
        "countries" : serializer.data
    })

@api_view(["GET"])
def competition_details(request,ctitle):
    season_param = request.query_params.get("season")
    if not season_param:
        #season_param = datetime.now().year
        season_param = 2024
        #return Response({"detail":"Invalid date format"},status=400)
    
    season_obj = Season.objects.filter(year_start=season_param).first()
    competition_qs = get_object_or_404(Competition, title=ctitle)
    top_goals_player_qs = PlayerCompetitionStats.objects.filter(season = season_obj).order_by("-goals")[:5]
    top_media_player_qs = PlayerCompetitionStats.objects.filter(season = season_obj).order_by("-media")[:5]
    most_yellow_card_qs = PlayerCompetitionStats.objects.filter(season = season_obj).order_by("-yellow_cards")[:5]
    top_goalkeepers_qs = PlayerCompetitionStats.objects.filter(season = season_obj).order_by("-cleansheets")[:5]

    competition_serializer = CompetitonTeamStatSerializer(competition_qs,many=False)
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

@api_view(["GET"])
def competition_matches(request,ctitle):
    start = int(request.query_params.get("start",0))
    limit = int(request.query_params.get("limit",20))
    season_param = request.query_params.get("season")
    
    if not season_param:
        #season_param = datetime.now().year
        season_param = 2024
        #return Response({"detail":"Invalid date format"},status=400)
    
    season_obj = Season.objects.filter(year_start=season_param).first()
    competition_qs = get_object_or_404(Competition, title=ctitle)
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

@api_view(["GET"])
def team_details(request, title):
    season_param = request.query_params.get("season")
    if not season_param:
        #season_param = datetime.now().year
        season_param = 2024
        #return Response({"detail":"Invalid date format"},status=400)
    
    season_obj = Season.objects.filter(year_start=season_param).first()
    team_qs = get_object_or_404(Team, title=title)
    player_season_stats_qs = PlayerSeasonStats.objects.filter(team = team_qs, season = season_obj)
    team_matches_qs = Match.objects.filter(Q(away_team = team_qs) | Q(home_team = team_qs),season = season_obj)

    team_serializer = TeamSerializer(team_qs)
    player_season_serializer = PlayerSeasonStatsSerializer(player_season_stats_qs,many=True)
    team_matches_serializer = CompetitionMatchesListSerializer(team_matches_qs,many=True)
    return Response({
        "team" : team_serializer.data,
        "player_stats" : player_season_serializer.data,
        "matches" : team_matches_serializer.data
    })

