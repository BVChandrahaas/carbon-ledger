import uuid
from django.core.management.base import BaseCommand
from apps.emission_factors.models import EmissionFactor

class Command(BaseCommand):
    help = 'Seeds initial common emission factors for the MVP'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding emission factors...")
        
        factors = [
            # --- SCOPE 1: Direct Emissions ---
            # Stationary Combustion
            {'scope': 'scope1', 'category': 'Diesel', 'subcategory': 'Stationary', 'emission_factor_co2e': 2.68787, 'unit': 'liter', 'region': 'Global'},
            {'scope': 'scope1', 'category': 'Natural Gas', 'subcategory': 'Stationary', 'emission_factor_co2e': 2.02135, 'unit': 'm3', 'region': 'Global'},
            {'scope': 'scope1', 'category': 'Natural Gas', 'subcategory': 'Energy-based', 'emission_factor_co2e': 0.18122, 'unit': 'kWh', 'region': 'Global'},
            {'scope': 'scope1', 'category': 'LPG', 'subcategory': 'Stationary', 'emission_factor_co2e': 1.55537, 'unit': 'liter', 'region': 'Global'},
            
            # Mobile Combustion
            {'scope': 'scope1', 'category': 'Petrol', 'subcategory': 'Passenger Car', 'emission_factor_co2e': 2.31495, 'unit': 'liter', 'region': 'Global'},
            {'scope': 'scope1', 'category': 'Diesel', 'subcategory': 'Van (Class II)', 'emission_factor_co2e': 2.68787, 'unit': 'liter', 'region': 'Global'},
            
            # Fugitive Emissions (Refrigerants - GWP values)
            {'scope': 'scope1', 'category': 'Refrigerant', 'subcategory': 'HFC-134a', 'emission_factor_co2e': 1430.0, 'unit': 'kg', 'region': 'Global'},
            {'scope': 'scope1', 'category': 'Refrigerant', 'subcategory': 'R-410A', 'emission_factor_co2e': 2088.0, 'unit': 'kg', 'region': 'Global'},

            # --- SCOPE 2: Indirect Emissions ---
            # Purchased Electricity (Location-based)
            {'scope': 'scope2', 'category': 'Electricity', 'subcategory': 'Grid (India)', 'emission_factor_co2e': 0.712, 'unit': 'kWh', 'region': 'India'},
            {'scope': 'scope2', 'category': 'Electricity', 'subcategory': 'Grid (USA)', 'emission_factor_co2e': 0.385, 'unit': 'kWh', 'region': 'US'},
            {'scope': 'scope2', 'category': 'Electricity', 'subcategory': 'Grid (UK)', 'emission_factor_co2e': 0.285, 'unit': 'kWh', 'region': 'UK'},
            
            # Purchased Heat/Steam
            {'scope': 'scope2', 'category': 'District Heating', 'subcategory': 'Steam', 'emission_factor_co2e': 0.17, 'unit': 'kWh', 'region': 'Global'},

            # --- SCOPE 3: Indirect Value Chain ---
            # Category 1: Purchased Goods and Services
            {'scope': 'scope3', 'category': 'Water Supply', 'subcategory': 'Mains Water', 'emission_factor_co2e': 0.149, 'unit': 'm3', 'region': 'Global'},
            {'scope': 'scope3', 'category': 'Paper', 'subcategory': 'Recycled Content 100%', 'emission_factor_co2e': 0.65, 'unit': 'kg', 'region': 'Global'},
            
            # Category 6: Business Travel
            {'scope': 'scope3', 'category': 'Business Travel', 'subcategory': 'Flight - Long Haul (Economy)', 'emission_factor_co2e': 0.147, 'unit': 'km', 'region': 'Global'},
            {'scope': 'scope3', 'category': 'Business Travel', 'subcategory': 'Taxis', 'emission_factor_co2e': 0.203, 'unit': 'km', 'region': 'Global'},
            
            # Category 7: Employee Commuting
            {'scope': 'scope3', 'category': 'Employee Commuting', 'subcategory': 'Public Transport (Bus)', 'emission_factor_co2e': 0.102, 'unit': 'km', 'region': 'Global'},
        ]
        
        created_count = 0
        for f_data in factors:
            obj, created = EmissionFactor.objects.get_or_create(
                scope=f_data['scope'],
                category=f_data['category'],
                subcategory=f_data['subcategory'],
                region=f_data['region'],
                valid_year=2024,
                defaults={
                    'emission_factor_co2e': f_data['emission_factor_co2e'],
                    'unit': f_data['unit'],
                    'source': 'DEFRA/EPA Mix 2024'
                }
            )
            if created:
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {created_count} emission factors."))
