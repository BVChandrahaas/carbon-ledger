"""
Utility functions used across the application.
"""

from decimal import Decimal
from datetime import datetime


def format_period(date):
    """
    Convert date to YYYY-MM format for reporting_period.
    
    Args:
        date: datetime.date or datetime.datetime object
    
    Returns:
        str: Period in YYYY-MM format (e.g., '2024-01')
    """
    if isinstance(date, datetime):
        return date.strftime('%Y-%m')
    return date.strftime('%Y-%m')


def format_number(value, decimals=2):
    """
    Format number with thousand separators.
    
    Args:
        value: Number to format
        decimals: Number of decimal places
    
    Returns:
        str: Formatted number (e.g., '1,234.56')
    """
    if value is None:
        return '0'
    return f"{value:,.{decimals}f}"


def convert_units(quantity, from_unit, to_unit):
    """
    Convert between units (basic implementation).
    TODO: Expand with more unit conversions.
    
    Args:
        quantity: Amount to convert
        from_unit: Source unit
        to_unit: Target unit
    
    Returns:
        Decimal: Converted quantity
    """
    quantity = Decimal(str(quantity))
    
    # Energy conversions
    energy_conversions = {
        ('kWh', 'MWh'): Decimal('0.001'),
        ('MWh', 'kWh'): Decimal('1000'),
        ('kWh', 'GJ'): Decimal('0.0036'),
        ('GJ', 'kWh'): Decimal('277.778'),
    }
    
    # Volume conversions
    volume_conversions = {
        ('liter', 'm3'): Decimal('0.001'),
        ('m3', 'liter'): Decimal('1000'),
        ('gallon', 'liter'): Decimal('3.78541'),
        ('liter', 'gallon'): Decimal('0.264172'),
    }
    
    # Mass conversions
    mass_conversions = {
        ('kg', 'tonne'): Decimal('0.001'),
        ('tonne', 'kg'): Decimal('1000'),
        ('lb', 'kg'): Decimal('0.453592'),
        ('kg', 'lb'): Decimal('2.20462'),
    }
    
    # Distance conversions
    distance_conversions = {
        ('km', 'mile'): Decimal('0.621371'),
        ('mile', 'km'): Decimal('1.60934'),
    }
    
    # Combine all conversions
    all_conversions = {
        **energy_conversions,
        **volume_conversions,
        **mass_conversions,
        **distance_conversions,
    }
    
    # If same unit, no conversion needed
    if from_unit == to_unit:
        return quantity
    
    # Look up conversion factor
    conversion_key = (from_unit, to_unit)
    if conversion_key in all_conversions:
        return quantity * all_conversions[conversion_key]
    
    # If conversion not found, return original
    # In production, should raise an exception
    return quantity
