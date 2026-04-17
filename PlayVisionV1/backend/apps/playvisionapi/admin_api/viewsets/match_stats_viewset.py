from rest_framework import viewsets, permissions, filters
from apps.playvisionapi.models import MatchStats
from apps.playvisionapi.serializer import MatchStatsSerializer
from apps.playvisionapi.admin_api.pagination import StandardResultsSetPagination

class MatchStatsViewSet(viewsets.ModelViewSet):
    serializer_class = MatchStatsSerializer
    queryset = MatchStats.objects.all()

    pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['match__home_team__title', 'match__away_team__title']