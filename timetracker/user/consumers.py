from channels.generic.websocket import WebsocketConsumer

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        print(self.channel_name)
        self.accept()

    def disconnect(self,close_code):
        pass