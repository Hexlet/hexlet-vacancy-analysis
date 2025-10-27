import asyncio
import os

from dotenv import load_dotenv
from telethon.sync import TelegramClient

load_dotenv()
lock = asyncio.Lock()


class TelegramChannelClient:
    def __init__(self, client):
        self.client = client

    @classmethod
    async def create(cls):
        async with lock:
            client = TelegramClient(
                os.getenv("TELEGRAM_SESSION"),
                int(os.getenv("TELEGRAM_API_ID")),
                os.getenv("TELEGRAM_API_HASH"),
                system_version="4.10.5 beta x64",
            )
            await client.start()
            return cls(client)
