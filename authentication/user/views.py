from django.shortcuts import render
from datetime import datetime, timedelta
from rest_framework.generics import GenericAPIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view


from .serializers import UserSerializer
from rest_framework.response import Response
# from django.http import HttpResponse


from rest_framework import status


import jwt

from contactsapi import base
# from .backends import JWTAuthentication

# Create your views here.


class RegisterView(GenericAPIView):
    serializer_class=UserSerializer


    def post(self,request):
        serializer=UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    



class Loginview(GenericAPIView):
    
    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')

        # Authenticating the user
        user = authenticate(username=username, password=password)

        if user is not None:
            try:
                # Set token expiration time (e.g., 24 hours)
                expiration = datetime.utcnow() + timedelta(hours=24)
                
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
                return Response(data, status=status.HTTP_200_OK)

            except jwt.DecodeError:
                return Response({'detail': 'Token generation failed. Invalid token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except jwt.ExpiredSignatureError:
                return Response({'detail': 'Token has expired.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                print(e)
                return Response({'detail': 'Server error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Invalid credentials
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET'])
def users(request) :
    all_user=User.objects.all() 

    serializer=UserSerializer(all_user,many=True)  

    return Response(serializer.data)