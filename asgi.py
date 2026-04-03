import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.news.routing # We will create this next

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snappy_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.news.routing.websocket_urlpatterns
        )
    ),
})
