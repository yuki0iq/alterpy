import util
import asyncio
import re
import telethon

log = util.get_log("main")
log.info("AlterPy")

telethon_config = util.get_config("telethon_config.toml")
api_id = telethon_config['api_id']
api_hash = telethon_config['api_hash']
bot_token = telethon_config['bot_token']
client = telethon.TelegramClient("alterpy", api_id, api_hash)
client.start(bot_token=bot_token)
log.info("Started telethon instance")

# TODO load all CommandHandlers from external files
handlers = []


async def command_version(cm: util.CommandMessage):
    await cm.int_cur.respond("AlterPy 1 on Jan 26 of 2023 by Yuki the girl")


handlers.append(
    util.CommandHandler(
        name='ver',
        pattern=util.re_pat_starts_with('/ver'),
        help_message='Show AlterPy version',
        author='@yuki_the_girl',
        version=1,
        handler_impl=command_version,
        is_elevated=False,
        is_replaceable=False
    )
)


@client.on(telethon.events.NewMessage)
async def event_handler(event: telethon.events.NewMessage):
    cm = await util.to_command_message(event)
    await asyncio.wait([
        handler.invoke(cm)
        for handler
        in filter(
            lambda handler:
            bool(re.search(handler.pattern, cm.arg)),
            handlers
        )
    ])


log.info("Started!")
with client:
    client.run_until_disconnected()
