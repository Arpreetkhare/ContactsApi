from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializer
from shared_file.backends import JWTAuthentication


class SendMessageView(generics.CreateAPIView):
    """
    A view that allows an authenticated user to send messages to other users.
    
    The sender is automatically set to the authenticated user, and the receiver is
    specified by the receiver's user ID in the request data.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        """
        Handle the logic to create a new message.
        
        - The sender is automatically set as the currently authenticated user.
        - The receiver is retrieved from the request data using the provided receiver ID.
        - If the receiver does not exist, an error is returned.
        - If the receiver ID is not provided, a bad request error is returned.
        """
        try:
            sender = self.request.user  # Set the sender as the authenticated user
            
            # Retrieve the receiver by the ID provided in the request data
            receiver = User.objects.get(id=self.request.data['receiver'])

            # Save the message, linking the sender and receiver
            serializer.save(sender=sender, receiver=receiver)
        
        except User.DoesNotExist:
            # If the receiver ID doesn't match any existing user, return a 404 error
            return Response({"error": "Receiver not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except KeyError:
            # If receiver ID is not provided in the request, return a 400 error
            return Response({"error": "Receiver ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            # Handle any other unexpected errors
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReceivedMessagesView(generics.ListAPIView):
    """
    A view that lists all messages received by the authenticated user.
    
    This view fetches messages where the currently authenticated user is the receiver.
    """
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Retrieve the messages where the current user is the receiver.

        - If any unexpected error occurs while fetching the messages, it is handled and
          an error response is returned.
        """
        try:
            # Get the currently authenticated user
            user = self.request.user
            
            # Filter the Message objects where the current user is the receiver
            return Message.objects.filter(receiver=user)

        except Exception as e:
            # Handle any unexpected errors during the query
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
