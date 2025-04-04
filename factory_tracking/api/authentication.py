from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import ApiKey

class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        key = request.headers.get('X-API-KEY')
        if not key:
            raise AuthenticationFailed("API key missing")
        try:
            api_key = ApiKey.objects.get(key=key)
        except ApiKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")
        return (api_key.owner, None)
