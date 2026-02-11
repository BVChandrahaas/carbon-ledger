"""
Global constants used across the application.
"""

# Emission Scopes
SCOPE_CHOICES = [
    ('scope1', 'Scope 1 - Direct Emissions'),
    ('scope2', 'Scope 2 - Indirect Emissions (Electricity)'),
    ('scope3', 'Scope 3 - Other Indirect Emissions'),
]

SCOPE_DICT = {
    'scope1': 'Scope 1',
    'scope2': 'Scope 2',
    'scope3': 'Scope 3',
}

# Emission Record Status
STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('verified', 'Verified'),
]

# Data Quality
DATA_QUALITY_CHOICES = [
    ('measured', 'Measured'),
    ('calculated', 'Calculated'),
    ('estimated', 'Estimated'),
    ('proxy', 'Proxy Data'),
]

# Common Units
UNIT_CHOICES = [
    # Energy
    ('kWh', 'Kilowatt-hour'),
    ('MWh', 'Megawatt-hour'),
    ('GJ', 'Gigajoule'),
    
    # Volume
    ('liter', 'Liter'),
    ('gallon', 'Gallon'),
    ('m3', 'Cubic meter'),
    
    # Mass
    ('kg', 'Kilogram'),
    ('tonne', 'Metric ton'),
    ('lb', 'Pound'),
    
    # Distance
    ('km', 'Kilometer'),
    ('mile', 'Mile'),
    
    # Other
    ('unit', 'Unit'),
]

# Facility Types
FACILITY_TYPE_CHOICES = [
    ('office', 'Office'),
    ('manufacturing', 'Manufacturing Plant'),
    ('warehouse', 'Warehouse'),
    ('retail', 'Retail Store'),
    ('data_center', 'Data Center'),
    ('other', 'Other'),
]

# Common Emission Categories
SCOPE1_CATEGORIES = [
    'Stationary Combustion',
    'Mobile Combustion',
    'Fugitive Emissions',
    'Process Emissions',
]

SCOPE2_CATEGORIES = [
    'Purchased Electricity',
    'Purchased Heat',
    'Purchased Steam',
    'Purchased Cooling',
]

SCOPE3_CATEGORIES = [
    'Purchased Goods and Services',
    'Capital Goods',
    'Fuel and Energy Related Activities',
    'Upstream Transportation',
    'Waste Generated in Operations',
    'Business Travel',
    'Employee Commuting',
    'Upstream Leased Assets',
    'Downstream Transportation',
    'Processing of Sold Products',
    'Use of Sold Products',
    'End-of-Life Treatment',
    'Downstream Leased Assets',
    'Franchises',
    'Investments',
]
