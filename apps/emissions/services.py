from django.db import transaction
from .models import EmissionRecord, ScopeDetails
from .calculators import CalculatorFactory
from apps.core.utils import format_period


class EmissionService:
    """
    Business logic layer for emission records.
    """
    
    @staticmethod
    def create_record(data, organization, user=None):
        """
        Creates an emission record and calculates CO2e.
        """
        # Get appropriate calculator
        calculator = CalculatorFactory.get_calculator(data['category'])
        
        # Calculate CO2e
        co2e = calculator.calculate(
            quantity=data['quantity'],
            emission_factor=data['emission_factor_used']
        )
        
        # Ensure reporting period
        if not data.get('reporting_period'):
            data['reporting_period'] = format_period(data['activity_date'])
            
        # Remove organization and details from data to avoid double-assignment in .create()
        data.pop('organization', None)
        details_dict = data.pop('details_data', None)
            
        with transaction.atomic():
            # Create the main record
            record = EmissionRecord.objects.create(
                organization=organization,
                co2e_calculated=co2e,
                created_by=user,
                **data
            )
            
            # Create details if provided
            if details_dict:
                ScopeDetails.objects.create(
                    emission_record=record,
                    details=details_dict
                )
            
            # TODO: Trigger analytics update
            
            return record

    @staticmethod
    def bulk_create_records(records_list, organization, user=None):
        """
        Handles bulk creation of emission records.
        """
        created_records = []
        with transaction.atomic():
            for record_data in records_list:
                record = EmissionService.create_record(record_data, organization, user)
                created_records.append(record)
        return created_records
