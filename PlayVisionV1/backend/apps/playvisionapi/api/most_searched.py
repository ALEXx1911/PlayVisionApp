from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Player, Team, Competition
from ..serializer import PlayerSerializer, TeamSerializer, CompetitionSerializer

#Return most searched items including players, teams, and competitions
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

#Return most searched players
@api_view (["GET"])
def most_searched_players(request):
    # In the future, implement logic to track and retrieve most searched players
    most_searched_players_qs = Player.objects.all()[:10]
    most_searched_players_serializer = PlayerSerializer(most_searched_players_qs,many=True)

    return Response({
        "most_searched_players": most_searched_players_serializer.data,
    })