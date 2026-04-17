from rest_framework import viewsets, filters
from apps.playvisionapi.models import Player
from apps.playvisionapi.serializer import PlayerSerializer
from apps.playvisionapi.admin_api.pagination import StandardResultsSetPagination

class PlayerViewSet(viewsets.ModelViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all()

    #permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['common_name', 'slug']