import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Teams 
from django.core import serializers

class BotConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "bot"
        self.room_group_name = 'bot_room'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            'bot_room',
            self.channel_name
        )

        self.accept()


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        teams = Teams.objects.order_by("-team_points")[:999]
        data = serializers.serialize("json", teams)
        # Send message to room group

    def bot_room(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))