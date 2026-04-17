from rest_framework import viewsets, permissions, filters
from apps.playvisionapi.models import MatchEvent
from apps.playvisionapi.serializer import MatchEventSerializer
from apps.playvisionapi.admin_api.pagination import StandardResultsSetPagination

class MatchEventViewSet(viewsets.ModelViewSet):
    serializer_class = MatchEventSerializer
    queryset = MatchEvent.objects.all()

    pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['match__home_team__title', 'match__away_team__title', 'event_type']