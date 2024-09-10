from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # Define fields explicitly
    password = serializers.CharField(max_length=65, write_only=True)
    email = serializers.EmailField(max_length=40)
    first_name = serializers.CharField(max_length=40)
    last_name = serializers.CharField(max_length=40)

    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')

        # Ensure email uniqueness (case-insensitive)
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists!'})

        return super().validate(attrs)

    def create(self, validated_data):
        # Extract the password from validated data
        password = validated_data.pop('password')
        
        # Create a new user with the provided data
        user = User.objects.create_user(**validated_data)
        
        # Set the password (hashed)
        user.set_password(password)
        user.save()
        
        return user
