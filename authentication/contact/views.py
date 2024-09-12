import logging
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from .serializers import ContactSerializer, ShareContactSerializer
from .models import Contact
from shared_file.backends import JWTAuthentication

# Set up logging
logger = logging.getLogger(__name__)

class ContactPagination(PageNumberPagination):
    page_size = 5  # You can customize this

class ContactViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions for Contact objects.
    This includes create, retrieve, update, delete, and share functionality.
    Users can manage their own contacts and share contacts with other users.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = ContactPagination  # Attach your custom pagination class

    def create(self, request):
        """
        Create a new contact for the authenticated user.
        
        The user field is automatically set to the requesting user.
        """
        logger.info(f"User {request.user} is attempting to create a new contact.")
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically set the user field to the current user
            serializer.save(user=request.user)
            logger.info(f"Contact created successfully for user {request.user}.")
            return Response(serializer.data, status=201)
        logger.error(f"Error creating contact: {serializer.errors}")
        return Response(serializer.errors, status=400)
    
    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """
        Share the contact with other users.

        This action allows a user to share a specific contact with a list of other users,
        identified by their user IDs.
        """
        logger.info(f"User {request.user} is sharing contact ID {pk}.")
        try:
            contact = Contact.objects.get(pk=pk, user=request.user)
            logger.info(f"Contact {pk} found for sharing.")
        except Contact.DoesNotExist:
            logger.error(f"Contact {pk} not found or you are not the owner.")
            return Response({'detail': 'Contact not found.'}, status=404)
        
        serializer = ShareContactSerializer(data=request.data)
        if serializer.is_valid():
            user_ids = serializer.validated_data["user_ids"]
            logger.info(f"Sharing contact {pk} with user IDs: {user_ids}.")
            users = User.objects.filter(id__in=user_ids)
            contact.shared_with.add(*users)
            contact.save()
            logger.info(f"Contact {pk} shared successfully.")
            return Response({'detail': 'Contact shared successfully.'}, status=200)
        logger.error(f"Error sharing contact: {serializer.errors}")
        return Response(serializer.errors, status=400)

    def list(self, request):
        """
        List all contacts for the authenticated user.

        This includes both contacts owned by the user and contacts shared with the user.
        """
        logger.info(f"User {request.user} is requesting their contact list.")
        owned_contacts = Contact.objects.filter(user=request.user)
        shared_contacts = Contact.objects.filter(shared_with=request.user)
        contacts = owned_contacts | shared_contacts

        # Serialize the combined contact list
        serializer = ContactSerializer(contacts, many=True)
        logger.info(f"Contact list retrieved for user {request.user}.")
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific contact by its primary key.

        The contact must belong to the authenticated user.
        """
        logger.info(f"User {request.user} is retrieving contact {pk}.")
        try:
            contact = Contact.objects.get(pk=pk, user=request.user)
            logger.info(f"Contact {pk} retrieved for user {request.user}.")
        except Contact.DoesNotExist:
            logger.error(f"Contact {pk} not found for user {request.user}.")
            return Response({'detail': 'Not found.'}, status=404)

        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update a contact's details for the authenticated user.

        Only the fields provided in the request data will be updated.
        """
        logger.info(f"User {request.user} is trying to update contact {pk}.")
        try:
            contact = Contact.objects.get(pk=pk, user=request.user)
            logger.info(f"Contact {pk} found for update.")
        except Contact.DoesNotExist:
            logger.error(f"Contact {pk} not found for update by user {request.user}.")
            return Response({'detail': 'Not found.'}, status=404)

        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            logger.info(f"Contact {pk} updated successfully for user {request.user}.")
            return Response(serializer.data)
        logger.error(f"Error updating contact {pk}: {serializer.errors}")
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """
        Delete a specific contact belonging to the authenticated user.
        """
        logger.info(f"User {request.user} is attempting to delete contact {pk}.")
        try:
            contact = Contact.objects.get(pk=pk, user=request.user)
            contact.delete()
            logger.info(f"Contact {pk} deleted successfully for user {request.user}.")
            return Response({f"Contact {pk} deleted successfully"},status=204)
        except Contact.DoesNotExist:
            logger.error(f"Contact {pk} not found for deletion by user {request.user}.")
            return Response({'detail': 'Not found.'}, status=404)
        

    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """
        Bulk delete contacts for the authenticated user.

        This action allows users to delete multiple contacts at once based on the provided contact IDs.
        """
        logger.info(f"User {request.user} is attempting to bulk delete contacts.")
        contact_ids = request.data.get('contact_ids', [])

        if not isinstance(contact_ids, list):
            logger.error("Invalid input data for bulk delete.")
            return Response({'detail': 'Invalid input data.'}, status=status.HTTP_400_BAD_REQUEST)

        contacts = Contact.objects.filter(pk__in=contact_ids, user=request.user)
        if not contacts:
            logger.error("No contacts found for bulk delete.")
            return Response({'detail': 'Contacts not found.'}, status=status.HTTP_404_NOT_FOUND)

        count, _ = contacts.delete()
        logger.info(f"Bulk delete completed successfully for contacts: {contact_ids}. Deleted {count} contacts.")
        return Response({'detail': f'{count} contacts deleted successfully.'}, status=status.HTTP_200_OK)
    

class FavoriteContactsView(generics.ListAPIView):
    """
    A view that lists all favorite contacts for the authenticated user.
    """
    serializer_class = ContactSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return only the contacts marked as favorite by the authenticated user.
        """
        logger.info(f"User {self.request.user} is requesting their favorite contacts.")
        return Contact.objects.filter(user=self.request.user, is_fav=True)

class ToggleFavoriteContactView(generics.GenericAPIView):
    """
    A view that toggles the favorite status of a specific contact.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, contact_id):
        """
        Toggle the favorite status of a contact.
        
        The contact must belong to the authenticated user.
        """
        logger.info(f"User {request.user} is toggling favorite status for contact {contact_id}.")
        try:
            contact = Contact.objects.get(id=contact_id, user=request.user)
            contact.is_fav = not contact.is_fav
            contact.save()
            logger.info(f"Favorite status for contact {contact_id} updated to {contact.is_fav}.")
            return Response({'message': 'Favorite status updated.', 'is_favorite': contact.is_fav})
        except Contact.DoesNotExist:
            logger.error(f"Contact {contact_id} not found for user {request.user}.")
            return Response({'error': 'Contact not found.'}, status=status.HTTP_404_NOT_FOUND)
