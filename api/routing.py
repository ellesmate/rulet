from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/kitchen/(?P<room_name>\w+)/$', consumers.CookConsumer),
    # path('ws/kitchen/<str:entity>/', consumers.CookConsumer),
    path('ws/kitchen/', consumers.CookConsumer),
    path('ws/hall/<str:entity>/', consumers.WaiterConsumer),
]
