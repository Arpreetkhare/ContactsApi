import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.models import User

class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request).decode("utf-8")

        if not auth_data:
            return None
        
        # Split the authorization header into two parts: prefix and token
        try:
            prefix, token = auth_data.split(' ')
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')

      
        if prefix.lower() != 'bearer':
            raise exceptions.AuthenticationFailed('Authorization header must start with Bearer')

        try:
           
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(username=payload['username'])

            return (user, token)

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Your token is invalid. Please log in again.')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Your token has expired. Please log in again.')
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user found with this token.')
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Authentication failed: {str(e)}')

        return None
