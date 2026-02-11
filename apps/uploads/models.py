"""
UploadedFile model - tracks bulk import files.
"""

from django.db import models
from apps.core.models import BaseModel


class UploadedFile(BaseModel):
    """
    Tracks and manages evidence and bulk upload files.
    """
    organization = models.ForeignKey(
        'organizations.Organization', 
        on_delete=models.CASCADE, 
        related_name='uploads'
    )
    
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(
        max_length=50, 
        choices=[('bulk_upload', 'Bulk Data Import'), ('evidence', 'Evidence Support')],
        default='bulk_upload'
    )
    
    processing_status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='pending'
    )
    
    records_created = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    
    uploaded_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True
    )

    class Meta:
        db_table = 'uploaded_files'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.file_name} - {self.processing_status}"
