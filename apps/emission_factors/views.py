from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import EmissionFactor
from .serializers import EmissionFactorSerializer


class EmissionFactorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoints for viewing emission factors.
    ReadOnly for MVP to prevent unauthorized changes to the library.
    """
    queryset = EmissionFactor.objects.all()
    serializer_class = EmissionFactorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['scope', 'category', 'region']
    search_fields = ['category', 'subcategory', 'region', 'source']
    ordering_fields = ['category', 'valid_year', 'scope']
