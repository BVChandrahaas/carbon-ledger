"""
EmissionRecord model - stores raw activity data and calculated CO2e.
"""

from django.db import models
from apps.core.models import BaseModel
from apps.core.constants import SCOPE_CHOICES, STATUS_CHOICES


class EmissionRecord(BaseModel):
    """
    The central transaction table for all emission activities.
    """
    # Identity & Hierarchy
    organization = models.ForeignKey(
        'organizations.Organization', 
        on_delete=models.CASCADE, 
        related_name='emission_records'
    )
    facility = models.ForeignKey(
        'facilities.Facility', 
        on_delete=models.CASCADE, 
        related_name='emission_records'
    )
    
    # Classification
    scope = models.CharField(max_length=10, choices=SCOPE_CHOICES)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100, blank=True)
    
    # Activity Data
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    unit = models.CharField(max_length=50)
    
    # Calculation Snapshots
    emission_factor_used = models.DecimalField(
        max_digits=12, 
        decimal_places=6,
        help_text="Snapshot of the EF value used at time of entry"
    )
    emission_factor = models.ForeignKey(
        'emission_factors.EmissionFactor', 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='records'
    )
    co2e_calculated = models.DecimalField(
        max_digits=15, 
        decimal_places=4,
        help_text="Total emissions in kg CO2e (quantity * EF)"
    )
    
    # Temporal Data
    activity_date = models.DateField()
    reporting_period = models.CharField(
        max_length=7, 
        blank=True,
        help_text="YYYY-MM format for aggregation"
    )
    
    # Metadata
    data_source = models.CharField(
        max_length=100, 
        blank=True,
        help_text="e.g., 'utility_bill', 'manual_entry'"
    )
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='draft'
    )
    notes = models.TextField(blank=True)
    
    # Audit
    created_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='recorded_emissions'
    )

    class Meta:
        db_table = 'emission_records'
        ordering = ['-activity_date', '-created_at']
        indexes = [
            models.Index(fields=['organization', 'reporting_period']),
            models.Index(fields=['facility', 'reporting_period']),
            models.Index(fields=['scope', 'category']),
            models.Index(fields=['activity_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.category} ({self.reporting_period}) - {self.co2e_calculated} kg CO2e"


class ScopeDetails(models.Model):
    """
    Flexible extra data for specific emission types using JSONB.
    This replaces having 7 separate detail tables for MVP.
    """
    emission_record = models.OneToOneField(
        EmissionRecord, 
        on_delete=models.CASCADE, 
        related_name='scope_details'
    )
    details = models.JSONField()
    
    class Meta:
        db_table = 'scope_details'
        verbose_name_plural = 'Scope Details'

    def __str__(self):
        return f"Details for {self.emission_record.id}"
