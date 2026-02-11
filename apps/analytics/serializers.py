from rest_framework import serializers
from .models import EmissionSummaryMonthly


class EmissionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmissionSummaryMonthly
        fields = '__all__'
