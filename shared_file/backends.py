import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.models import User

class JWTAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class to handle JSON Web Token (JWT) authentication.

    This class extends `BaseAuthentication` from Django REST Framework and implements
    JWT authentication for API requests. It extracts the token from the request header,
    validates it, and retrieves the corresponding user.
    """

    def authenticate(self, request):
        """
        Authenticate the user by extracting and validating the JWT from the request.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            tuple: A tuple containing the user and token if authentication is successful.
            None: If authentication fails or no token is provided.

        Raises:
            exceptions.AuthenticationFailed: If token validation fails or user is not found.
        """
        # Extract the authorization header from the request and decode it
        auth_data = authentication.get_authorization_header(request).decode("utf-8")

        # Check if the authorization header is present
        if not auth_data:
            return None
        
        # Split the authorization header into prefix and token
        try:
            prefix, token = auth_data.split(' ')
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')

        # Ensure the prefix is 'Bearer'
        if prefix.lower() != 'bearer':
            raise exceptions.AuthenticationFailed('Authorization header must start with Bearer')

        try:
            # Decode the JWT token using the secret key and algorithm
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
            
            # Retrieve the user from the database based on the username in the payload
            user = User.objects.get(username=payload['username'])

            # Return the user and token if everything is correct
            return (user, token)

        except jwt.DecodeError:
            # Handle errors related to decoding the token
            raise exceptions.AuthenticationFailed('Your token is invalid. Please log in again.')
        except jwt.ExpiredSignatureError:
            # Handle errors related to token expiration
            raise exceptions.AuthenticationFailed('Your token has expired. Please log in again.')
        except User.DoesNotExist:
            # Handle cases where the user does not exist
            raise exceptions.AuthenticationFailed('No user found with this token.')
        except Exception as e:
            # Handle any other exceptions
            raise exceptions.AuthenticationFailed(f'Authentication failed: {str(e)}')

        return None
