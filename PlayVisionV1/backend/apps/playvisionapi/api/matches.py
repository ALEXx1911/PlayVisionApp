from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, inline_serializer
from django.db.models import Q
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from ..models import Match, Team, TeamCompetitionStats, MatchStats, MatchEvent
from ..serializer import MatchSerializer,MatchEventSerializer ,TeamCompetitionStatSerializer, CompetitionMatchesListSerializer
from ..utils.utils import match_stats_header

#Return detailed information about a specific match
@extend_schema(
    description="Return detailed information about a finished specific match. ",
    parameters = [
        OpenApiParameter(
            name="matchid",
            type=int,
            location=OpenApiParameter.PATH,
            description="The ID of the match to retrieve details for",
            required=True,
            examples=[OpenApiExample("match-id", value=1)]
        )
    ],
    responses={
        200: inline_serializer(
            name='MatchDetailsResponse',
            fields={
                'match_data': MatchSerializer(),
                'match_stats': inline_serializer(
                    name='MatchStats',
                    fields={
                        "field": serializers.CharField(),
                        "home_data": serializers.CharField(),
                        "away_data": serializers.CharField()
                    },
                    many=True
                ),
                'match_events': MatchEventSerializer(many=True)
            }
        ),
        404: OpenApiResponse(
            response=inline_serializer(
                name='MatchNotFoundResponse',
                fields={
                    "detail": serializers.CharField()
                }
            ),
            description="Match not found with the provided ID.",
            examples=[
                OpenApiExample(
                    'Match Not Found',
                    value={"detail":"Not Match found with the provided ID."},
                    description="Match not found with the provided ID."
                )
            ]
        )
    },
    auth=None,
    tags=["Matches"],
)
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
            "match_data" : match_serializer.data,
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
            "match_data" : match_serializer.data,
            #"match_stats" : match_stats_serializer.data,
            "match_stats" : match_stats,
            "match_events" : match_events_serializer.data
        })