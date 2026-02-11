import pandas as pd
from datetime import datetime
from apps.emissions.services import EmissionService


class CSVParser:
    """
    Parses CSV files into emission records.
    """
    
    EXPECTED_COLUMNS = [
        'facility_id', 'scope', 'category', 'subcategory', 
        'quantity', 'unit', 'emission_factor_used', 
        'activity_date', 'notes'
    ]

    @staticmethod
    def parse(file_path):
        """
        Reads CSV and returns a list of dictionaries.
        """
        df = pd.read_csv(file_path)
        
        # Basic validation of columns
        for col in CSVParser.EXPECTED_COLUMNS:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        records = df.to_dict('records')
        
        # Clean data types
        for record in records:
            # Convert NaN to empty string for subcategory/notes
            for key in ['subcategory', 'notes']:
                if pd.isna(record.get(key)):
                    record[key] = ''
            
            # Ensure date is properly formatted
            if isinstance(record['activity_date'], str):
                record['activity_date'] = datetime.strptime(record['activity_date'], '%Y-%m-%d').date()
                
        return records
