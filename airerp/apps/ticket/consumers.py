import json
from channels.generic.websocket import AsyncWebsocketConsumer


class TicketStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'ticket_status'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def send_ticket_status(self, event):
        await self.send(text_data=json.dumps({'data': event['data']}))

