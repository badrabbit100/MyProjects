from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import channels.layers
from .services_consumer import select_type_data


channel_layer = channels.layers.get_channel_layer()


class GameRoom(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = 'room_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

    def receive(self, text_data):
        """ Receive message from web socket """

        if select_type_data(text_data) is True:
            type_message = 'run_game'
        else:
            type_message = 'chat_message'
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {
                'type': type_message,
                'payload': text_data
            }
        )

    def chat_message(self, event):
        """ Send chat-data to websocket """

        data = event['payload']
        data = json.loads(data)
        self.send(text_data=json.dumps({
            'payload': data['data']
        }))

    def run_game(self, event):
        """ Send Game-data to websocket """

        data = event['payload']
        data = json.loads(data)
        self.send(text_data=json.dumps({
            'payload': data['data']
        }))
