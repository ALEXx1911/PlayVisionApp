from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db.models import Prefetch , Q
from .models import Team,Season, Player, PlayerSeasonStats, Match, Competition , Country , PlayerCompetitionStats , TeamCompetitionStats, MatchStats, MatchEvent
from .serializer import MatchSerializer, MatchEventSerializer, TeamSerializer, TeamCompetitionStatSerializer , PlayerSerializer, PlayerSeasonStatsSerializer, CompetitionsMatchesSerializer , CountryCompetitionSerializer , CompetitonTeamStatSerializer, PlayerCompetitionStatsSerializer , CompetitionMatchesListSerializer

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

@api_view(["GET"])
def player_details(request,pname):
    season_param = request.query_params.get("season")
    if not season_param:
        #season_param = datetime.now().year
        season_param = 2024
        #return Response({"detail":"Invalid date format"},status=400)

    season_obj = Season.objects.filter(year_start = season_param).first()
    player_qs = get_object_or_404(Player, pname = pname)
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

@api_view(["GET"])
def match_details(request,matchid):
    match_qs = get_object_or_404(Match, id = matchid)

    match_serializer = MatchSerializer(match_qs,many=False)

    if not match_qs:
        return Response({"detail":"No se encontró el partido"},status=404)
    
    if match_qs.status == "Not Started":
        home_team_qs = get_object_or_404(Team, id = match_qs.home_team.id) 
        away_team_qs = get_object_or_404(Team, id = match_qs.away_team.id) 
        home_team_last_matches_qs = Match.objects.filter(Q(home_team = home_team_qs) | Q(away_team= home_team_qs)).order_by("-match_date")[:5]
        away_team_last_matches_qs = Match.objects.filter(Q(home_team = away_team_qs) | Q(away_team= away_team_qs)).order_by("-match_date")[:5]
        home_team_obj = TeamCompetitionStats.objects.filter(team=home_team_qs).first()
        away_team_obj = TeamCompetitionStats.objects.filter(team=away_team_qs).first()

        home_stats_serializer = TeamCompetitionStatSerializer(home_team_obj,many=False)
        away_stats_serializer = TeamCompetitionStatSerializer(away_team_obj,many=False)
        home_matches_serializer = CompetitionMatchesListSerializer(home_team_last_matches_qs,many=True)
        away_matches_serializer = CompetitionMatchesListSerializer(away_team_last_matches_qs,many=True)
        
        return Response({
            "data" : match_serializer.data,
            "home_team_stats" : home_stats_serializer.data,
            "away_team_stats" : away_stats_serializer.data,
            "home_last_matches" : home_matches_serializer.data,
            "away_last_matches" : away_matches_serializer.data
        })
    
    if match_qs.status == "Finished":
        match_stats_qs = MatchStats.objects.filter(match = match_qs).first()
        match_events_qs = MatchEvent.objects.filter(match = match_qs).order_by("minute")
        #match_stats_serializer = MatchStatsSerializer(match_stats_qs,many=False)
        match_events_serializer = MatchEventSerializer(match_events_qs,many=True)
        match_stats = []
        for item in match_stats_header:
            match_stats.append({
                "field": item["field"],
                "home_data": getattr(match_stats_qs, item["home_data"]),
                "away_data": getattr(match_stats_qs, item["away_data"])
            })

        return Response({
            "data" : match_serializer.data,
            #"match_stats" : match_stats_serializer.data,
            "match_stats" : match_stats,
            "match_events" : match_events_serializer.data
        })
    
match_stats_header = [
    {
        "field":"Shots",
        "home_data":"home_shots",
        "away_data":"away_shots"
     },
     {
        "field":"Shots on Target",
        "home_data":"home_shots_ontarget",
        "away_data":"away_shots_ontarget"
     },
     {
        "field":"Corners",
        "home_data":"home_corners",
        "away_data":"away_corners"
     },
     {
        "field":"Possession %",
        "home_data":"home_possession",
        "away_data":"away_possession"
     },
     {
        "field":"Passes",
        "home_data":"home_passes",
        "away_data":"away_passes"
     },
     {
        "field":"Fouls",
        "home_data":"home_fouls",
        "away_data":"away_fouls"
     },
     {
        "field":"Yellow Cards",
        "home_data":"home_yellow_cards",
        "away_data":"away_yellow_cards"
     },
     {
        "field":"Red Cards",
        "home_data":"home_red_cards",
        "away_data":"away_red_cards"
     },
     {
        "field":"Offsides",
        "home_data":"home_offsides",
        "away_data":"away_offsides"
     }

]