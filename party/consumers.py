import asyncio
import json
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
        await self.delete_party()
        print("disconnect", event)

    @database_sync_to_async
    def delete_party(self):
        parties = Party.objects.get_queryset().filter(party_leader=self.scope['user'])
        if parties.count() == 0:
            return

        Party.objects.get(party_leader=self.scope['user']).delete()