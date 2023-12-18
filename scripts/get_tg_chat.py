# asyncio.run(main())
import asyncio
import os
from telethon import TelegramClient
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")
username = os.getenv("USERNAME")

async def get_messages():
    data = []
    async with TelegramClient(username, api_id, api_hash) as client:
        messages = await client.get_messages("https://t.me/armada_alli", limit=2000)
        for message in messages:
            if hasattr(message, 'sender_id'):
                reply = "No"
                reply_to_message_id = None
                if message.reply_to:
                    reply = "Yes"
                    reply_to_message_id = message.reply_to
                data.append([message.sender_id, message.text, message.date, message.id, reply, reply_to_message_id])
    return data

async def main():
    data = await get_messages()
    df = pd.DataFrame(data, columns=["sender_id", "text","date", "message_id", "reply", "reply_to_message_id"])
    df.to_csv('armada_chat_test.csv', encoding='utf-8')
    df.to_markdown('armada_chat_test.md')

asyncio.run(main())