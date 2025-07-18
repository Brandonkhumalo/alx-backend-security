from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema setup
schema_view = get_schema_view(
    openapi.Info(
        title="IP Tracking & Security API",
        default_version='v1',
        description="API documentation for IP tracking, rate limiting, geolocation, and anomaly detection.",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,  # Makes it accessible without authentication
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('ip_tracking/', include('ip_tracking.urls')),

    # Swagger documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
