import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer

redis_client = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)

class LocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.rider_id = self.scope["url_route"]["kwargs"]["rider_id"]
        self.room_group_name = f"rider_{self.rider_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f"✅ WebSocket Connection Established: {self.rider_id}")

    async def receive(self, text_data):
        print(f"📩 Received Data: {text_data}")  # DEBUG LOG

        try:
            data = json.loads(text_data)
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            if latitude and longitude:
                print(f"✅ Valid Location Data: {latitude}, {longitude}")

                redis_client.set(
                    f"rider:{self.rider_id}:location",
                    json.dumps({"lat": latitude, "lng": longitude})
                )

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "send_location",
                        "latitude": latitude,
                        "longitude": longitude,
                    },
                )
            else:
                print("⚠️ Missing latitude or longitude")
        except json.JSONDecodeError:
            print("❌ Error Decoding JSON")

    async def send_location(self, event):
        await self.send(text_data=json.dumps({
            "latitude": event["latitude"],
            "longitude": event["longitude"]
        }))

    async def disconnect(self, close_code):
        print(f"⚠️ WebSocket Disconnected: {self.rider_id}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
