from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import UploadedFile
from .serializers import UploadedFileSerializer
from .services import UploadService


class UploadedFileViewSet(viewsets.ModelViewSet):
    """
    API endpoints for file uploads.
    """
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def get_queryset(self):
        org_id = self.request.query_params.get('organization')
        if org_id:
            return self.queryset.filter(organization_id=org_id)
        return self.queryset

    def perform_create(self, serializer):
        """
        Hook to trigger processing after upload.
        """
        instance = serializer.save()
        
        # Trigger processing if it's a bulk upload
        if instance.file_type == 'bulk_upload':
            try:
                UploadService.process_bulk_upload(instance)
            except Exception:
                # We handle the error inside the service, 
                # but we let the view know something happened if needed
                pass
