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


async def on_set_gender_en(cm: util.CommandMessage):
    if cm.arg:
        g = util.str_to_gender(cm.arg)
        cm.sender.set_gender(g)
        await cm.int_cur.reply(f"Gender set to {util.gender_to_str_en(g)}")
    else:
        await cm.int_cur.reply(f"Your gender is {util.gender_to_str_en(cm.sender.get_gender())}")


async def on_set_gender_ru(cm: util.CommandMessage):
    if cm.arg:
        g = util.str_to_gender(cm.arg)
        cm.sender.set_gender(g)
        await cm.int_cur.reply(f"Установлен гендер {util.gender_to_str_ru(g)}")
    else:
        await cm.int_cur.reply(f"Ваш гендер — {util.gender_to_str_ru(cm.sender.get_gender())}")


async def on_reset_gender_en(cm: util.CommandMessage):
    cm.sender.set_gender(0)
    await cm.int_cur.reply("Gender is not set now")


async def on_reset_gender_ru(cm: util.CommandMessage):
    cm.sender.set_gender(0)
    await cm.int_cur.reply("Гендер сброшен")


handlers.append(util.CommandHandler("+name", re.compile(util.re_pat_starts_with("\\+?name")), "Set or show name", "@yuki_the_girl", on_set_name_en, is_prefix=True))
handlers.append(util.CommandHandler("+имя", re.compile(util.re_pat_starts_with("\\+?имя")), "Изменить или показать имя", "@yuki_the_girl", on_set_name_ru, is_prefix=True))
handlers.append(util.CommandHandler("-name", re.compile(util.re_pat_starts_with("-name")), "Reset name", "@yuki_the_girl", on_reset_name_en))
handlers.append(util.CommandHandler("-имя", re.compile(util.re_pat_starts_with("-имя")), "Сбросить имя", "@yuki_the_girl", on_reset_name_ru))
handlers.append(util.CommandHandler("+gender", re.compile(util.re_pat_starts_with("\\+?gen(der){0,1}")), "Set or show gender", "@yuki_the_girl", on_set_gender_en, is_prefix=True))
handlers.append(util.CommandHandler("+гендер", re.compile(util.re_pat_starts_with("\\+?ген(дер){0,1}")), "Изменить или показать гендер", "@yuki_the_girl", on_set_gender_ru, is_prefix=True))
handlers.append(util.CommandHandler("-gender", re.compile(util.re_pat_starts_with("-gen(der){0,1}")), "Reset gender", "@yuki_the_girl", on_reset_gender_en))
handlers.append(util.CommandHandler("-гендер", re.compile(util.re_pat_starts_with("-ген(дер){0,1}")), "Сбросить гендер", "@yuki_the_girl", on_reset_gender_ru))
