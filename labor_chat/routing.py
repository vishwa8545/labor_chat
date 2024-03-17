from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat import consumers

websocket_urlpatterns = [
    path('ws/group_chat/<str:group_name>/', consumers.GroupChatConsumer.as_asgi()),
    path('ws/chat/<str:username>/', consumers.ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})


