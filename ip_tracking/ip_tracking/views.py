from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse
from ratelimit.decorators import ratelimit

# 10 requests/min for authenticated users
@ratelimit(key='ip', rate='10/m', method='POST', block=True)
# 5 requests/min for anonymous users
@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def login_view(request):
    if request.method == 'POST':
        # Dummy response for now
        return JsonResponse({"message": "Login attempt received."})
    return JsonResponse({"error": "Only POST allowed."}, status=405)