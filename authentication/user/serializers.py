import logging
from rest_framework import serializers
from django.contrib.auth.models import User

# Get the logger for this module
logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Handles the serialization and deserialization of user data.
    Provides validation for email uniqueness and ensures password 
    hashing upon user creation.
    """
    
    # Define fields explicitly
    password = serializers.CharField(max_length=65, write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(max_length=40)
    first_name = serializers.CharField(max_length=40)
    last_name = serializers.CharField(max_length=40)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']

    def validate(self, attrs):
        """
        Validate the provided user data.

        Ensures that the email provided is unique across all users.
        Raises a validation error if the email already exists.
        
        Args:
            attrs (dict): The user data to validate.

        Returns:
            dict: The validated data.
        """
        email = attrs.get('email', '')

        # Ensure email uniqueness (case-insensitive)
        if User.objects.filter(email__iexact=email).exists():
            logger.warning(f"Validation failed: Email already exists - {email}")
            raise serializers.ValidationError({'email': 'Email already exists!'})

        logger.info(f"Validation passed for email: {email}")
        return super().validate(attrs)

    def create(self, validated_data):
        """
        Create a new user instance.

        Extracts the password from the validated data, creates a user 
        with the provided data, sets the password (hashed), and 
        saves the user to the database.
        
        Args:
            validated_data (dict): The validated data used to create the user.

        Returns:
            User: The created user instance.
        """
        # Extract the password from validated data
        password = validated_data.pop('password')
        
        # Create a new user with the provided data
        try:
            user = User.objects.create_user(**validated_data)
            # Set the password (hashed)
            user.set_password(password)
            user.save()
            logger.info(f"User created successfully: {user.username}")
            return user
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise serializers.ValidationError({'detail': 'Error creating user.'})
