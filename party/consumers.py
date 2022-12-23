import asyncio
import json
import time
from django.contrib.auth import get_user_model, get_user
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Party, Party_Invite

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept",
        })

        await self.send({
            "type": "websocket.send",
            "text": "Hello world"
        })

    async def websocket_receive(self, event):
        print("recieve", event)

    async def websocket_disconnect(self, event):
        await self.remove_user()
        print("disconnect", event)

    @database_sync_to_async
    def remove_user(self):
        party = Party.get_current_party(self.scope['user'])

        if not party:
            return

        if party.users.count() == 0:
            party.delete()
            return

        party.remove_and_rearrange(self.scope['user'])

