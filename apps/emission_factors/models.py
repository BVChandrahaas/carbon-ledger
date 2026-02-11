"""
EmissionFactor model - the calculation library for the platform.
"""

from django.db import models
from apps.core.models import BaseModel
from apps.core.constants import SCOPE_CHOICES


class EmissionFactor(BaseModel):
    """
    Stores emission factors for various activity types.
    Example: 2.68 kg CO2e per liter of Diesel.
    """
    # Classification
    scope = models.CharField(max_length=10, choices=SCOPE_CHOICES)
    category = models.CharField(max_length=100, help_text="Emission category (e.g., 'Diesel', 'Electricity')")
    subcategory = models.CharField(max_length=100, blank=True, help_text="Subcategory (e.g., 'Economy Class')")
    
    # Emission Factor Data
    emission_factor_co2e = models.DecimalField(
        max_digits=12, 
        decimal_places=6, 
        help_text="kg CO2e per unit"
    )
    unit = models.CharField(max_length=50, help_text="Unit (e.g., 'liter', 'kWh', 'km', 'kg')")
    
    # Geography & Validity
    region = models.CharField(max_length=100, default='Global', help_text="Region for this factor")
    source = models.CharField(max_length=255, blank=True, help_text="Data source (e.g., 'IPCC 2024')")
    valid_year = models.IntegerField(default=2024, help_text="Year this factor is valid for")
    
    class Meta:
        db_table = 'emission_factors'
        unique_together = [['scope', 'category', 'subcategory', 'region', 'valid_year']]
        ordering = ['scope', 'category', 'subcategory']
        indexes = [
            models.Index(fields=['scope', 'category', 'region']),
        ]

    def __str__(self):
        parts = [self.scope.upper(), self.category]
        if self.subcategory:
            parts.append(self.subcategory)
        parts.append(f"({self.region})")
        return " - ".join(parts)
