# Carbon Accounting Platform - MVP

A comprehensive carbon accounting system for tracking, calculating, and reporting greenhouse gas emissions across Scope 1, 2, and 3.

---

## PROJECT STRUCTURE

```
carbon_accounting/                    # PROJECT ROOT
|
|-- README.md                         # This file - project documentation
|-- requirements.txt                  # Python dependencies (Django, DRF, pandas, etc.)
|-- .gitignore                        # Git ignore file
|-- .env.example                      # Environment variables template
|-- manage.py                         # Django management script
|
|-- config/                           # DJANGO PROJECT CONFIGURATION
|   |                                 # PURPOSE: Centralized settings, URLs, WSGI/ASGI
|   |                                 # WHY: Separates config from business logic
|   |
|   |-- __init__.py                   # Makes this a Python package
|   |
|   |-- settings/                     # SPLIT SETTINGS (different environments)
|   |   |                             # WHY: Dev uses SQLite, Prod uses PostgreSQL
|   |   |-- __init__.py
|   |   |-- base.py                   # Common settings (all environments)
|   |   |                             # CONTAINS:
|   |   |                             #   - INSTALLED_APPS (Django apps, DRF, CORS)
|   |   |                             #   - MIDDLEWARE
|   |   |                             #   - TEMPLATES config
|   |   |                             #   - REST_FRAMEWORK config
|   |   |                             #   - STATIC_URL, MEDIA_URL
|   |   |
|   |   |-- local.py                  # Development settings
|   |   |                             # CONTAINS:
|   |   |                             #   - DEBUG = True
|   |   |                             #   - SQLite database
|   |   |                             #   - CORS_ALLOW_ALL_ORIGINS = True
|   |   |                             #   - Relaxed security
|   |   |
|   |   '-- production.py             # Production settings
|   |                                 # CONTAINS:
|   |                                 #   - DEBUG = False
|   |                                 #   - PostgreSQL database
|   |                                 #   - Strict CORS
|   |                                 #   - Security headers
|   |
|   |-- urls.py                       # ROOT URL CONFIGURATION
|   |                                 # PURPOSE: Maps URLs to app views
|   |                                 # CONTAINS:
|   |                                 #   - /api/v1/ -> app URLs
|   |                                 #   - /admin/ -> Django admin
|   |
|   |-- wsgi.py                       # WSGI entry point (production servers)
|   |                                 # PURPOSE: Gunicorn/uWSGI use this
|   |
|   '-- asgi.py                       # ASGI entry point (async/WebSockets)
|                                     # PURPOSE: Future real-time features
|
|-- apps/                             # DJANGO APPLICATIONS (modular architecture)
|   |                                 # WHY: Each app = one business domain
|   |                                 # BENEFIT: Reusable, testable, maintainable
|   |
|   |-- __init__.py
|   |
|   |-- core/                         # SHARED UTILITIES (no models, just helpers)
|   |   |                             # PURPOSE: DRY - Don't Repeat Yourself
|   |   |                             # USED BY: All other apps
|   |   |-- __init__.py
|   |   |-- models.py                 # ABSTRACT BASE MODELS
|   |   |                             # CONTAINS:
|   |   |                             #   - TimeStampedModel (created_at, updated_at)
|   |   |                             #   - SoftDeleteModel (deleted_at field)
|   |   |                             #   - UUIDModel (UUID primary key)
|   |   |                             # WHY: All models inherit these (DRY)
|   |   |
|   |   |-- managers.py               # CUSTOM QUERYSETS
|   |   |                             # CONTAINS:
|   |   |                             #   - SoftDeleteManager (alive(), deleted())
|   |   |                             #   - OrganizationQuerySet (for_user())
|   |   |                             # WHY: Reusable query logic
|   |   |
|   |   |-- mixins.py                 # REUSABLE VIEW/MODEL MIXINS
|   |   |                             # CONTAINS:
|   |   |                             #   - OrganizationFilterMixin
|   |   |                             # WHY: DRY for common view patterns
|   |   |
|   |   |-- validators.py             # CUSTOM VALIDATORS
|   |   |                             # CONTAINS:
|   |   |                             #   - validate_positive_decimal()
|   |   |                             #   - validate_year_range()
|   |   |
|   |   |-- constants.py              # GLOBAL CONSTANTS
|   |   |                             # CONTAINS:
|   |   |                             #   - SCOPE_CHOICES = [('scope1', 'Scope 1'), ...]
|   |   |                             #   - STATUS_CHOICES, ROLE_CHOICES
|   |   |                             # WHY: Single source of truth
|   |   |
|   |   |-- exceptions.py             # CUSTOM EXCEPTIONS
|   |   |                             # CONTAINS:
|   |   |                             #   - EmissionCalculationError
|   |   |                             #   - InvalidEmissionFactorError
|   |   |
|   |   '-- utils.py                  # HELPER FUNCTIONS
|   |                                 # CONTAINS:
|   |                                 #   - convert_units()
|   |                                 #   - format_period()
|   |
|   |-- organizations/                # ORGANIZATION MANAGEMENT
|   |   |                             # PURPOSE: Manage company/organization data
|   |   |                             # DATABASE TABLE: organizations
|   |   |                             # FIELDS: name, industry, country, baseline_year
|   |   |-- __init__.py
|   |   |-- models.py                 # Organization model
|   |   |-- serializers.py            # DRF serializers (JSON <-> Model)
|   |   |-- views.py                  # API ViewSets
|   |   |-- services.py               # Business logic layer
|   |   |-- urls.py                   # URL routing
|   |   |-- admin.py                  # Django admin config
|   |   |-- apps.py                   # App configuration
|   |   '-- tests.py                  # Unit tests
|   |
|   |-- accounts/                     # USER MANAGEMENT (DEFER FOR MVP)
|   |   |                             # PURPOSE: Authentication, user profiles
|   |   |                             # DATABASE TABLE: users
|   |   |                             # MVP: Skip for now (single user)
|   |   |-- __init__.py
|   |   |-- models.py                 # User model (extends AbstractUser)
|   |   |-- serializers.py            # UserSerializer, LoginSerializer
|   |   |-- views.py                  # Login, Register, Profile APIs
|   |   |-- permissions.py            # IsOrgAdmin, CanVerifyRecords
|   |   |-- urls.py
|   |   '-- tests.py
|   |
|   |-- facilities/                   # FACILITY/LOCATION MANAGEMENT
|   |   |                             # PURPOSE: Track emission sources by location
|   |   |                             # DATABASE TABLE: facilities
|   |   |                             # FIELDS: name, city, country, grid_region
|   |   |                             # WHY grid_region: Electricity factors vary by region
|   |   |-- __init__.py
|   |   |-- models.py                 # Facility model
|   |   |-- serializers.py            # FacilitySerializer
|   |   |-- views.py                  # FacilityViewSet (CRUD)
|   |   |-- services.py               # FacilityService (geocoding, grid assignment)
|   |   |-- urls.py
|   |   |-- admin.py
|   |   '-- tests.py
|   |
|   |-- emission_factors/             # EMISSION FACTOR LIBRARY
|   |   |                             # PURPOSE: Store calculation factors (kg CO2e per unit)
|   |   |                             # DATABASE TABLE: emission_factors
|   |   |                             # CRITICAL: This is the brain of calculations
|   |   |                             # EXAMPLE: Diesel = 2.68 kg CO2e/liter
|   |   |-- __init__.py
|   |   |-- models.py                 # EmissionFactor model
|   |   |-- serializers.py            # EmissionFactorSerializer
|   |   |-- views.py                  # EmissionFactorViewSet
|   |   |-- services.py               # EmissionFactorService (search, get_factor)
|   |   |-- management/               # Django management commands
|   |   |   |-- __init__.py
|   |   |   '-- commands/
|   |   |       |-- __init__.py
|   |   |       '-- seed_emission_factors.py  # Seed initial data
|   |   |                             # RUNS: python manage.py seed_emission_factors
|   |   |-- urls.py
|   |   |-- admin.py
|   |   '-- tests.py
|   |
|   |-- emissions/                    # CORE: EMISSION RECORDING
|   |   |                             # PURPOSE: Record all emission activities
|   |   |                             # DATABASE TABLES: emission_records, scope_details
|   |   |                             # THIS IS THE HEART OF THE SYSTEM
|   |   |-- __init__.py
|   |   |-- models.py                 # EmissionRecord, ScopeDetails models
|   |   |                             # EmissionRecord FIELDS:
|   |   |                             #   - scope, category, quantity, unit
|   |   |                             #   - emission_factor_used, co2e_calculated
|   |   |                             #   - activity_date, reporting_period
|   |   |                             # ScopeDetails: JSONB for flexible extra data
|   |   |
|   |   |-- serializers.py            # Multiple serializers
|   |   |                             #   - EmissionRecordSerializer (list)
|   |   |                             #   - EmissionRecordCreateSerializer (create)
|   |   |                             #   - EmissionRecordDetailSerializer (detail)
|   |   |
|   |   |-- views.py                  # API ViewSets
|   |   |                             # ENDPOINTS:
|   |   |                             #   - GET/POST /api/v1/emissions/
|   |   |                             #   - POST /api/v1/emissions/bulk/
|   |   |
|   |   |-- services.py               # EMISSION SERVICE (CRITICAL!)
|   |   |                             # CONTAINS:
|   |   |                             #   - create_emission_record()
|   |   |                             #   - bulk_create_records()
|   |   |                             #   - calculate_co2e()
|   |   |                             # WHY: All business logic here (not in views)
|   |   |
|   |   |-- calculators.py            # CALCULATION ENGINE
|   |   |                             # CONTAINS:
|   |   |                             #   - BaseCalculator (abstract)
|   |   |                             #   - FuelCombustionCalculator
|   |   |                             #   - ElectricityCalculator
|   |   |                             #   - TravelCalculator
|   |   |                             # WHY: Encapsulate calculation logic
|   |   |
|   |   |-- validators.py             # Validation logic
|   |   |-- signals.py                # Django signals (DEFER FOR MVP)
|   |   |-- urls.py
|   |   '-- tests.py
|   |
|   |-- analytics/                    # AGGREGATIONS AND DASHBOARD DATA
|   |   |                             # PURPOSE: Pre-calculated summaries for performance
|   |   |                             # DATABASE TABLE: emission_summary_monthly
|   |   |                             # WHY: Avoid scanning millions of records
|   |   |-- __init__.py
|   |   |-- models.py                 # EmissionSummaryMonthly model
|   |   |-- serializers.py            # DashboardSerializer, TrendsSerializer
|   |   |-- views.py                  # Analytics API views
|   |   |                             # ENDPOINTS:
|   |   |                             #   - GET /api/v1/analytics/dashboard/
|   |   |                             #   - GET /api/v1/analytics/trends/
|   |   |                             #   - GET /api/v1/analytics/breakdown/
|   |   |
|   |   |-- services.py               # AnalyticsService
|   |   |                             # CONTAINS:
|   |   |                             #   - calculate_monthly_summary()
|   |   |                             #   - get_scope_breakdown()
|   |   |
|   |   |-- tasks.py                  # Celery tasks (DEFER FOR MVP)
|   |   |-- urls.py
|   |   '-- tests.py
|   |
|   |-- uploads/                      # FILE UPLOAD HANDLING
|   |   |                             # PURPOSE: Bulk CSV/Excel import
|   |   |                             # DATABASE TABLE: uploaded_files
|   |   |-- __init__.py
|   |   |-- models.py                 # UploadedFile model
|   |   |-- serializers.py            # FileUploadSerializer
|   |   |-- views.py                  # Upload API views
|   |   |                             # ENDPOINTS:
|   |   |                             #   - POST /api/v1/uploads/bulk-import/
|   |   |
|   |   |-- services.py               # UploadService
|   |   |                             # CONTAINS:
|   |   |                             #   - handle_file_upload()
|   |   |                             #   - parse_csv()
|   |   |
|   |   |-- parsers/                  # File format parsers
|   |   |   |-- __init__.py
|   |   |   |-- base.py               # BaseParser (abstract)
|   |   |   |-- csv_parser.py         # CSV parsing logic
|   |   |   '-- excel_parser.py       # Excel parsing logic
|   |   |
|   |   |-- validators.py             # validate_csv_structure()
|   |   |-- urls.py
|   |   '-- tests.py
|   |
|   |-- reporting/                    # REPORT GENERATION (DEFER FOR MVP)
|   |   |                             # PURPOSE: Generate GHG Protocol, CDP reports
|   |   |                             # DATABASE TABLE: reports
|   |   '-- ...                       # (Skip for MVP)
|   |
|   |-- suppliers/                    # SUPPLIER MANAGEMENT (DEFER FOR MVP)
|   |   |                             # PURPOSE: Scope 3 supplier engagement
|   |   '-- ...                       # (Skip for MVP)
|   |
|   |-- targets/                      # REDUCTION TARGETS (DEFER FOR MVP)
|   |   |                             # PURPOSE: Track emission reduction goals
|   |   '-- ...                       # (Skip for MVP)
|   |
|   '-- audit/                        # AUDIT LOGGING (DEFER FOR MVP)
|       |                             # PURPOSE: Compliance audit trail
|       '-- ...                       # (Skip for MVP)
|
|-- static/                           # STATIC FILES (CSS, JS, images)
|   |                                 # PURPOSE: Django collectstatic for production
|   |-- css/                          # Custom stylesheets
|   |-- js/                           # Custom JavaScript
|   '-- images/                       # Static images (logos, icons)
|
|-- media/                            # USER UPLOADS (local dev only)
|   |                                 # PURPOSE: Store uploaded files locally
|   |                                 # PRODUCTION: Use S3
|   '-- uploads/                      # Uploaded CSV/Excel files
|
|-- templates/                        # DJANGO TEMPLATES
|   |                                 # PURPOSE: Django admin customization, emails
|   '-- admin/                        # Custom admin templates
|
|-- tests/                            # TEST SUITE (DEFER FOR MVP)
|   |                                 # PURPOSE: Centralized testing
|   |-- conftest.py                   # Pytest fixtures
|   |-- test_emissions.py             # Emission tests
|   |-- test_calculations.py          # Calculator tests
|   '-- test_api.py                   # API endpoint tests
|
|-- frontend/                         # STREAMLIT FRONTEND
|   |                                 # PURPOSE: User interface for MVP
|   |                                 # WHY: Separate from Django backend
|   |
|   |-- app.py                        # MAIN STREAMLIT ENTRY POINT
|   |                                 # RUNS: streamlit run app.py
|   |                                 # CONTAINS: Login page, main dashboard
|   |
|   |-- pages/                        # MULTI-PAGE STREAMLIT APP
|   |   |                             # WHY: Streamlit auto-creates sidebar navigation
|   |   |                             # FILE NAMING: 1_Dashboard.py (number = order)
|   |   |-- 1_Dashboard.py            # Overview dashboard (charts, metrics)
|   |   |-- 2_Add_Emissions.py        # Manual data entry form
|   |   |-- 3_Bulk_Upload.py          # Bulk CSV upload
|   |   '-- 4_Settings.py             # Manage settings
|   |
|   |-- utils/                        # FRONTEND UTILITIES
|   |   |-- api_client.py             # Django API wrapper
|   |   |                             # CONTAINS: APIClient class (requests wrapper)
|   |   |                             # METHODS: get_dashboard(), create_emission(), etc.
|   |   |
|   |   |-- auth.py                   # Login/logout (DEFER FOR MVP)
|   |   |-- charts.py                 # Plotly chart generators
|   |   |                             # CONTAINS:
|   |   |                             #   - create_scope_pie_chart()
|   |   |                             #   - create_trend_chart()
|   |   |
|   |   '-- formatters.py             # Data formatting utilities
|   |                                 # CONTAINS:
|   |                                 #   - format_number()
|   |                                 #   - format_date()
|   |
|   |-- components/                   # REUSABLE STREAMLIT COMPONENTS
|   |   |-- metrics.py                # Metric cards (st.metric wrappers)
|   |   |-- data_tables.py            # Styled dataframes
|   |   '-- filters.py                # Filter widgets (date, scope, facility)
|   |
|   |-- config.py                     # Frontend config
|   |                                 # CONTAINS:
|   |                                 #   - API_BASE_URL = "http://localhost:8000/api/v1"
|   |
|   '-- requirements.txt              # Frontend dependencies
|                                     # CONTAINS: streamlit, plotly, requests, pandas
|
|-- scripts/                          # UTILITY SCRIPTS
|   |                                 # PURPOSE: Automation, data migration
|   |-- seed_data.py                  # Seed sample data for testing
|   '-- reset_db.py                   # Reset database (delete + recreate)
|
'-- docs/                             # DOCUMENTATION (DEFER FOR MVP)
    |-- api.md                        # API documentation
    |-- setup.md                      # Setup guide
    '-- architecture.md               # Architecture overview
```

---

## MVP PRIORITY (What to Build First)

### MUST CREATE NOW (Day 1-1.5)

#### Backend (Django):
1. config/ - Settings and URLs
2. apps/core/ - Base models and constants
3. apps/organizations/ - Organization model
4. apps/facilities/ - Facility model
5. apps/emission_factors/ - Emission factor library + seed command
6. apps/emissions/ - Emission recording (models, services, calculators)
7. apps/analytics/ - Dashboard aggregations
8. apps/uploads/ - CSV bulk upload

#### Frontend (Streamlit):
1. app.py - Main entry point
2. pages/1_Dashboard.py - Overview dashboard
3. pages/2_Add_Emissions.py - Manual data entry
4. pages/3_Bulk_Upload.py - Bulk CSV upload
5. utils/api_client.py - API wrapper

### DEFER TO LATER (v2)
- accounts/ - Authentication (use single user for MVP)
- reporting/ - Report generation
- suppliers/ - Supplier management
- targets/ - Reduction targets
- audit/ - Audit logging
- tests/ - Unit tests
- Celery tasks (use synchronous for MVP)

---

## DATABASE (MVP)

### For MVP: SQLite
- Zero setup (built into Python)
- File-based (easy to reset)
- Perfect for development

### 6 Core Tables:
1. organizations - Company data
2. facilities - Locations
3. emission_factors - Calculation library (~100 rows)
4. emission_records - Core transaction data
5. scope_details - Flexible JSONB extra data
6. emission_summary_monthly - Pre-calculated aggregations

### When to Switch to PostgreSQL:
- Production deployment
- Need JSONB queries
- Multiple concurrent users

---

## QUICK START (After Setup)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py makemigrations
python manage.py migrate

# 3. Seed emission factors
python manage.py seed_emission_factors

# 4. Create superuser (optional)
python manage.py createsuperuser

# 5. Run Django server
python manage.py runserver

# 6. Run Streamlit (separate terminal)
cd frontend
streamlit run app.py
```

---

## KEY CONCEPTS

### 1. Service Layer Pattern
- Views = HTTP handling only (thin)
- Services = Business logic (create_emission_record, calculate_co2e)
- Models = Data structure only

### 2. Calculator Pattern
- Each emission type has a calculator class
- FuelCombustionCalculator, ElectricityCalculator, etc.
- Encapsulates calculation logic

### 3. Aggregation Strategy
- Pre-calculate monthly summaries
- Avoid scanning millions of records
- Fast dashboard loads

### 4. JSONB Flexibility
- scope_details table uses JSONB
- Avoids 7 separate scope-specific tables
- Easy to add new fields without migrations

---

## ARCHITECTURE DECISIONS

| Decision | Choice | Why |
|----------|--------|-----|
| Database (MVP) | SQLite | Zero setup, easy dev |
| Database (Prod) | PostgreSQL | JSONB, scalability |
| API Framework | Django REST Framework | Mature, well-documented |
| Auth (MVP) | Skip | Single user for speed |
| Auth (Prod) | JWT | Stateless, scalable |
| Tasks (MVP) | Synchronous | Simpler for MVP |
| Tasks (Prod) | Celery + Redis | Async processing |
| File Storage (MVP) | Local files | Simple |
| File Storage (Prod) | S3 | Scalable, cheap |
| Frontend (MVP) | Streamlit | Rapid prototyping |
| Frontend (Prod) | React/Next.js | Better UX |

---

## NEXT STEPS

1. Directory structure created (you're here!)
2. Create requirements.txt (dependencies)
3. Initialize Django project (django-admin startproject)
4. Create models (6 core tables)
5. Seed emission factors (~100 rows)
6. Build API endpoints (DRF ViewSets)
7. Create Streamlit dashboard (3 pages)
8. Test end-to-end (upload CSV, view dashboard)

---

## MVP TIMELINE (1.5 Days)

### Day 1 (8 hours):
- Django setup + models (4 hours)
- API endpoints (2 hours)
- Seed data (1 hour)
- Test API (1 hour)

### Day 2 (4 hours):
- Streamlit dashboard (2 hours)
- Upload CSV (1 hour)
- Charts (1 hour)

---

## RESOURCES

- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Streamlit Docs: https://docs.streamlit.io/
- GHG Protocol: https://ghgprotocol.org/

---

## CONTRIBUTING

This is an MVP. Focus on:
1. Working code over perfect code
2. Core features over nice-to-haves
3. Speed over optimization

Refactor later based on real usage!

---

Built for carbon accounting
