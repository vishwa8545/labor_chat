from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import GroupChat, GroupChatMessage,Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['username']
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        recipient_username = text_data_json['recipient']
        sender_username = text_data_json['sender']
        message_text = text_data_json['message']
        recipient = User.objects.get(username=recipient_username)
        sender = User.objects.get(username=sender_username)

        # Save the message to the database
        message = Message.objects.create(sender=sender, recipient=recipient, text=message_text)

        # Send the message to the recipient
        await self.channel_layer.group_add(
            f"user_{recipient.id}",
            self.channel_name
        )

        await self.channel_layer.group_send(
            f"user_{recipient.id}",
            {
                'type': 'chat_message',
                'message': message_text,
                'sender': sender_username,
                'timestamp': str(message.timestamp)
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.group_chat = await self.get_group_chat(self.group_name)

        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']

        # Save message to database
        await self.save_message(sender_id, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id
        }))

    @database_sync_to_async
    def get_group_chat(self, group_name):
        return GroupChat.objects.get(name=group_name)

    @database_sync_to_async
    def save_message(self, sender_id, message):
        group_chat_message = GroupChatMessage.objects.create(
            group_chat=self.group_chat,
            sender_id=sender_id,
            message=message
        )
        group_chat_message.save()