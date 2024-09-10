# apps/contacts/serializers.py
from rest_framework import serializers

from .models import Contact



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'contact_name', 'contact_number', 'contact_email','is_fav','Other_details']



class ShareContactSerializer(serializers.Serializer):

    user_ids= serializers.ListField (
        child=serializers.IntegerField(), 
        allow_empty=False
    )


    def validate_user_ids(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("User IDs must be a list.")
        if not all(isinstance(id, int) for id in value):
            raise serializers.ValidationError("Each User ID must be an integer.")
        return value