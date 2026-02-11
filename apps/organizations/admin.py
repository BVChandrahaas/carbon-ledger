from django.contrib import admin
from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'country', 'baseline_year', 'is_active', 'created_at']
    list_filter = ['is_active', 'industry', 'country']
    search_fields = ['name', 'industry']
    ordering = ['name']
