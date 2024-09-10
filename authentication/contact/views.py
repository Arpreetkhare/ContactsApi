from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.decorators import action


from .serializers import ContactSerializer,ShareContactSerializer
from .models import Contact
from shared_file.backends import JWTAuthentication

class ContactViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            # Automatically set the user field from the request
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

    @action(detail=True,methods=['post'])

    def share(self,request,pk=None):

        contact=Contact.objects.get(pk=pk, user=request.user)
        if not contact:
            return Response({'detail': 'Contact not found or you are not the owner.'}, status=404)
        
        serializer = ShareContactSerializer(data=request.data)
        if serializer.is_valid():
            user_ids=serializer.validated_data["user_ids"]

            users= User.objects.filter(id__in=user_ids)

            contact.shared_with.add(*users)

            contact.save()  
            return Response({'detail': 'Contact shared successfully.'}, status=200)
        return Response(serializer.errors, status=400)



    def list(self, request):
        # Fetch user's own contacts
        owned_contacts = Contact.objects.filter(user=request.user)
        # Fetch contacts shared with the user
        shared_contacts = Contact.objects.filter(shared_with=request.user)
        # Combine both lists
        contacts = owned_contacts | shared_contacts

        # Serialize the contacts
        serializer = ContactSerializer(contacts, many=True)
        # Return the serialized data
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            contact = Contact.objects.get(pk=pk, user=request.user)
        except Contact.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            contact = Contact.objects.get(pk=pk, user=request.user)
        except Contact.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            # Only the fields provided in the request data will be updated
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        try:
            contact = Contact.objects.get(pk=pk, user=request.user)
        except Contact.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=404)
        contact.delete()
        return Response(status=204)

class FavoriteContactsView(generics.ListAPIView): 
    serializer_class = ContactSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only favorite contacts for the current user
        return Contact.objects.filter(user=self.request.user, is_fav=True)

class ToggleFavoriteContactView(generics.GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, contact_id):
        try:
            contact = Contact.objects.get(id=contact_id, user=request.user)
            contact.is_fav = not contact.is_fav
            contact.save()
            return Response({'message': 'Favorite status updated.', 'is_favorite': contact.is_fav})
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found.'}, status=status.HTTP_404_NOT_FOUND)
