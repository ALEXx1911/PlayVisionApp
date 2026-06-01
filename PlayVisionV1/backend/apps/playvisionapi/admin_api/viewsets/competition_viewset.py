from rest_framework import viewsets, filters
from apps.playvisionapi.models import Competition
from apps.playvisionapi.serializer import CompetitionSerializer
from apps.playvisionapi.admin_api.pagination import StandardResultsSetPagination

class CompetitionViewSet(viewsets.ModelViewSet):
    serializer_class = CompetitionSerializer
    queryset = Competition.objects.all()

    #permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'slug']
