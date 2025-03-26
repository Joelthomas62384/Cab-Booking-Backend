from django.urls import path
from . views import *



urlpatterns = [
    path('register' , CabView.as_view()),
    path('get-cabs', CabView.as_view()),
    path('approve/<pk>' ,ApproveView.as_view() ),
    path('get-riders' ,GetFreeCabs.as_view()),
    path('update-path', UpdatePath.as_view()),
    path('get-driver-profile' , DriverProfile.as_view()),
    path('check-change' , CheckChange.as_view()),
]
