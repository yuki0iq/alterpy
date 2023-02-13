import util

import iuliia

handlers = []


async def on_layout(cm: util.CommandMessage):
    if cm.arg:
        await cm.int_cur.reply(util.change_layout(cm.arg))


async def on_trl(cm: util.CommandMessage):
    if cm.arg:
        await cm.int_cur.reply(iuliia.translate(cm.arg, iuliia.WIKIPEDIA))


async def on_me(cm: util.CommandMessage):
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


handlers.append(util.CommandHandler(
    name='layout',
    pattern=util.re_ignore_case(util.re_pat_starts_with(
        util.re_prefix() + util.re_unite('kb', 'ли', 'layout', 'дфнщге', 'раскладка', 'hfcrkflrf', 'рас', 'hfc')
    )),
    help_message="",
    help_message_en="Change keyboard layout (qwerty <-> йцукен)",
    help_message_ru="Сменить раскладку клавиатуры (qwerty <-> йцукен)",
    handler_impl=on_layout,
    is_prefix=True
))

handlers.append(util.CommandHandler(
    name='iuliia',
    pattern=util.re_ignore_case(util.re_pat_starts_with(
        util.re_prefix() + util.re_unite('trl', 'translit', 'iuliia', 'трл', 'транслит', 'йуля')
    )),
    help_message="",
    help_message_en="wikipedia-style iuliia transliterate (привет -> privet), habr.com/post/499574",
    help_message_ru="Транслитерация сообщения (привет -> privet) с помощью iuliia, habr.com/post/499574",
    handler_impl=on_trl,
    is_prefix=True
))

handlers.append(util.CommandHandler(
    name="me",
    pattern=util.re_ignore_case(util.re_pat_starts_with(util.re_only_prefix() + util.re_unite('me', 'я'))),
    help_message="",
    help_message_en="IRC-style /me command",
    help_message_ru="Команда /me как в IRC",
    handler_impl=on_me,
    is_prefix=True
))
