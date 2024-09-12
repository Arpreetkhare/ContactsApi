from rest_framework import serializers
from django.contrib.auth.models import User

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
            ''' "WHY EMAIL_IEXACT WHY NOT EMAIL !! "
            If email is example@example.com, 
            the query will match EXAMPLE@EXAMPLE.COM, Example@Example.Com, etc., 
            as well as example@example.com.
T           his is useful for cases where you want to ensure that 
            email addresses are unique without regard to case differences. it will
            go for same looking email.
            '''
            raise serializers.ValidationError({'email': 'Email already exists!'})

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
        user = User.objects.create_user(**validated_data)
        
        # Set the password (hashed)
        user.set_password(password)
        user.save()
        
        return user
