from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import EmissionRecord
from .serializers import EmissionRecordSerializer
from .services import EmissionService


class EmissionRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoints for emission records.
    """
    queryset = EmissionRecord.objects.select_related('organization', 'facility', 'scope_details').all()
    serializer_class = EmissionRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['scope', 'category', 'facility', 'status', 'reporting_period']
    search_fields = ['category', 'subcategory', 'notes']
    ordering_fields = ['activity_date', 'co2e_calculated', 'created_at']

    def get_queryset(self):
        """
        Filter queryset by user's organization if provided.
        """
        queryset = super().get_queryset()
        org_id = self.request.query_params.get('organization', None)
        if org_id:
            queryset = queryset.filter(organization_id=org_id)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Overridden create to use EmissionService for calculation.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        organization = serializer.validated_data.get('organization')
        
        try:
            record = EmissionService.create_record(
                data=serializer.validated_data,
                organization=organization,
                user=request.user if not request.user.is_anonymous else None
            )
            return Response(
                EmissionRecordSerializer(record).data, 
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """
        Bulk creation of records.
        Expects a list of record objects.
        """
        records_data = request.data.get('records', [])
        organization_id = request.data.get('organization')
        
        if not records_data or not organization_id:
            return Response(
                {'error': 'Records and organization are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            from apps.organizations.models import Organization
            organization = Organization.objects.get(id=organization_id)
            
            records = EmissionService.bulk_create_records(
                records_list=records_data,
                organization=organization,
                user=request.user if not request.user.is_anonymous else None
            )
            
            return Response(
                {'message': f'Successfully created {len(records)} records'}, 
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
