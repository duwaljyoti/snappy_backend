import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# 1. Set settings first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'snappy_backend.settings')

# 2. Initialize the Django ASGI app early (This is the critical step!)
django_asgi_app = get_asgi_application()

# 3. Import your routing AFTER get_asgi_application()
import apps.news.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.news.routing.websocket_urlpatterns
        )
    ),
})
