from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

API_AUTH_TOKEN = "MTEyMzQ1cmRzZ2hobjBvaTQzMw=="

class StaticTokenAuthentication(BaseAuthentication):
    """
    Custom authentication using a fixed API token.
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise exceptions.AuthenticationFailed("Missing Authorization header")

        # Expected format: Bearer <token>
        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise exceptions.AuthenticationFailed("Invalid token format")

        token = parts[1]

        if token != API_AUTH_TOKEN:
            raise exceptions.AuthenticationFailed("Invalid token")

        # Return a dummy user (DRF requires a user, can be Anonymous)
        return (None, None)
