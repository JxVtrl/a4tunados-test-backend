# backend/aulas/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Tenta pegar o token do header Authorization normalmente
        header = self.get_header(request)
        if header is None:
            # Se não tem header, tenta pegar do cookie
            raw_token = request.COOKIES.get('access_token')
            if raw_token is not None:
                validated_token = self.get_validated_token(raw_token)
                return self.get_user(validated_token), validated_token
            return None
        return super().authenticate(request)