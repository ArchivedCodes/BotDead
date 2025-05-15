import asyncio
from os import environ
from telethon import TelegramClient
from telethon.sessions import MemorySession
from telethon.events import NewMessage
from telethon.extensions import markdown

bot = TelegramClient(
    MemorySession(),
    api_id=int(environ.get("API_ID")),
    api_hash=environ.get("API_HASH")
    )

async def handleMessage(update: NewMessage.Event):
    await update.message.reply(
        message="""😔 We're sorry...
[This bot is no longer available.
Click here for more information.
Thank you for being with us](https://t.me/SpringsFern/141)""",
        link_preview=False,
        parse_mode=markdown
    )

bot.add_event_handler(handleMessage, NewMessage(
    incoming=True,
    func=lambda e: e.is_private,
))

async def handle_client(reader, writer):
    await reader.read(1024)
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        "Content-Length: 13\r\n"
        "\r\n"
        "OK"
    )
    writer.write(response.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def start_http_server():
    server = await asyncio.start_server(handle_client, '0.0.0.0', environ.get("PORT", 8080))
    print("HTTP server Started")
    async with server:
        await server.serve_forever()

async def main():
    asyncio.create_task(start_http_server())
    await bot.start(bot_token=environ.get("BOT_TOKEN"))
    print((await bot.get_me()).username)
    await bot.run_until_disconnected()

asyncio.run(main())