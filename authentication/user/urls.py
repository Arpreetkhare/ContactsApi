from django.urls import path
from .views import RegisterView,LoginView,users


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('users/', users, name='user-list')
]