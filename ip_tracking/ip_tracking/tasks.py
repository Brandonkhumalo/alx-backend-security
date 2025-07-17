from celery import shared_task
from django.utils.timezone import now, timedelta
from .models import RequestLog, SuspiciousIP

SENSITIVE_PATHS = ['/admin', '/login']

@shared_task
def detect_suspicious_ips():
    one_hour_ago = now() - timedelta(hours=1)
    logs = RequestLog.objects.filter(timestamp__gte=one_hour_ago)

    # Count requests per IP
    ip_counts = {}
    for log in logs:
        ip_counts[log.ip_address] = ip_counts.get(log.ip_address, 0) + 1

    for ip, count in ip_counts.items():
        if count > 100:
            SuspiciousIP.objects.get_or_create(
                ip_address=ip,
                defaults={'reason': f'High request volume: {count} requests in the past hour'}
            )

    # Check for sensitive path access
    for log in logs:
        if any(log.path.startswith(p) for p in SENSITIVE_PATHS):
            SuspiciousIP.objects.get_or_create(
                ip_address=log.ip_address,
                defaults={'reason': f'Accessed sensitive path: {log.path}'}
            )