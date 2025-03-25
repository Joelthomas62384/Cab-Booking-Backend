from django.urls import path
from . views import *



urlpatterns = [
    path('register' , CabView.as_view()),
    path('get-cabs', CabView.as_view()),
]
