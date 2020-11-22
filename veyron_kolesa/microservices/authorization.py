from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from veyron_kolesa.microservices.models import Service
from veyron_kolesa.users.models import User


class CapsTokenAuthentication(BaseAuthentication):
    keyword = 'Token'
    model = None

    @property
    def caps(self):
        return Service.objects.get(name='caps')

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        response = self.caps.remote_call('get', '/api/users/profile',
                                     headers={'Authorization': 'Token {key}'.format(key=key)})
        user = User(response.json())
        return user, key

    def authenticate_header(self, request):
        return self.keyword
