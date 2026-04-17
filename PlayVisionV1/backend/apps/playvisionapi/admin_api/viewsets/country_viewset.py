from rest_framework import viewsets, permissions, filters
from apps.playvisionapi.models import Country
from apps.playvisionapi.serializer import CountrySerializer
from apps.playvisionapi.admin_api.pagination import StandardResultsSetPagination



class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all

    pagination_class = StandardResultsSetPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['country_name']