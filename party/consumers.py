import asyncio
import json
from time import sleep
from django.contrib.auth import get_user_model, get_user
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import Party, Party_Invite, Party_Member
from login.models import Users

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        #updates status
        await self.update_refresh()
        print("connected", event)
        await self.send({
            "type": "websocket.accept",
        })

        """await self.send({
            "type": "websocket.send",
            "text": "Hello world"
        })"""

    async def websocket_receive(self, event):
        print("recieve", event)

    async def websocket_disconnect(self, event):
        #changes status of user then waits
        #if status is not changed back, deletes user
        await self.not_in_party()
        await asyncio.sleep(5)
        await self.delete_member()
        print("disconnect", event)


    #if the user has not been deleted from the party and refreshes the page
    #the user will be back in the party
    @database_sync_to_async
    def update_refresh(self):
        user = self.scope['user']

        party = Party.get_current_party(user)

        if not party:
            return 

        if party.is_member(user):
            member = party.users.get_queryset().filter(user=user).get()
        else:
            member = party.party_leader

        if not member.in_party:
            member.in_party = True
            member.save()
        
    #changes the party member to not be in the party
    #doesn't actually delete the user
    @database_sync_to_async
    def not_in_party(self):
        user = self.scope['user']

        party = Party.get_current_party(user)

        if not party:
            return

        party.pseudoremove_member(user)

    #If the user has not refreshed, the user is completely deleted through the data base
    @database_sync_to_async
    def delete_member(self):
        user = self.scope['user']

        party = Party.get_current_party(user)

        if not party:
            return

        member = Party_Member.objects.get_queryset().filter(user=user).get()

        if not member.in_party:
            party.remove_and_rearrange(user)

