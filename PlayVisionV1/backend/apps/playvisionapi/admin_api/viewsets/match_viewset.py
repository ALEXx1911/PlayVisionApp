from rest_framework import viewsets, filters
from apps.playvisionapi.models import Match
from apps.playvisionapi.serializer import MatchSerializer
from apps.playvisionapi.admin_api.pagination import StandardResultsSetPagination

class MatchViewSet(viewsets.ModelViewSet):
    serializer_class = MatchSerializer
    queryset = Match.objects.all()

    pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['home_team__title', 'away_team__title', 'competition__title']