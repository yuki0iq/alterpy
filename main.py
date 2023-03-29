import utils.log
import utils.config
import utils.mod
import sqlite3
import asyncio
import telethon.events
import telethon.tl.custom.message
import rich.traceback
import context


log = utils.log.get("main")
message_handlers = []


async def process_message(msg: telethon.tl.custom.message.Message):
    tasks = [
        asyncio.create_task(handler.invoke(msg))
        for handler in message_handlers
    ]
    if tasks:
        await asyncio.wait(tasks)


async def event_handler(event: telethon.events.NewMessage):
    await process_message(event.message)


async def main():
    log.info("AlterPy")

    config = utils.config.load("config.toml")
    for el in config["admins"]: context.admins.add(el)
    for el in config["banned"]: context.banned.add(el)
    del config
    del el
    log.info("loaded config")

    telethon_config = utils.config.load("telethon_config.toml")
    try:
        client = telethon.TelegramClient("alterpy", telethon_config['api_id'], telethon_config['api_hash'])
        await client.start(bot_token=telethon_config['bot_token'])
        async with client:
            log.info("Started telethon instance")

            context.the_bot_id = int(telethon_config['bot_token'].split(':')[0])
            del telethon_config

            global message_handlers
            await utils.mod.load_handlers([], message_handlers, "handlers", True)

            client.add_event_handler(event_handler, telethon.events.NewMessage)

            log.info("Started!")
            await client.run_until_disconnected()
    except sqlite3.OperationalError:
        log.error("Another instance of this bot is already running!")


if __name__ == '__main__':
    rich.traceback.install(show_locals=True)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Stopping... [KeyboardInterrupt]")

