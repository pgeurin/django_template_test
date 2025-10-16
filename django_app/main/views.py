from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.sites.models import Site
import json

def home(request):
    """Home page view."""
    return render(request, 'main/home.html', {
        'django_version': '5.2.6',  # Hardcoded for simplicity
    })

def debug_oauth(request):
    """Debug view for OAuth configuration."""
    site = Site.objects.get_current()
    callback_url = f"http://{site.domain}/accounts/google/login/callback/"
    
    # Get query parameters from request
    query_params = {k: v for k, v in request.GET.items()}
    
    # Get headers from request
    headers = {k: v for k, v in request.headers.items()}
    
    return JsonResponse({
        'site_domain': site.domain,
        'site_name': site.name,
        'callback_url': callback_url,
        'request_path': request.path,
        'request_host': request.get_host(),
        'query_params': query_params,
        'headers': headers,
    })

@require_http_methods(["GET"])
def api_example(request):
    """Public API example endpoint."""
    response_data = {
        'status': 'success',
        'message': 'This is an example API endpoint',
        'data': {
            'items': ['item1', 'item2', 'item3'],
            'count': 3
        }
    }
    return JsonResponse(response_data)

@login_required
@require_http_methods(["GET", "POST"])
def api_protected(request):
    """Protected API endpoint that requires authentication."""
    if request.method == 'GET':
        response_data = {
            'status': 'success',
            'message': 'You are authenticated!',
            'user': {
                'email': request.user.email,
                'id': request.user.id
            }
        }
        return JsonResponse(response_data)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            response_data = {
                'status': 'success',
                'message': 'Data received successfully',
                'received': data
            }
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)