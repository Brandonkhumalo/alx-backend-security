from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
from django.utils.timezone import now
from ip2geotools.databases.noncommercial import DbIpCity
from django.core.cache import cache

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)

        # Block blacklisted IPs
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # Try to get geolocation from cache
        cache_key = f"geo:{ip_address}"
        geo = cache.get(cache_key)

        if not geo:
            try:
                response = DbIpCity.get(ip_address, api_key='free')
                geo = {
                    'country': response.country,
                    'city': response.city
                }
                # Cache for 24 hours
                cache.set(cache_key, geo, 60 * 60 * 24)
            except Exception:
                geo = {'country': None, 'city': None}

        # Log request
        RequestLog.objects.create(
            ip_address=ip_address,
            timestamp=now(),
            path=request.path,
            country=geo['country'],
            city=geo['city']
        )

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
