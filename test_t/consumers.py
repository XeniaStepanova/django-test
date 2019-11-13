from channels.generic.websocket import AsyncWebsocketConsumer
import json
import httpx
from asyncio import as_completed


class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

        
    # Receive message from WebSocket
    async def receive(self, text_data):

        async def make_reque(client, url):
            response = await client.head(url)
            return url, response
            
            
        text_data_json = json.loads(text_data)
        message = text_data_json['message'].strip()
        if message[-1] != '/':
            message = f'{message}/'
        
        with open("test_t/directory-list-2.3-small.txt") as folders:
            urls = [f'{message}{line.strip()}/' for line in folders]
        async with httpx.AsyncClient() as client:
            pendings = [make_reque(client, url) for url in urls]
            
            batches = (pendings[i:i + 30] for i in range(0, len(pendings), 30))
            
            for batch in batches:
                for future in as_completed(batch):
                    url, response = await future
                    if response.status_code == 200:
                        answ = "exist"
                    else:
                        answ = "not exist"
                    await self.send(text_data=json.dumps({'message': f'{url} : {answ}'}))

    
       

