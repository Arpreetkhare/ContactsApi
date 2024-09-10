from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Message
from .serializers import MessageSerializer
from shared_file.backends import JWTAuthentication


class SendMessageView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        try:
            sender = self.request.user

            # Retrieve receiver by ID from the request data
            receiver = User.objects.get(id=self.request.data['receiver'] , username=self.request.data['receiver'])

            # Save the message with sender and receiver
            serializer.save(sender=sender, receiver=receiver)
        
        except User.DoesNotExist:
            return Response({"error": "Receiver not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except KeyError:
            return Response({"error": "Receiver ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ReceivedMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            user = self.request.user
            return Message.objects.filter(receiver=user)

        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
