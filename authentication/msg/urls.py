from django.urls import path
from .views import SendMessageView,ReceivedMessagesView


urlpatterns = [
    path('send-msg/', SendMessageView.as_view(), name='send-msg'),
    
    path('received-msg/', ReceivedMessagesView.as_view(), name='received-msg'),


]
