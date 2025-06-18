import requests
from django.conf import settings

def api_request(method, endpoint, request, data=None):
    url = f"{settings.API_BASE_URL}/{endpoint.lstrip('/')}"
    headers = {}
    if request.session.get('api_token'):
        headers['Authorization'] = f"Token {request.session['api_token']}"
    try:
        response = requests.request(method, url, headers=headers, json=data)
        response.raise_for_status()
        return response.json() if response.content else None
    except requests.RequestException as e:
        print(f"API request failed: {e}")  # Debug line
        return None