from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import AnalyticsService
from apps.organizations.models import Organization


class DashboardOverviewView(APIView):
    """
    API view to get high-level dashboard data.
    """
    def get(self, request):
        org_id = request.query_params.get('organization')
        period = request.query_params.get('period')
        
        if not org_id:
            return Response({'error': 'Organization ID required'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            organization = Organization.objects.get(id=org_id)
            # Ensure summaries are fresh for MVP (Simple trigger)
            AnalyticsService.calculate_monthly_summary(organization, period)
            
            data = AnalyticsService.get_dashboard_data(organization, period)
            return Response(data)
        except Organization.DoesNotExist:
            return Response({'error': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
