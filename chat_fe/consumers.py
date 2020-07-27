# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Friend
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def fetch_messages(self, data):
        print("room:", data["room"])
        room = data["room"]
        room_obj = Friend.objects.filter(room=room).first()
        # serialize the messages
        msg = self.get_messages(room_obj)
        content = {"command": "messages", "messages": msg}
        self.send(text_data=json.dumps(content))
        other_user = room_obj.other_user.client.get_username()
        self.send(text_data=json.dumps(other_user))

    def new_message(self, data):
        # add to db and send back to client
        user_id = data["from"]
        msg = data["message"]
        roomName = data["room"]
        # room name
        rooms = Friend.objects.filter(room=roomName)
        user = User.objects.get(username=user_id)
        message = Message.objects.create(user=user, messenger=msg)
        for room in rooms:
            room.messages.add(message)
        content = {
            "command": "new_message",
            "message": {"user": message.user.username, "messenger": message.messenger,},
        }
        return self.send_chat_message(content)

    commands = {"fetch_messages": fetch_messages, "new_message": new_message}

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        # receive a command what to do from ws
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))

    # method that gets the messages from db
    def get_messages(self, room):
        msg = []
        messages = room.get_messages()
        for message in messages:
            msger = {
                "user": message.user.username,
                "messenger": message.messenger,
                "room": str(room.pk),
            }
            msg.append(msger)

        return msg

