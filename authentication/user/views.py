import logging
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
import jwt
from contactsapi import base
from .serializers import UserSerializer

# Get the logger for this module
logger = logging.getLogger(__name__)


def home():
    return "hello!! you are in "

class RegisterView(GenericAPIView):
    """
    View for registering a new user.
    """
    serializer_class = UserSerializer

    def post(self, request):
        """
        Handle POST request for user registration.

        Validates and saves the new user data using the UserSerializer.
        Returns a success response with user data on successful creation,
        or an error response if validation fails.
        """
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"User registered successfully: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.error(f"User registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    """
    View for user login and JWT token generation.
    """
    
    def post(self, request):
        """
        Handle POST request for user login.

        Authenticates the user based on provided username and password.
        On successful authentication, generates a JWT token and returns
        the user data along with the token. Handles token generation errors
        and returns appropriate error responses.
        """
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')

        # Authenticating the user
        user = authenticate(username=username, password=password)

        if user is not None:
            try:
                # Set token expiration time (e.g., 24 hours)
                expiration = datetime.utcnow() + timedelta(hours=1234)
                
                # Create JWT token with an expiration time
                auth_token = jwt.encode(
                    {'username': user.username, 'exp': expiration},
                    base.JWT_SECRET_KEY,
                    algorithm="HS256"
                )
                
                # Serialize the user data
                serializer = UserSerializer(user)
                
                # Return the user data and the JWT token
                data = {'user': serializer.data, 'token': auth_token}
                logger.info(f"User logged in successfully: {user.username}")
                return Response(data, status=status.HTTP_200_OK)

            except jwt.DecodeError:
                logger.error('Token generation failed. Invalid token.')
                return Response({'detail': 'Token generation failed. Invalid token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except jwt.ExpiredSignatureError:
                logger.error('Token has expired.')
                return Response({'detail': 'Token has expired.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                # Log the exception for debugging
                logger.error(f"Server error: {e}")
                return Response({'detail': 'Server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Invalid credentials
        logger.warning('Invalid credentials provided.')
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def users(request):
    """
    Retrieve a list of all users.

    Handles GET requests and returns a list of all users serialized
    using the UserSerializer.
    """
    try:
        all_user = User.objects.all()
        serializer = UserSerializer(all_user, many=True)
        logger.info('Successfully retrieved list of users.')
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error retrieving list of users: {e}")
        return Response({'detail': 'Server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
