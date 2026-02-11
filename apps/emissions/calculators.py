from abc import ABC, abstractmethod
from decimal import Decimal


class BaseCalculator(ABC):
    """
    Abstract base class for all emission calculators.
    """
    @abstractmethod
    def calculate(self, quantity, emission_factor, **kwargs):
        pass

    def validate_inputs(self, quantity, unit):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if not unit:
            raise ValueError("Unit is required")


class StandardCalculator(BaseCalculator):
    """
    Standard calculator: Quantity * Emission Factor.
    Used for most combustion and electricity activities.
    """
    def calculate(self, quantity, emission_factor, **kwargs):
        self.validate_inputs(quantity, 'placeholder') 
        return Decimal(str(quantity)) * Decimal(str(emission_factor))


class FugitiveCalculator(BaseCalculator):
    """
    For fugitive emissions (refrigerants).
    Calculates based on the GWP (Global Warming Potential) of the gas.
    """
    def calculate(self, quantity, emission_factor, **kwargs):
        # EF for refrigerants in our DB is the GWP
        return Decimal(str(quantity)) * Decimal(str(emission_factor))


class RadiativeForcingCalculator(BaseCalculator):
    """
    For air travel. Often requires a Radiative Forcing (RF) multiplier (~1.9x) 
    to account for high-altitude climate impacts.
    """
    def calculate(self, quantity, emission_factor, **kwargs):
        use_rf = kwargs.get('use_rf', True)
        rf_multiplier = Decimal('1.9') if use_rf else Decimal('1.0')
        return Decimal(str(quantity)) * Decimal(str(emission_factor)) * rf_multiplier


class CalculatorFactory:
    """
    Factory to return appropriate calculator based on activity type.
    """
    @staticmethod
    def get_calculator(category):
        category_lower = category.lower()
        if 'refrigerant' in category_lower or 'fugitive' in category_lower:
            return FugitiveCalculator()
        if 'flight' in category_lower or 'air travel' in category_lower:
            return RadiativeForcingCalculator()
        return StandardCalculator()
