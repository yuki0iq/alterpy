import re

import util

handlers = []


async def on_set_name_en(cm: util.CommandMessage):
    if cm.arg:
        cm.sender.set_name(cm.arg)
        await cm.int_cur.reply(f"Name set to {cm.arg}")
    else:
        await cm.int_cur.reply(f"Your name is {cm.sender.get_name() or 'not set'}")


async def on_set_name_ru(cm: util.CommandMessage):
    if cm.arg:
        cm.sender.set_name(cm.arg)
        await cm.int_cur.reply(f"Установлено имя {cm.arg}")
    else:
        await cm.int_cur.reply(f"Ваше имя — {cm.sender.get_name() or 'не установлено'}")


async def on_reset_name_en(cm: util.CommandMessage):
    cm.sender.reset_name()
    await cm.int_cur.reply("Name is not set now")


async def on_reset_name_ru(cm: util.CommandMessage):
    cm.sender.reset_name()
    await cm.int_cur.reply("Имя сброшено")


handlers.append(util.CommandHandler("+name", re.compile(util.re_pat_starts_with("\\+?name")), "Set or show name", "@yuki_the_girl", on_set_name_en, is_prefix=True))
handlers.append(util.CommandHandler("+имя", re.compile(util.re_pat_starts_with("\\+?имя")), "Изменить или показать имя", "@yuki_the_girl", on_set_name_ru, is_prefix=True))
handlers.append(util.CommandHandler("-name", re.compile(util.re_pat_starts_with("-name")), "Reset name", "@yuki_the_girl", on_reset_name_en))
handlers.append(util.CommandHandler("-имя", re.compile(util.re_pat_starts_with("-имя")), "Сбросить имя", "@yuki_the_girl", on_reset_name_ru))
