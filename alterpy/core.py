import utils.log
import utils.config
import utils.mod
import utils.file
import sqlite3
import aiohttp
import asyncio
import telethon.events.newmessage
import telethon.tl.custom.message
import logging
import typing
import os

from . import context


async def process_message(msg: telethon.tl.custom.message.Message) -> None:
    tasks = [
        asyncio.create_task(handler.invoke(msg))
        for handler in context.message_handlers
    ]
    if tasks:
        await asyncio.wait(tasks)


async def event_handler(event: telethon.events.newmessage.NewMessage) -> None:
    await process_message(event.message)


async def main(log: logging.Logger) -> None:
    log.info("AlterPy")

    config = utils.config.load("config")
    for el in config["admins"]: context.admins.add(el)
    log_id = config.get("log", 0)
    del config
    del el
    log.info("loaded config")

    alterpy_prev = os.getenv('alterpy_prev', '')
    try:
        _chat, _reply = map(int, alterpy_prev.split())
    except:
        _chat, _reply = log_id, None

    telethon_config = utils.config.load("telethon")
    try:
        async with aiohttp.ClientSession() as context.session:
            client = telethon.TelegramClient("alterpy", telethon_config['api_id'], telethon_config['api_hash'])
            await client.start(bot_token=telethon_config['bot_token'])
            async with client:
                log.info("Started telethon instance")
                if log_id:
                    await client.send_message(_chat, "← alterpy is starting...", reply_to=_reply)

                context.the_bot_id = int(telethon_config['bot_token'].split(':')[0])
                del telethon_config

                res = await utils.mod.load_handlers([], context.message_handlers, "handlers", True)
                await client.send_message(_chat, f"← alterpy start: {res}. Check logs for further info", reply_to=_reply)

                client.add_event_handler(event_handler, telethon.events.newmessage.NewMessage)

                log.info("Started!")
                await client.run_until_disconnected()
    except sqlite3.OperationalError:
        log.error("Another instance of this bot is already running!")


