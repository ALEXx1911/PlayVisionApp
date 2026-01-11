from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.db.models import Prefetch
from .models import Season, PlayerSeasonStats, Match, Competition , Country
from .serializer import PlayerSeasonStatsSerializer, CompetitionsMatchesSerializer , CountryCompetitionSerializer

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
