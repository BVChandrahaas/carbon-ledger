"""
Organization model - represents a company/organization.
"""

from django.db import models
from apps.core.models import BaseModel


class Organization(BaseModel):
    """
    Represents a company or organization tracking emissions.
    """
    # Basic Information
    name = models.CharField(max_length=255, help_text="Organization name")
    industry = models.CharField(max_length=100, blank=True, help_text="Industry sector")
    country = models.CharField(max_length=2, blank=True, help_text="ISO country code")
    
    # Configuration
    baseline_year = models.IntegerField(default=2023, help_text="Baseline year for emissions tracking")
    fiscal_year_start = models.CharField(
        max_length=5, 
        default='01-01',
        help_text="Fiscal year start (MM-DD format)"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'organizations'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['industry']),
        ]
    
    def __str__(self):
        return self.name
