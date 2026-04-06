import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NewsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "counter_group"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the broadcast group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # 1. Parse the incoming message from the button click
        data = json.loads(text_data)
        count = data.get('count')

        # 2. Broadcast that count to the ENTIRE group (everyone connected)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'counter_update', # This must match the method name below
                'count': count
            }
        )

    async def counter_update(self, event):
        count = event['count']
        await self.send(text_data=json.dumps({
            'count': count
        }))
