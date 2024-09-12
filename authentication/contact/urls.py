# urls.py
from django.urls import path
from .views import ContactViewSet,FavoriteContactsView,ToggleFavoriteContactView

# Define viewset actions
contact_list = ContactViewSet.as_view({'get': 'list', 'post': 'create'})
contact_detail = ContactViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'update', 'delete': 'destroy'})
contact_share = ContactViewSet.as_view({'post': 'share'})
contact_bulk_delete = ContactViewSet.as_view({'post': 'bulk_delete'})  # Add this line



urlpatterns = [
    path('contacts/', contact_list, name='contact-list'),
    path('contacts/<int:pk>/', contact_detail, name='contact-detail'),
    path('contacts/<int:pk>/share/', contact_share, name='contact-share'),
    path('favorites/', FavoriteContactsView.as_view(), name='favorite-contacts'),
    path('contacts/bulk-delete/', contact_bulk_delete, name='contact-bulk-delete'),
    path('contacts/<int:contact_id>/toggle-favorite/', ToggleFavoriteContactView.as_view(), name='toggle-favorite-contact'),

]
