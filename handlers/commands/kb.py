import utils.regex
import utils.str
import utils.cm
import utils.ch
import utils.locale
import utils.common
import utils.kiri43i

handler_list = []


async def on_layout(cm: utils.cm.CommandMessage):
    if cm.arg:
        await cm.int_cur.reply(utils.str.escape(utils.str.change_layout(cm.arg)))


async def on_trl(cm: utils.cm.CommandMessage):
    if cm.arg:
        res = []
        for part in utils.common.split_by_func(cm.arg, utils.str.is_eng):
            if utils.str.is_eng(part):
                res.append(utils.locale.lang('ru').tr(part))
            else:
                res.append(utils.locale.lang('en').tr(part))
        await cm.int_cur.reply(utils.str.escape(utils.kiri43i.parse(''.join(res))))


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


handler_list.append(utils.ch.CommandHandler(
    name='layout',
    pattern=utils.regex.command(utils.regex.unite('kb', 'ли', 'layout', 'дфнщге', 'раскладка', 'hfcrkflrf', 'рас', 'hfc')),
    help_page=["keyboard", "клавиатура"],
    handler_impl=on_layout,
    is_prefix=True
))

handler_list.append(utils.ch.CommandHandler(
    name='iuliia',
    pattern=utils.regex.command(utils.regex.unite('trl', 'translit', 'iuliia', 'трл', 'транслит', 'йуля')),
    help_page=["keyboard", "клавиатура"],
    handler_impl=on_trl,
    is_prefix=True
))

handler_list.append(utils.ch.CommandHandler(
    name="me",
    pattern=utils.regex.pre_command(utils.regex.unite('me', 'я')),
    help_page=["irc", "ирка"],
    handler_impl=on_me,
    is_prefix=True
))
