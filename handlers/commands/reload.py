import utils.cm
import utils.mod
import utils.ch
import utils.regex
import handlers.cm


async def on_reload(cm: utils.cm.CommandMessage):
    res = await utils.mod.load_handlers(
        handlers.cm.initial_handlers,
        handlers.cm.ch_list,
        handlers.cm.handlers_dir,
        True
    )
    await cm.int_cur.reply(res)


handler_list = [utils.ch.CommandHandler(
    name="reload",
    pattern=utils.regex.command(utils.regex.unite("перезапуск", "reload")),
    help_page='elevated',
    handler_impl=on_reload,
    is_elevated=True
)]
