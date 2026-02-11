"""
Facility API views.
"""

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Facility
from .serializers import FacilitySerializer, FacilityCreateSerializer


class FacilityViewSet(viewsets.ModelViewSet):
    """
    API endpoints for facilities.
    """
    queryset = Facility.objects.select_related('organization').all()
    serializer_class = FacilitySerializer
    
    def get_serializer_class(self):
        """Use different serializer for create."""
        if self.action == 'create':
            return FacilityCreateSerializer
        return FacilitySerializer
    
    def get_queryset(self):
        """
        Optionally filter by organization.
        """
        queryset = super().get_queryset()
        org_id = self.request.query_params.get('organization', None)
        
        if org_id:
            queryset = queryset.filter(organization_id=org_id)
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def emissions(self, request, pk=None):
        """
        Get emissions for this facility.
        TODO: Implement when emissions app is ready.
        """
        facility = self.get_object()
        
        # Placeholder - will be implemented with emissions app
        return Response({
            'facility_id': str(facility.id),
            'facility_name': facility.name,
            'message': 'Emissions data will be available after emissions app is implemented'
        })
