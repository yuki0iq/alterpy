import utils.cm
import utils.ch
import utils.th
import re
import telethon.tl.custom.message
import asyncio
import utils.mod
import utils.help
import main


the_bot_id = main.the_bot_id
ch_list = []

utils.help.add(ch_list, "commands", "help", "command", "commands", is_eng=True)
utils.help.add(ch_list, "commands", "справка", "команда", "commands", is_eng=False)

initial_handlers = ch_list[:]
handlers_dir = "handlers/commands"


async def init():
    await utils.mod.load_handlers(initial_handlers, ch_list, handlers_dir)


async def process_command_message(cm: utils.cm.CommandMessage):
    media_type = cm.media.type()
    tasks = [
        asyncio.create_task(handler.invoke(
            utils.ch.apply(cm, handler) if handler.is_prefix else cm
        ))
        for handler in filter(
            lambda handler:
            bool(re.search(handler.pattern, cm.arg))
                and (media_type in handler.required_media_type
                     or not handler.required_media_type),
            ch_list
        )
    ]
    if tasks:
        await asyncio.wait(tasks)


async def on_command_message(msg: telethon.tl.custom.message.Message):
    if msg.sender_id == the_bot_id:  # Ignore messages from self
        return
    if msg.fwd_from is not None:  # Ignore forwarded messages
        return

    cm = await utils.cm.from_message(msg)
    await process_command_message(cm)


handler_list = [utils.th.TelethonHandler("command-message", on_command_message)]
