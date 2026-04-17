from rest_framework import viewsets, permissions, filters
from apps.playvisionapi.models import PlayerCompetitionStats
from apps.playvisionapi.serializer import PlayerCompetitionStatsSerializer
from apps.playvisionapi.admin_api.pagination import StandardResultsSetPagination

class PlayerCompetitionStatsViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerCompetitionStatsSerializer
    queryset = PlayerCompetitionStats.objects.all()

    #permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['player__name']