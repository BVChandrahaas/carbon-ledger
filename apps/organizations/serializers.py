"""
Organization serializers for API.
"""

from rest_framework import serializers
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Serializer for Organization model.
    """
    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'industry',
            'country',
            'baseline_year',
            'fiscal_year_start',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrganizationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating organizations.
    """
    class Meta:
        model = Organization
        fields = ['name', 'industry', 'country', 'baseline_year', 'fiscal_year_start']
    
    def validate_baseline_year(self, value):
        """Validate baseline year is reasonable."""
        if value < 1990 or value > 2030:
            raise serializers.ValidationError("Baseline year must be between 1990 and 2030")
        return value
