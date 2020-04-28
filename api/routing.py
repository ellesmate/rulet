from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/kitchen/(?P<room_name>\w+)/$', consumers.CookConsumer),
    path('ws/group/<str:entity>/', consumers.CookConsumer),
]
