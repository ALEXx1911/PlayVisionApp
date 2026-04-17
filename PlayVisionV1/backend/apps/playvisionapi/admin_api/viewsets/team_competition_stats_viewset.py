from rest_framework import viewsets, permissions, filters
from apps.playvisionapi.models import TeamCompetitionStats
from apps.playvisionapi.serializer import TeamCompetitionStatSerializer
from apps.playvisionapi.admin_api.pagination import StandardResultsSetPagination


class TeamCompetitionStatsViewSet(viewsets.ModelViewSet):
    serializer_class = TeamCompetitionStatSerializer
    queryset = TeamCompetitionStats.objects.all()

    pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['team__title']