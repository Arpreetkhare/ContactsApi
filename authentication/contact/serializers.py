import logging
from rest_framework import serializers

from .models import Contact



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'contact_name', 'contact_number', 'contact_email','is_fav','Other_details']



# Get the logger for this module
logger = logging.getLogger(__name__)

class ShareContactSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), 
        allow_empty=False
    )

    def validate_user_ids(self, value):
        """
        Validate the user IDs provided for sharing contacts.

        Ensures that the user IDs are in the correct format and are integers.

        Args:
            value (list): The user IDs to validate.

        Returns:
            list: The validated user IDs.
        """
        logger.info("Validating user IDs for sharing contacts.")
        
        if not isinstance(value, list):
            logger.error("Validation failed: User IDs is not a list.")
            raise serializers.ValidationError("User IDs must be a list.")
        if not all(isinstance(id, int) for id in value):
            logger.error("Validation failed: One or more User IDs are not integers.")
            raise serializers.ValidationError("Each User ID must be an integer.")
        
        logger.info("User IDs validated successfully.")
        return value