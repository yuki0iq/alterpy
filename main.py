import util
import asyncio
import re
import telethon
import importlib

log = util.get_log("main")
log.info("AlterPy")

telethon_config = util.get_config("telethon_config.toml")
api_id = telethon_config['api_id']
api_hash = telethon_config['api_hash']
bot_token = telethon_config['bot_token']
client = telethon.TelegramClient("alterpy", api_id, api_hash)
client.start(bot_token=bot_token)
log.info("Started telethon instance")


handlers = []


def append_handler(*args, **kwargs):
    handlers.append(util.CommandHandler(*args, **kwargs))


async def command_version(cm: util.CommandMessage):
    await cm.int_cur.reply("AlterPy 1 on Jan 26 of 2023 by Yuki the girl")


append_handler(
    name='ver',
    pattern=util.re_pat_starts_with('/ver'),
    help_message='Show AlterPy version',
    author='@yuki_the_girl',
    version=1,
    handler_impl=command_version,
    is_elevated=False
)


commands_filenames = list(filter(lambda filename: filename[-3:] == ".py", sorted(util.list_files("commands/"))))
log.info(f"commands: {commands_filenames}")
for filename in commands_filenames:
    mod = importlib.import_module(f"commands.{filename[:-3]}")
    handlers.extend(mod.handlers)


@client.on(telethon.events.NewMessage)
async def event_handler(event: telethon.events.NewMessage):
    cm = await util.to_command_message(event)
    filtered_handlers = list(filter(
        lambda handler:
            bool(re.search(handler.pattern, cm.arg)),
        handlers
    ))
    if len(filtered_handlers):
        await asyncio.wait([
            asyncio.create_task(handler.invoke(cm))
            for handler in filtered_handlers
        ])


log.info("Started!")
with client:
    client.run_until_disconnected()
