import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.user_id = self.user.id
            self.room_group_name = f'user_{self.user_id}'

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        receiver_id = text_data_json["receiver_id"]
        client_id = text_data_json["client_id"]
        username = text_data_json["username"]

        # Save message to database
        await self.save_message(self.user, receiver_id, message)

        # Send to receiver's group
        receiver_group = f'user_{receiver_id}'
        await self.channel_layer.group_send(
            receiver_group,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": self.user_id,
                "sender_username": username,
                "client_id": client_id
            }
        )

        # Send to sender's group to show in their chat too
        sender_group = f'user_{self.user_id}'
        await self.channel_layer.group_send(
            sender_group,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": self.user_id,
                "sender_username": username,
                "client_id": client_id
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        sender_id = event["sender_id"]
        sender_username = event["sender_username"]
        client_id = event["client_id"]

        await self.send(text_data=json.dumps({
            "message": message,
            "sender_id": sender_id,
            "sender_username": sender_username,
            "client_id": client_id
        }))

    @database_sync_to_async
    def save_message(self, sender, receiver_id, content):
        receiver = User.objects.get(id=receiver_id)
        return Message.objects.create(sender=sender, receiver=receiver, content=content)
