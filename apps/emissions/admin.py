from django.contrib import admin
from .models import EmissionRecord, ScopeDetails

class ScopeDetailsInline(admin.StackedInline):
    model = ScopeDetails
    can_delete = False

@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):
    list_display = [
        'category', 'scope', 'organization', 'facility', 
        'quantity', 'unit', 'co2e_calculated', 
        'activity_date', 'reporting_period', 'status'
    ]
    list_filter = ['scope', 'status', 'organization', 'reporting_period']
    search_fields = ['category', 'subcategory', 'notes']
    date_hierarchy = 'activity_date'
    inlines = [ScopeDetailsInline]
    raw_id_fields = ['organization', 'facility', 'emission_factor']
    readonly_fields = ['co2e_calculated']
