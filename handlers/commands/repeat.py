import utils.cm
import utils.regex
import utils.ch
import handlers.cm


async def on_repeat(cm: utils.cm.CommandMessage):
    if cm.int_prev:
        msg_prev = cm.int_prev.message
        cm_new = await utils.cm.from_message(msg_prev)
        cm_new = cm_new._replace(sender=cm.sender)._replace(time=cm.time)._replace(local_time=cm.local_time)  # <- for rights, and other
        await handlers.cm.process_command_message(cm_new)


handler_list = [utils.ch.CommandHandler(
    name="repeat",
    pattern=utils.regex.command(utils.regex.unite("повтор", "заново", "repeat")),
    help_page=["repeat", "повтор"],
    handler_impl=on_repeat
)]
