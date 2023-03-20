import utils.log
import utils.config
import utils.cm
import utils.ch
import utils.regex
import utils.help
import utils.file
import utils.mod
import utils.common
import utils.quote

import asyncio
import re
import telethon
import traceback

import rich.traceback
rich.traceback.install(show_locals=True)


log = utils.log.get("main")
log.info("AlterPy")


telethon_config = utils.config.load("telethon_config.toml")
client = telethon.TelegramClient("alterpy", telethon_config['api_id'], telethon_config['api_hash'])
client.start(bot_token=telethon_config['bot_token'])
log.info("Started telethon instance")

the_bot_id = int(telethon_config['bot_token'].split(':')[0])
del telethon_config


handlers, initial_handlers = [], []


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
        lined_code = '\n'.join(f"{i+1:02}  {code_lines[i]}" for i in range(len(code_lines)))
        await cm.int_cur.reply(f"While executing following code:\n```{lined_code}```")


handlers.append(utils.ch.CommandHandler(
    name="exec",
    pattern=utils.regex.command("exec"),
    help_page=["elevated", "повышенные"],
    handler_impl=on_exec,
    is_prefix=True,
    is_elevated=True
))


async def on_repeat(cm: utils.cm.CommandMessage):
    if cm.int_prev:
        msg_prev = cm.int_prev.message
        cm_new = await utils.cm.from_message(msg_prev)
        cm_new = cm_new._replace(sender=cm.sender)._replace(time=cm.time)._replace(local_time=cm.local_time)  # <- for rights, and other
        await process_command_message(cm_new)


handlers.append(utils.ch.CommandHandler(
    name="repeat",
    pattern=utils.regex.command(utils.regex.unite("повтор", "заново", "repeat")),
    help_page=["repeat", "повтор"],
    handler_impl=on_repeat
))


async def on_reload(cm: utils.cm.CommandMessage):
    global handlers
    global initial_handlers
    res = await utils.mod.load_handlers(initial_handlers, handlers, "commands")
    await cm.int_cur.reply(res)


handlers.append(utils.ch.CommandHandler(
    name="reload",
    pattern=utils.regex.command(utils.regex.unite("перезапуск", "reload")),
    help_page=["elevated", "повышенные"],
    handler_impl=on_reload,
    is_elevated=True
))


utils.help.add(handlers, "commands", "help", "command", "commands", is_eng=True)
utils.help.add(handlers, "commands", "справка", "команда", "commands", is_eng=False)

initial_handlers[:] = handlers[:]

asyncio.get_event_loop().run_until_complete(utils.mod.load_handlers(initial_handlers, handlers, "commands"))


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


@client.on(telethon.events.NewMessage)
async def event_handler(event: telethon.events.NewMessage):
    if event.message.sender_id == the_bot_id:  # Ignore messages from self
        return
    if event.message.fwd_from is not None:  # Ignore forwarded messages
        return

    cm = await utils.cm.from_event(event)
    await process_command_message(cm)


log.info("Started!")
with client:
    client.run_until_disconnected()
