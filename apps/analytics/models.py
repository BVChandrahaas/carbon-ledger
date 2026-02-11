"""
EmissionSummaryMonthly model - stores aggregated data for fast performance.
"""

from django.db import models
from apps.core.models import BaseModel


class EmissionSummaryMonthly(BaseModel):
    """
    Pre-calculated monthly summaries to avoid scanning millions of records for dashboard.
    """
    organization = models.ForeignKey(
        'organizations.Organization', 
        on_delete=models.CASCADE, 
        related_name='monthly_summaries'
    )
    facility = models.ForeignKey(
        'facilities.Facility', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='monthly_summaries'
    )
    
    reporting_period = models.CharField(max_length=7)  # YYYY-MM
    scope = models.CharField(max_length=10, blank=True)  # Blank means total across scopes
    
    total_co2e = models.DecimalField(max_digits=15, decimal_places=4)
    record_count = models.IntegerField(default=0)
    
    last_calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'emission_summary_monthly'
        unique_together = [['organization', 'facility', 'reporting_period', 'scope']]
        indexes = [
            models.Index(fields=['organization', 'reporting_period']),
            models.Index(fields=['organization', 'scope']),
        ]

    def __str__(self):
        fac_name = self.facility.name if self.facility else "Total Org"
        return f"{fac_name} - {self.reporting_period} - {self.total_co2e} kg CO2e"
