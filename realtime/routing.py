

from django.urls import re_path
from . consumers import *


websocket_urlpatterns = [
    re_path(r"^ws/location/(?P<rider_id>\d+)/$", LocationConsumer.as_asgi()),
    ]