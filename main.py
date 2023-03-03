import utils

import asyncio
import re
import telethon
import importlib
import traceback

log = utils.log.get("main")
log.info("AlterPy")


telethon_config = utils.config.load("telethon_config.toml")
client = telethon.TelegramClient("alterpy", telethon_config['api_id'], telethon_config['api_hash'])
client.start(bot_token=telethon_config['bot_token'])
log.info("Started telethon instance")

the_bot_id = int(telethon_config['bot_token'].split(':')[0])
del telethon_config


handlers = []


async def on_command_version(cm: utils.cm.CommandMessage):
    await cm.int_cur.reply("AlterPy on Feb 13 of 2023 by Yuki the girl")


handlers.append(utils.ch.CommandHandler(
    name='ver',
    pattern=utils.regex.pre_command('ver'),
    help_page=["start", "начало"],
    handler_impl=on_command_version,
    is_elevated=False
))


async def on_exec(cm: utils.cm.CommandMessage):
    shifted_arg = cm.arg.strip().strip('`').replace('\n', '\n    ')
    code = '\n'.join([
        f"async def func():",
        f"    {shifted_arg}",
    ])
    try:
        code_locals = dict()
        exec(code, globals() | locals(), code_locals)
        await code_locals['func']()
    except:
        await cm.int_cur.reply(f"```{traceback.format_exc()}```")
        code_lines = code.split('\n')
        lined_code = '\n'.join(f"{i+1}  {code_lines[i]}" for i in range(len(code_lines)))
        await cm.int_cur.reply(f"While executing following code:\n```{lined_code}```")


handlers.append(utils.ch.CommandHandler(
    name="exec",
    pattern=utils.regex.command("exec"),
    help_page=["elevated", "повышенные"],
    handler_impl=on_exec,
    is_prefix=True,
    is_elevated=True
))

utils.help.add(handlers, "commands", "help", ".", is_eng=True)
utils.help.add(handlers, "commands", "справка", ".", is_eng=False)

initial_handlers = handlers[:]


def load_commands():
    global handlers
    handlers[:] = initial_handlers[:]
    commands_filenames = list(filter(lambda filename: filename[-3:] == ".py", sorted(utils.file.list_files("commands/"))))
    log.info(f"commands: {commands_filenames}")
    for filename in commands_filenames:
        try:
            mod = importlib.import_module(f"commands.{filename[:-3]}")
            handlers.extend(mod.handlers)
        except:
            utils.log.fail(log, f"Loading {filename} failed")


async def process_command_message(cm: utils.cm.CommandMessage):
    tasks = [
        asyncio.create_task(handler.invoke(
            utils.ch.apply(cm, handler) if handler.is_prefix else cm
        ))
        for handler in filter(
            lambda handler:
            bool(re.search(handler.pattern, cm.arg))
                and (cm.media.type() in handler.required_media_type
                     or not handler.required_media_type),
            handlers
        )
    ]
    if tasks:
        await asyncio.wait(tasks)


load_commands()


@client.on(telethon.events.NewMessage)
async def event_handler(event: telethon.events.NewMessage):
    if event.message.sender_id == the_bot_id:  # Ignore messages from self
        return

    cm = await utils.cm.from_event(event)
    await process_command_message(cm)


log.info("Started!")
with client:
    client.run_until_disconnected()
