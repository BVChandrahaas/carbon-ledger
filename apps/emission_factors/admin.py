from django.contrib import admin
from .models import EmissionFactor


@admin.register(EmissionFactor)
class EmissionFactorAdmin(admin.ModelAdmin):
    list_display = ['category', 'subcategory', 'scope', 'emission_factor_co2e', 'unit', 'region', 'valid_year']
    list_filter = ['scope', 'region', 'valid_year']
    search_fields = ['category', 'subcategory', 'source']
    ordering = ['scope', 'category']
