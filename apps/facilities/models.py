"""
Facility model - represents emission source locations.
"""

from django.db import models
from apps.core.models import BaseModel
from apps.core.constants import FACILITY_TYPE_CHOICES


class Facility(BaseModel):
    """
    Represents a physical location where emissions occur.
    """
    # Relationships
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='facilities'
    )
    
    # Basic Information
    name = models.CharField(max_length=255, help_text="Facility name")
    facility_type = models.CharField(
        max_length=100,
        choices=FACILITY_TYPE_CHOICES,
        blank=True,
        help_text="Type of facility"
    )
    
    # Location
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=2, blank=True, help_text="ISO country code")
    
    # Grid Region (critical for Scope 2 electricity emission factors)
    grid_region = models.CharField(
        max_length=100,
        blank=True,
        help_text="Electricity grid region (e.g., 'US', 'India-Northern', 'EU-Germany')"
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'facilities'
        ordering = ['name']
        indexes = [
            models.Index(fields=['organization', 'name']),
            models.Index(fields=['country']),
            models.Index(fields=['grid_region']),
        ]
        verbose_name_plural = 'Facilities'
    
    def __str__(self):
        return f"{self.name} ({self.organization.name})"
