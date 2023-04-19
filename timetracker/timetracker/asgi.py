"""
ASGI config for timetracker project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from user.consumers import *
from . import consumers


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timetracker.settings')

application = get_asgi_application()

ws_patterns=[
    path('ws/notifications/', NotificationConsumer),
]

application=ProtocolTypeRouter({
    'websocket':URLRouter(ws_patterns),
})
