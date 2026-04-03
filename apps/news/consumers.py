import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NewsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': 'Socket connection established with snappy_backend!'
        }))

    async def receive(self, text_data):
        # This handles data sent FROM the client
        pass
