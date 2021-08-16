import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .tasks import sum

class DemoConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add('operations', self.channel_name))
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard('operations', self.channel_name))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        operation = text_data_json['operation']
        reply = {}
        if operation:
            if operation == 'sum':
                sum.delay(text_data_json['number1'], text_data_json['number2'])
                self.send('Task Created!')
        else:
            reply['result'] = 'FAILED'
            self.send(json.dumps(reply))
    
    def result(self, event):
        self.send(json.dumps(event['reply']))