from django.urls import path
from .views import RegisterView,Loginview,users


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', Loginview.as_view()),
    path('users/', users, name='user-list'),
]