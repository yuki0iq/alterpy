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

the_bot_id = int(bot_token.split(':')[0])


handlers = []


async def command_version(cm: util.CommandMessage):
    await cm.int_cur.reply("AlterPy 1 on Jan 26 of 2023 by Yuki the girl")


handlers.append(util.CommandHandler(
    name='ver',
    pattern=re.compile(util.re_pat_starts_with('/ver')),
    help_message='Show AlterPy version',
    author='@yuki_the_girl',
    handler_impl=command_version,
    is_elevated=False
))


commands_filenames = list(filter(lambda filename: filename[-3:] == ".py", sorted(util.list_files("commands/"))))
log.info(f"commands: {commands_filenames}")
for filename in commands_filenames:
    try:
        mod = importlib.import_module(f"commands.{filename[:-3]}")
        handlers.extend(mod.handlers)
    except:
        util.log_fail(log, f"Loading {filename} failed")


@client.on(telethon.events.NewMessage)
async def event_handler(event: telethon.events.NewMessage):
    if event.message.sender_id == the_bot_id:  # Ignore messages from self
        return

    cm = await util.to_command_message(event)
    tasks = [
        asyncio.create_task(handler.invoke(
            util.cm_apply(cm, handler.pattern) if handler.is_prefix else cm
        ))
        for handler in filter(
            lambda handler:
                bool(re.search(handler.pattern, cm.arg)),
            handlers
        )
    ]
    if tasks:
        await asyncio.wait(tasks)


log.info("Started!")
with client:
    client.run_until_disconnected()
