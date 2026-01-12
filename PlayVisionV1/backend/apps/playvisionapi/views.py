from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db.models import Prefetch , Q
from .models import Team, TeamInsights ,Season, Player, PlayerSeasonStats, Match, Competition , Country , PlayerCompetitionStats , TeamCompetitionStats, MatchStats, MatchEvent
from .serializer import CompetitionSerializer, MatchSerializer, MatchEventSerializer, TeamSerializer, TeamInsightsSerializer , TeamCompetitionStatSerializer , PlayerSerializer , PlayerSeasonStatSerializerBasic , PlayerLineupSerializer , PlayerSeasonStatsSerializer, CompetitionsMatchesSerializer , CountryCompetitionSerializer , CompetitonTeamStatSerializer, PlayerCompetitionStatsSerializer , CompetitionMatchesListSerializer
from .utils.utils import match_stats_header , get_last_matches_results , FORMATION_POSITIONS

#Get homepage data
@api_view(["GET"])
def homepage(request):
    date_str = request.query_params.get("date")
    positions = FORMATION_POSITIONS.get("4-3-3",[])
    top_player_lineup = []
    if date_str :
        target_date = parse_date(date_str)
        actual_season = target_date.year
        if target_date is None:
            return Response({"detail":"Invalid format"},status=400)
    else:
        target_date = timezone.localdate()
        actual_season = 2024 #datetime.now().year
        
    for position in positions:
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
    top_goals_player_serializer = PlayerSeasonStatsSerializer(top_goals_player_qs,many=True)
    top_media_player_serializer = PlayerSeasonStatsSerializer(top_media_player_qs,many=True)
    most_yellow_card_serializer = PlayerSeasonStatsSerializer(most_yellow_card_qs,many=True)
    top_goalkeepers_serializer = PlayerSeasonStatsSerializer(top_goalkeepers_qs,many=True)
    competitions_matches_serializer = CompetitionsMatchesSerializer(competition_qs, many=True, context ={"request":request})
    top_player_lineup_serializer = PlayerLineupSerializer(top_player_lineup,many=True)
    return Response({
        "competitions" : competitions_matches_serializer.data,
        "top_scorers" : top_goals_player_serializer.data,
        "top_media_players" : top_media_player_serializer.data,
        "most_yellow_cards" : most_yellow_card_serializer.data,
        "top_goalkeepers" : top_goalkeepers_serializer.data,
        "top_players_lineup": top_player_lineup_serializer.data
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

@api_view(["GET"])
def match_details(request,matchid):
    match_qs = get_object_or_404(Match, id = matchid)

    match_serializer = MatchSerializer(match_qs,many=False)

    if not match_qs:
        return Response({"detail":"Match not found"},status=404)
    
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
    
    if match_qs.status == "Finished" or match_qs.status == "FT":
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
    
@api_view (["GET"])
def search_page(request):
    searchParam = request.query_params.get("searchTerm").strip()
    
    if not searchParam or searchParam.strip() == "":
        return Response({"detail":"The search term cannot be empty."},status=400)
    
    player_obj = Player.objects.filter(pname=searchParam)
    team_obj = Team.objects.filter(title=searchParam)
    competition_obj = Competition.objects.filter(title=searchParam)

    if not player_obj.exists():
        player_obj = Player.objects.filter(pname__istartswith=searchParam)
    if not team_obj.exists():
        team_obj = Team.objects.filter(title__istartswith=searchParam)
    if not competition_obj.exists():
        competition_obj = Competition.objects.filter(title__istartswith=searchParam)

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

@api_view (["GET"])
def most_searched_items(request):
    # In the future, implement logic to track and retrieve most searched items
    most_searched_players_qs = Player.objects.all()[:5]
    most_searched_teams_qs = Team.objects.all()[:5]
    most_searched_competitions_qs = Competition.objects.all()[:5]

    most_searched_competitions_serializer = CompetitionSerializer(most_searched_competitions_qs,many=True)
    most_searched_teams_serializer = TeamSerializer(most_searched_teams_qs,many=True)
    most_searched_players_serializer = PlayerSerializer(most_searched_players_qs,many=True)

    return Response({
        "most_searched_competitions": most_searched_competitions_serializer.data,
        "most_searched_teams": most_searched_teams_serializer.data,
        "most_searched_players": most_searched_players_serializer.data,
    })

@api_view (["GET"])
def most_searched_players(request):
    # In the future, implement logic to track and retrieve most searched players
    most_searched_players_qs = Player.objects.all()[:10]
    most_searched_players_serializer = PlayerSerializer(most_searched_players_qs,many=True)

    return Response({
        "most_searched_players": most_searched_players_serializer.data,
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