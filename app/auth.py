from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class AppTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization', None)
        if auth is None:
            raise AuthenticationFailed('Invalid authorization header. No credentials provided.')
        if auth:
            try:
                token = self.get_model().objects.get(key=auth)
                return self.authenticate_credentials(token)
            except self.get_model().DoesNotExist:
                raise AuthenticationFailed('Invalid token.')

        raise AuthenticationFailed('Invalid authorization header. No credentials provided.')