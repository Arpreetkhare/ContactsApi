# contactsApi/urls.py
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.user.urls')),

    path('api/', include('authentication.contact.urls')),  # Include the app's urls
      path('api/msg/', include('authentication.msg.urls')), 

]

