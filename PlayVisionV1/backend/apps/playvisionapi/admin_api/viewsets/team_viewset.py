from rest_framework import viewsets, permissions , filters
from apps.playvisionapi.models import Team
from apps.playvisionapi.serializer import TeamSerializer
from apps.playvisionapi.admin_api.pagination import StandardResultsSetPagination

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    
    #permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'slug']
    