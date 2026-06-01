from rest_framework import viewsets, permissions, filters
from apps.playvisionapi.models import Season
from apps.playvisionapi.serializer import SeasonSerializer
from apps.playvisionapi.admin_api.pagination import StandardResultsSetPagination

class SeasonViewSet(viewsets.ModelViewSet):
    serializer_class = SeasonSerializer
    queryset = Season.objects.all()
    
    #permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['year_start']
