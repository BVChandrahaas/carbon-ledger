"""
Facility serializers for API.
"""

from rest_framework import serializers
from .models import Facility


class FacilitySerializer(serializers.ModelSerializer):
    """
    Serializer for Facility model.
    """
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    
    class Meta:
        model = Facility
        fields = [
            'id',
            'organization',
            'organization_name',
            'name',
            'facility_type',
            'city',
            'country',
            'grid_region',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class FacilityCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating facilities.
    """
    class Meta:
        model = Facility
        fields = ['organization', 'name', 'facility_type', 'city', 'country', 'grid_region']
    
    def validate_name(self, value):
        """Validate facility name is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("Facility name cannot be empty")
        return value.strip()
