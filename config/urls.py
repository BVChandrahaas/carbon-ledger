"""
URL configuration for carbon_accounting project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'name': 'Carbon Accounting API',
        'version': 'v1.0',
        'status': 'active',
        'endpoints': {
            'organizations': '/api/v1/organizations/',
            'facilities': '/api/v1/facilities/',
            'emissions': '/api/v1/emissions/',
            'emission_factors': '/api/v1/emission-factors/',
            'analytics': '/api/v1/analytics/dashboard/',
            'uploads': '/api/v1/uploads/',
        }
    })

urlpatterns = [
    # Admin
    path('admin/', admin.site.admin_view),
    
    # API v1
    path('api/v1/', include([
        path('', api_root, name='api-root'),
        path('organizations/', include('apps.organizations.urls')),
        path('facilities/', include('apps.facilities.urls')),
        path('emission-factors/', include('apps.emission_factors.urls')),
        path('emissions/', include('apps.emissions.urls')),
        path('analytics/', include('apps.analytics.urls')),
        path('uploads/', include('apps.uploads.urls')),
    ])),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
