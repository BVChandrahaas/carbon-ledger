from .parsers.csv_parser import CSVParser
from apps.emissions.services import EmissionService
from django.db import transaction


class UploadService:
    """
    Coordinates file processing and ingestion.
    """
    
    @staticmethod
    def process_bulk_upload(upload_obj):
        """
        Synchronous processing for MVP.
        In production, this should be a Celery task.
        """
        upload_obj.processing_status = 'processing'
        upload_obj.save()
        
        try:
            # 1. Parse file
            records_data = CSVParser.parse(upload_obj.file.path)
            
            # 2. Bulk create using EmissionService
            with transaction.atomic():
                created_records = EmissionService.bulk_create_records(
                    records_list=records_data,
                    organization=upload_obj.organization,
                    user=upload_obj.uploaded_by
                )
                
            # 3. Update status
            upload_obj.processing_status = 'completed'
            upload_obj.records_created = len(created_records)
            upload_obj.save()
            
            return created_records
            
        except Exception as e:
            upload_obj.processing_status = 'failed'
            upload_obj.error_message = str(e)
            upload_obj.save()
            raise e
