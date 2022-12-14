"""
ASGI config for ListeningParty project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import re_path
from party.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ListeningParty.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                re_path(r'^p/(?P<party_name>[\w.@+-0123456789]+)$', ChatConsumer.as_asgi()),
                re_path(r'^p/(?P<party_name>[\w.@+-0123456789]+)/search$', ChatConsumer.as_asgi())
            ])
        )
    )
})
