from rest_framework import viewsets, permissions, filters
from apps.playvisionapi.models import TeamInsights
from apps.playvisionapi.serializer import TeamInsightsSerializer
from apps.playvisionapi.admin_api.pagination import StandardResultsSetPagination


class TeamInsightsViewSet(viewsets.ModelViewSet):
    serializer_class = TeamInsightsSerializer
    queryset = TeamInsights.objects.all()
    #permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['team__title']