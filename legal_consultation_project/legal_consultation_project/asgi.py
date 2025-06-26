"""
ASGI config for legal_consultation_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""


# import os
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
# from ChatApp.routing import websocket_urlpatterns
# from videochat.routing import websocket_urlpatterns

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_consultation_project.settings')

# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })


# legal_consultation_project/legal_consultation_project/asgi.py

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_consultation_project.settings')

# --- IMPORTANT CHANGE: Import routing from your app ---
import video_app.routing # This line tells Python where to find your websocket_urlpatterns
# ---
import ChatApp.routing 
 

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                # --- IMPORTANT CHANGE: Reference the imported routing ---
                video_app.routing.websocket_urlpatterns + ChatApp.routing.websocket_urlpatterns
            )
        )
    ),
})
