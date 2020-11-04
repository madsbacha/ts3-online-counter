from utils import env
from constants import DATA_UPDATE, REDIS_CHANNEL
from redis import Redis
from discord import Client
from threading import Thread
import asyncio


def get_redis():
    return Redis(env("REDIS_HOST", "localhost"), env("REDIS_PORT", 6379, int), db=0, socket_timeout=10000)



class MyClient(Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        self.redis = asyncio.create_task(self.redis_thread())
        

    async def update_channel_count(self, count):
        print("Updating channel count")
        channel = self.get_channel(int(env("DISCORD_CHANNEL_ID")))
        print(channel)
        if channel is not None:
            print(f"UPDATING TO {count}")
            await channel.edit(name=f"TS: {count} online")
        print("Done")
        
    async def redis_thread(self):
        r = get_redis()
        p = r.pubsub()
        p.subscribe(REDIS_CHANNEL)
        last_count = 0
        await self.update_channel_count(last_count)
        for message in p.listen():
            print(message)
            try:
                print(f"is message: {message['type'] == 'message'}, is dataupdate:{message['data'].decode('ascii') == DATA_UPDATE}")
                if message['type'] == "message" and message['data'].decode('ascii') == DATA_UPDATE:
                    print(message)
                    count = r.get('counter').decode("ascii")
                    print(f"count: {count}, last_count: {last_count}, update: {count != last_count}")
                    if count != last_count:
                      last_count = count
                      await self.update_channel_count(count)
            except (UnicodeDecodeError, AttributeError):
                pass


client = MyClient()
client.run(env('DISCORD_TOKEN'))
