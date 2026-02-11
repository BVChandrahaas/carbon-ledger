# Quick Reference - Module Descriptions

## Core Django Apps (apps/)

### 1. core/ - Shared Utilities
**Purpose:** Reusable code for all apps (DRY principle)
**Contains:**
- models.py - Abstract base models (TimeStampedModel, UUIDModel, SoftDeleteModel)
- constants.py - Global constants (SCOPE_CHOICES, STATUS_CHOICES)
- managers.py - Custom QuerySets (SoftDeleteManager)
- validators.py - Custom validators (validate_positive_decimal)
- utils.py - Helper functions (convert_units, format_period)

**Why:** Every model inherits from base models, every app uses constants

---

### 2. organizations/ - Company Management
**Purpose:** Manage organization/company data
**Database Table:** organizations
**Key Fields:** name, industry, country, baseline_year
**API Endpoints:**
- GET /api/v1/organizations/ - List organizations
- GET /api/v1/organizations/{id}/ - Get organization details
- GET /api/v1/organizations/{id}/stats/ - Organization stats

**Why:** Multi-tenant system - all data belongs to an organization

---

### 3. facilities/ - Location Management
**Purpose:** Track emission sources by location (offices, plants, warehouses)
**Database Table:** facilities
**Key Fields:** name, city, country, grid_region
**API Endpoints:**
- GET/POST /api/v1/facilities/ - CRUD facilities
- GET /api/v1/facilities/{id}/emissions/ - Facility emissions

**Why:** Emissions vary by location (grid factors differ by region)

---

### 4. emission_factors/ - Calculation Library
**Purpose:** Store emission factors (kg CO2e per unit)
**Database Table:** emission_factors
**Key Fields:** scope, category, emission_factor_co2e, unit, region
**Example Data:**
- Diesel: 2.68 kg CO2e/liter
- Electricity (India): 0.92 kg CO2e/kWh
- Flight (Economy): 0.255 kg CO2e/km

**API Endpoints:**
- GET /api/v1/emission-factors/ - List factors
- POST /api/v1/emission-factors/search/ - Search factors

**Management Command:**
- python manage.py seed_emission_factors - Seed ~100 common factors

**Why:** This is the "brain" - without emission factors, no calculations possible

---

### 5. emissions/ - CORE MODULE
**Purpose:** Record all emission activities
**Database Tables:** emission_records, scope_details
**Key Fields:**
- scope, category, subcategory
- quantity, unit
- emission_factor_used, co2e_calculated
- activity_date, reporting_period

**Key Files:**
- models.py - EmissionRecord, ScopeDetails
- services.py - EmissionService (create_record, calculate_co2e)
- calculators.py - Calculation engine (FuelCalculator, ElectricityCalculator)
- serializers.py - API serializers
- views.py - API ViewSets

**API Endpoints:**
- GET/POST /api/v1/emissions/ - CRUD emissions
- POST /api/v1/emissions/bulk/ - Bulk create from CSV

**Calculation Flow:**
1. User enters: 100 liters of diesel
2. System finds emission factor: 2.68 kg CO2e/liter
3. Calculator: 100 × 2.68 = 268 kg CO2e
4. Save to database

**Why:** This is the HEART of the system - all emission data flows through here

---

### 6. analytics/ - Dashboard and Aggregations
**Purpose:** Pre-calculated summaries for fast dashboards
**Database Table:** emission_summary_monthly
**Key Fields:** organization, facility, reporting_period, scope, total_co2e

**Key Files:**
- models.py - EmissionSummaryMonthly
- services.py - AnalyticsService (calculate_summary, get_breakdown)
- views.py - Dashboard APIs

**API Endpoints:**
- GET /api/v1/analytics/dashboard/ - Main dashboard data
- GET /api/v1/analytics/trends/ - Time-series trends
- GET /api/v1/analytics/breakdown/ - Scope/category breakdown

**Why:** Avoid scanning millions of emission_records - query pre-calculated summaries instead

**Performance:**
- Without aggregations: Query 1M records = 5 seconds
- With aggregations: Query 12 summary rows = 50ms

---

### 7. uploads/ - File Processing
**Purpose:** Bulk CSV/Excel import
**Database Table:** uploaded_files

**Key Files:**
- models.py - UploadedFile
- services.py - UploadService (handle_upload, parse_csv)
- parsers/csv_parser.py - CSV parsing logic
- parsers/excel_parser.py - Excel parsing logic

**API Endpoints:**
- POST /api/v1/uploads/bulk-import/ - Upload CSV/Excel

**CSV Format Example:**
```csv
facility,scope,category,quantity,unit,activity_date
Mumbai Office,scope2,Electricity,1500,kWh,2024-01-15
Delhi Plant,scope1,Diesel,200,liter,2024-01-20
```

**Why:** Manual entry is slow - bulk upload enables importing 1000s of records

---

### 8. accounts/ (DEFER FOR MVP)
**Purpose:** User authentication, profiles, permissions
**Database Table:** users
**Why Defer:** MVP uses single user - add multi-user later

---

### 9. reporting/ (DEFER FOR MVP)
**Purpose:** Generate GHG Protocol, CDP reports
**Why Defer:** Focus on data collection first, reporting later

---

### 10. suppliers/ (DEFER FOR MVP)
**Purpose:** Scope 3 supplier engagement
**Why Defer:** Advanced Scope 3 feature

---

### 11. targets/ (DEFER FOR MVP)
**Purpose:** Track emission reduction goals
**Why Defer:** Nice-to-have, not core MVP

---

### 12. audit/ (DEFER FOR MVP)
**Purpose:** Compliance audit trail
**Why Defer:** Add when needed for compliance

---

## Frontend (Streamlit)

### frontend/app.py - Main Entry Point
**Purpose:** Streamlit app entry point
**Runs:** streamlit run app.py
**Contains:** Login page (if auth enabled), main navigation

---

### frontend/pages/ - Multi-Page App
**Purpose:** Separate pages for different features
**Naming Convention:** 1_Dashboard.py (number = order in sidebar)

**Pages:**
1. 1_Dashboard.py - Overview (metrics, charts)
2. 2_Add_Emissions.py - Manual data entry form
3. 3_View_Records.py - List all emission records
4. 4_Facilities.py - Manage facilities
5. 5_Analytics.py - Detailed charts and trends
6. 6_Upload_Data.py - Bulk CSV upload

---

### frontend/utils/api_client.py - API Wrapper
**Purpose:** Centralized API calls to Django backend
**Contains:**
```python
class APIClient:
    def get_dashboard_stats(self, period):
        # GET /api/v1/analytics/dashboard/
    
    def create_emission_record(self, data):
        # POST /api/v1/emissions/
    
    def upload_csv(self, file):
        # POST /api/v1/uploads/bulk-import/
```

**Why:** DRY - don't repeat API calls in every page

---

### frontend/utils/charts.py - Chart Generators
**Purpose:** Reusable Plotly chart functions
**Contains:**
- create_scope_pie_chart() - Scope 1/2/3 breakdown
- create_trend_chart() - Monthly trend line
- create_category_bar_chart() - Category comparison

---

### frontend/components/ - Reusable Components
**Purpose:** Streamlit UI components
**Contains:**
- metrics.py - Metric cards (total emissions, YoY change)
- data_tables.py - Styled dataframes
- filters.py - Date/scope/facility filters

---

## Database Tables (MVP - 6 Tables)

### 1. organizations
**Purpose:** Company/organization data
**Key Fields:** name, industry, country, baseline_year
**Relationships:** 1 org to many facilities, many emissions

---

### 2. facilities
**Purpose:** Emission source locations
**Key Fields:** name, city, country, grid_region
**Relationships:** 1 facility to many emissions

---

### 3. emission_factors
**Purpose:** Calculation library
**Key Fields:** scope, category, emission_factor_co2e, unit, region
**Rows:** ~100-200 common factors
**Relationships:** Referenced by emission_records

---

### 4. emission_records - CORE TABLE
**Purpose:** All emission activities
**Key Fields:**
- scope, category, quantity, unit
- emission_factor_used, co2e_calculated
- activity_date, reporting_period
**Relationships:** Many records to 1 facility, 1 emission_factor

---

### 5. scope_details
**Purpose:** Flexible extra data (JSONB)
**Key Fields:** emission_record_id, details (JSONB)
**Example JSONB:**
```json
{
  "type": "electricity",
  "utility_provider": "State Grid",
  "meter_number": "M-789"
}
```
**Why:** Avoids 7 separate scope-specific tables

---

### 6. emission_summary_monthly
**Purpose:** Pre-calculated aggregations
**Key Fields:** organization, facility, period, scope, total_co2e
**Why:** Fast dashboard queries

---

## Key Design Patterns

### 1. Service Layer Pattern
**What:** Business logic in services, not views
**Example:**
```python
# Logic in view (NOT RECOMMENDED)
class EmissionViewSet:
    def create(self, request):
        # 50 lines of calculation logic...

# Logic in service (RECOMMENDED)
class EmissionViewSet:
    def create(self, request):
        record = EmissionService.create_record(data, user)
        return Response(record)
```

---

### 2. Calculator Pattern
**What:** Separate calculator class for each emission type
**Example:**
```python
class FuelCombustionCalculator:
    def calculate(self, liters, ef):
        return liters * ef

class ElectricityCalculator:
    def calculate(self, kwh, grid_factor):
        return kwh * grid_factor
```

---

### 3. Aggregation Strategy
**What:** Pre-calculate summaries, don't query raw records
**Flow:**
1. User creates emission record
2. Trigger: Update monthly summary
3. Dashboard: Query summary table (fast!)

---

## Data Flow Example

### User uploads CSV with 1000 emission records:

1. Upload to POST /api/v1/uploads/bulk-import/
2. Parse via UploadService.parse_csv()
3. Validate - Check all rows have required fields
4. Create Records - Loop through rows:
   - Get emission factor
   - Calculate CO2e
   - Create EmissionRecord
5. Update Aggregations - Recalculate monthly summaries
6. Dashboard - Query summaries, show updated charts

**Time:** ~5 seconds for 1000 records

---

## MVP Development Order

### Phase 1: Backend Foundation (Day 1 - 4 hours)
1. Django setup (django-admin startproject)
2. Create 6 models
3. Run migrations
4. Seed emission factors

### Phase 2: Core API (Day 1 - 4 hours)
5. Emission recording API
6. Calculators
7. Analytics API
8. Test with Postman

### Phase 3: Frontend (Day 2 - 4 hours)
9. Streamlit dashboard
10. Manual entry form
11. CSV upload
12. Charts

---

## Next Steps

1. Directory structure created
2. Create requirements.txt
3. Initialize Django project
4. Create models
5. Build API
6. Build frontend

---

Ready to start coding!
