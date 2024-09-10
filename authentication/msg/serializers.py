from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Only include necessary fields

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested serializer for sender
    content = serializers.CharField()  # Include content field

    class Meta:
        model = Message
        fields = ['sender', 'content']  # Only include sender and content fields
