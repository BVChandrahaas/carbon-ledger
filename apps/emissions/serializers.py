from rest_framework import serializers
from .models import EmissionRecord, ScopeDetails
from apps.emission_factors.models import EmissionFactor


class ScopeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScopeDetails
        fields = ['details']


class EmissionRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for EmissionRecord model.
    """
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    scope_details = ScopeDetailsSerializer(read_only=True)
    details_data = serializers.JSONField(write_only=True, required=False)
    reporting_period = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = EmissionRecord
        fields = [
            'id', 'organization', 'organization_name', 'facility', 'facility_name',
            'scope', 'category', 'subcategory', 'quantity', 'unit',
            'emission_factor_used', 'emission_factor', 'co2e_calculated',
            'activity_date', 'reporting_period', 'data_source', 'status',
            'notes', 'scope_details', 'details_data', 'created_at'
        ]
        read_only_fields = ['id', 'co2e_calculated', 'created_at']
