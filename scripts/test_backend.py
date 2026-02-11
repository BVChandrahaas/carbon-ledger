import os
import sys
import django
from decimal import Decimal

# Set up Django environment
sys.path.append('E:\\carbon_accounting')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.organizations.models import Organization
from apps.facilities.models import Facility
from apps.emission_factors.models import EmissionFactor
from apps.emissions.models import EmissionRecord
from apps.emissions.services import EmissionService
from apps.analytics.services import AnalyticsService

def run_test():
    print("--- Starting Backend Logic Test ---")
    
    # 1. Create Organization
    org, created = Organization.objects.get_or_create(
        name="Test Corp",
        defaults={'industry': 'Tech', 'country': 'IN'}
    )
    print(f"Organization: {org.name} ({'Created' if created else 'Existing'})")
    
    # 2. Create Facility
    facility, created = Facility.objects.get_or_create(
        organization=org,
        name="Mumbai HQ",
        defaults={'city': 'Mumbai', 'country': 'IN', 'grid_region': 'India'}
    )
    print(f"Facility: {facility.name} ({'Created' if created else 'Existing'})")
    
    # 3. Get Emission Factor (Diesel)
    ef = EmissionFactor.objects.filter(category='Diesel', scope='scope1').first()
    if not ef:
        print("Error: Diesel emission factor not found. Run seed_emission_factors first.")
        return
    print(f"Using EF: {ef.category} ({ef.emission_factor_co2e} {ef.unit})")
    
    # 4. Create Emission Record
    from datetime import date
    record_data = {
        'facility': facility,
        'scope': ef.scope,
        'category': ef.category,
        'subcategory': ef.subcategory,
        'quantity': Decimal('100.0'),
        'unit': ef.unit,
        'emission_factor_used': ef.emission_factor_co2e,
        'emission_factor': ef,
        'activity_date': date(2024, 1, 15),
        'data_source': 'manual_test'
    }
    
    record = EmissionService.create_record(record_data, org)
    print(f"Created Record: {record.category} - {record.co2e_calculated} kg CO2e")
    
    # 5. Check Aggregations
    # Calculate for Jan 2024
    AnalyticsService.calculate_monthly_summary(org, '2024-01')
    
    # Get Dashboard Data
    stats = AnalyticsService.get_dashboard_data(org, '2024-01')
    print(f"Dashboard Stats (2024-01): {stats}")
    
    print("--- Test Completed Successfully ---")

if __name__ == "__main__":
    run_test()
