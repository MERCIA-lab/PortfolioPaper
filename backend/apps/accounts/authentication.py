from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

class CookieOrHeaderJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        if header is not None:
            raw_token = self.get_raw_token(header)
            if raw_token is not None:
                try:
                    validated_token = self.get_validated_token(raw_token)
                    return self.get_user(validated_token), validated_token
                except InvalidToken:
                    pass  
        cookie_token = request.COOKIES.get('access_token')
        if cookie_token:
            try:
                validated_token = self.get_validated_token(cookie_token)
                return self.get_user(validated_token), validated_token
            except InvalidToken:
                pass  
