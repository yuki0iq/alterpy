import utils.log
import utils.config
import utils.mod
import sqlite3
import asyncio
import telethon.events
import telethon.tl.custom.message
import rich.traceback


the_bot_id = 0
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


def main():
    log = utils.log.get("main")
    log.info("AlterPy")

    telethon_config = utils.config.load("telethon_config.toml")
    client = telethon.TelegramClient("alterpy", telethon_config['api_id'], telethon_config['api_hash'])
    try:
        client.start(bot_token=telethon_config['bot_token'])
        log.info("Started telethon instance")
    except sqlite3.OperationalError:
        log.error("Another instance of this bot is already running!")

    global the_bot_id
    the_bot_id = int(telethon_config['bot_token'].split(':')[0])
    del telethon_config

    global message_handlers
    asyncio.get_event_loop().run_until_complete(utils.mod.load_handlers([], message_handlers, "handlers", True))

    client.add_event_handler(event_handler, telethon.events.NewMessage)

    log.info("Started!")
    with client:
        client.run_until_disconnected()


if __name__ == '__main__':
    rich.traceback.install(show_locals=True)
    main()
