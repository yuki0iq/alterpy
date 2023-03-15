import utils.regex
import utils.str
import utils.cm
import utils.ch
import utils.locale

handlers = []


async def on_layout(cm: utils.cm.CommandMessage):
    if cm.arg:
        await cm.int_cur.reply(utils.str.change_layout(cm.arg))


async def on_trl(cm: utils.cm.CommandMessage):
    if cm.arg:
        await cm.int_cur.reply(utils.locale.lang('en').tr(cm.arg))
        await cm.int_cur.reply(utils.locale.lang('ru').tr(cm.arg))


async def on_me(cm: utils.cm.CommandMessage):
    if cm.arg:
        msg = f"\* _{await cm.sender.get_display_name()} {cm.arg}_"
        if cm.int_prev:
            await cm.int_prev.reply(msg)
        else:
            await cm.int_cur.respond(msg)
        try:
            await cm.int_cur.delete()
        except:
            await cm.int_cur.reply("Can't delete message — no permission")


handlers.append(utils.ch.CommandHandler(
    name='layout',
    pattern=utils.regex.command(utils.regex.unite('kb', 'ли', 'layout', 'дфнщге', 'раскладка', 'hfcrkflrf', 'рас', 'hfc')),
    help_page=["keyboard", "клавиатура"],
    handler_impl=on_layout,
    is_prefix=True
))

handlers.append(utils.ch.CommandHandler(
    name='iuliia',
    pattern=utils.regex.command(utils.regex.unite('trl', 'translit', 'iuliia', 'трл', 'транслит', 'йуля')),
    help_page=["keyboard", "клавиатура"],
    handler_impl=on_trl,
    is_prefix=True
))

handlers.append(utils.ch.CommandHandler(
    name="me",
    pattern=utils.regex.pre_command(utils.regex.unite('me', 'я')),
    help_page=["keyboard", "клавиатура"],
    handler_impl=on_me,
    is_prefix=True
))
