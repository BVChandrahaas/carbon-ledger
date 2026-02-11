import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

class APIClient:
    """
    Client for interacting with the Carbon Accounting API.
    """
    def __init__(self, base_url=None):
        self.base_url = base_url or os.getenv('API_BASE_URL', 'http://localhost:8000/api/v1')

    def _get(self, endpoint, params=None):
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint, data=None, files=None):
        response = requests.post(f"{self.base_url}/{endpoint}", json=data, files=files)
        response.raise_for_status()
        return response.json()

    # --- Organizations ---
    def get_organizations(self):
        return self._get('organizations/')

    def get_organization_stats(self, org_id):
        return self._get(f'organizations/{org_id}/stats/')

    # --- Facilities ---
    def get_facilities(self, org_id=None):
        params = {'organization': org_id} if org_id else {}
        return self._get('facilities/', params=params)

    # --- Emission Factors ---
    def get_emission_factors(self, scope=None, category=None):
        params = {}
        if scope: params['scope'] = scope
        if category: params['category'] = category
        return self._get('emission-factors/', params=params)

    # --- Emissions ---
    def get_emission_records(self, org_id=None):
        params = {'organization': org_id} if org_id else {}
        return self._get('emissions/', params=params)

    def create_emission_record(self, data):
        return self._post('emissions/', data=data)

    # --- Analytics ---
    def get_dashboard_stats(self, org_id, period=None):
        params = {'organization': org_id}
        if period: params['period'] = period
        return self._get('analytics/dashboard/', params=params)

    # --- Uploads ---
    def upload_bulk_csv(self, org_id, file):
        files = {'file': file}
        data = {'organization': org_id, 'file_type': 'bulk_upload'}
        # Note: requests uses different format for multipart/form-data
        response = requests.post(
            f"{self.base_url}/uploads/", 
            files=files, 
            data=data
        )
        response.raise_for_status()
        return response.json()
