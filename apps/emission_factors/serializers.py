from rest_framework import serializers
from .models import EmissionFactor


class EmissionFactorSerializer(serializers.ModelSerializer):
    """
    Serializer for EmissionFactor model.
    """
    class Meta:
        model = EmissionFactor
        fields = '__all__'
