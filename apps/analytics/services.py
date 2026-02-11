from django.db.models import Sum, Count
from .models import EmissionSummaryMonthly
from apps.emissions.models import EmissionRecord


class AnalyticsService:
    """
    Service layer for calculating and retrieving analytics data.
    """
    
    @staticmethod
    def calculate_monthly_summary(organization, period=None, facility=None):
        """
        Calculates and updates summaries. 
        If period is None, it recalculates for all periods found in the organization.
        """
        if period:
            periods = [period]
        else:
            # Get all unique periods for this org
            periods = EmissionRecord.objects.filter(
                organization=organization
            ).values_list('reporting_period', flat=True).distinct()

        for p in periods:
            queryset = EmissionRecord.objects.filter(
                organization=organization,
                reporting_period=p,
                deleted_at__isnull=True
            )
            
            if facility:
                queryset = queryset.filter(facility=facility)
                
            # Get aggregations by scope
            scope_totals = queryset.values('scope').annotate(
                total=Sum('co2e_calculated'),
                count=Count('id')
            )
            
            # Totals across all scopes
            org_total = queryset.aggregate(
                total=Sum('co2e_calculated'),
                count=Count('id')
            )
            
            # Update scope-specific summaries
            for entry in scope_totals:
                EmissionSummaryMonthly.objects.update_or_create(
                    organization=organization,
                    facility=facility,
                    reporting_period=p,
                    scope=entry['scope'],
                    defaults={
                        'total_co2e': entry['total'] or 0,
                        'record_count': entry['count']
                    }
                )
                
            # Update total summary (scope='')
            EmissionSummaryMonthly.objects.update_or_create(
                organization=organization,
                facility=facility,
                reporting_period=p,
                scope='',
                defaults={
                    'total_co2e': org_total['total'] or 0,
                    'record_count': org_total['count']
                }
            )

    @staticmethod
    def get_dashboard_data(organization, period=None):
        """
        Retrieves formatted data. If period is None, returns consolidated (all-time) data.
        """
        queryset = EmissionSummaryMonthly.objects.filter(
            organization=organization,
            facility__isnull=True
        )
        
        if period:
            queryset = queryset.filter(reporting_period=period)
            
        # Aggregate across whatever remains in the queryset (all periods or one)
        aggr = queryset.values('scope').annotate(
            total=Sum('total_co2e'),
            records=Sum('record_count')
        )
            
        data = {
            'total_emissions': 0,
            'scope1': 0,
            'scope2': 0,
            'scope3': 0,
            'record_count': 0,
            'period': period or 'All-Time'
        }
        
        for entry in aggr:
            if entry['scope'] == '':
                data['total_emissions'] = float(entry['total'] or 0)
                data['record_count'] = int(entry['records'] or 0)
            elif entry['scope'] == 'scope1':
                data['scope1'] = float(entry['total'] or 0)
            elif entry['scope'] == 'scope2':
                data['scope2'] = float(entry['total'] or 0)
            elif entry['scope'] == 'scope3':
                data['scope3'] = float(entry['total'] or 0)
                
        return data
