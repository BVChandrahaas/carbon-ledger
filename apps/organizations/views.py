"""
Organization API views.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Organization
from .serializers import OrganizationSerializer, OrganizationCreateSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    API endpoints for organizations.
    
    list: Get all organizations
    retrieve: Get single organization
    create: Create new organization
    update: Update organization
    partial_update: Partially update organization
    destroy: Delete organization (soft delete)
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    
    def get_serializer_class(self):
        """Use different serializer for create."""
        if self.action == 'create':
            return OrganizationCreateSerializer
        return OrganizationSerializer
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """
        Get organization statistics.
        Returns basic stats for now, will be enhanced with emission data.
        """
        organization = self.get_object()
        
        # TODO: Add emission statistics when analytics app is ready
        stats = {
            'organization_id': str(organization.id),
            'name': organization.name,
            'baseline_year': organization.baseline_year,
            'facilities_count': organization.facility_set.count(),
            'is_active': organization.is_active,
        }
        
        return Response(stats)
