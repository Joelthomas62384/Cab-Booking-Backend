from django.urls import path
from . utils import get_places

urlpatterns = [
    path("search" ,get_places )
]
