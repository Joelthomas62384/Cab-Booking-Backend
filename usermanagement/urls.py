from django.urls import path
from .views import *


urlpatterns = [
    path('register' ,RegisterUserView.as_view()),
    path('login' , LoginView.as_view()),
    path('refresh_token', RefreshTokenView.as_view()),  
    path('me' , UserView.as_view()),
    path('logout', LogoutView.as_view()),
]
