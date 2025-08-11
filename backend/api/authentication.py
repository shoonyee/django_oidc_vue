from rest_framework.authentication import SessionAuthentication

class NoCSRFSessionAuthentication(SessionAuthentication):
    """
    Custom session authentication that bypasses CSRF for local development
    """
    def enforce_csrf(self, request):
        # Skip CSRF enforcement for local development
        return None
