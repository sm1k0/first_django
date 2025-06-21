import requests
from django.conf import settings

def api_request(method, endpoint, request, data=None):
    url = f"{settings.API_BASE_URL}/{endpoint.lstrip('/')}"
    headers = {}
    token = request.session.get('api_token')
    if token:
        headers['Authorization'] = f"Token {token}"
    print(f"API request: {method} {url}, Data: {data}, Headers: {headers}, Session token: {token}")
    try:
        response = requests.request(method, url, headers=headers, json=data, timeout=5)
        print(f"API response: {response.status_code} {response.text}")
        response.raise_for_status()
        return response.json() if response.content else None
    except requests.Timeout:
        print(f"API request failed: Timeout for {method} {url}")
        return None
    except requests.HTTPError as e:
        print(f"API request failed: HTTPError {e.response.status_code} {e.response.text}")
        return None
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None