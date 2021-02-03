from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from API.routing import urlpatterns
application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
            URLRouter(urlpatterns)
        ),
})