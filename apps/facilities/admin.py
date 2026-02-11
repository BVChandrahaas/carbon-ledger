from django.contrib import admin
from .models import Facility


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'organization', 'facility_type', 'city', 'country', 'grid_region', 'is_active']
    list_filter = ['is_active', 'facility_type', 'country', 'organization']
    search_fields = ['name', 'city', 'organization__name']
    ordering = ['organization', 'name']
    raw_id_fields = ['organization']
