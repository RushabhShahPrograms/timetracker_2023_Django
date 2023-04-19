from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        # self.accept()
        self.room_name="test_consumer"
        self.room_group_name="test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_name,self.room_group_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status':'connected'}))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        notification_type = text_data_json['notification_type']
        sender = text_data_json['sender']
        recipient = text_data_json['recipient']
        
        # If the sender is a manager and the recipient is a developer, send the notification to the developer
        if sender == 'is_manager' and recipient == 'is_developer':
            self.send(text_data=json.dumps({
                'message': message,
                'notification_type': notification_type,
                'sender': sender,
                'recipient': recipient
            }))
        
        # If the sender is a developer and the recipient is a manager, send the notification to the manager
        elif sender == 'is_developer' and recipient == 'is_manager':
            self.send(text_data=json.dumps({
                'message': message,
                'notification_type': notification_type,
                'sender': sender,
                'recipient': recipient
            }))

    def disconnect(self, close_code):
        pass

