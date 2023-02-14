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
        g = util.str_to_pronouns(cm.arg)
        cm.sender.set_pronouns(g)
        await cm.int_cur.reply(f"Pronoun set is {util.pronouns_to_str_en(g)}")
    else:
        await cm.int_cur.reply(f"Your pronoun set is {util.pronouns_to_str_en(cm.sender.get_pronouns())}")


async def on_set_gender_ru(cm: util.CommandMessage):
    if cm.arg:
        g = util.str_to_pronouns(cm.arg)
        cm.sender.set_pronouns(g)
        await cm.int_cur.reply(f"Установлен набор местоимений {util.pronouns_to_str_en(g)}")
    else:
        await cm.int_cur.reply(f"Ваш набор местоимений — {util.pronouns_to_str_ru(cm.sender.get_pronouns())}")


async def on_reset_gender_en(cm: util.CommandMessage):
    cm.sender.reset_pronouns()
    await cm.int_cur.reply("Prounon set is unset now")


async def on_reset_gender_ru(cm: util.CommandMessage):
    cm.sender.reset_pronouns()
    await cm.int_cur.reply("Набор местоимений сброшен")


handlers.append(util.CommandHandler(
    "+name",
    util.re_ignore_case(util.re_pat_starts_with("\\+name")),
    ["name", "имя"], on_set_name_en, is_prefix=True, is_arg_current=True
))
handlers.append(util.CommandHandler(
    "+имя",
    util.re_ignore_case(util.re_pat_starts_with("\\+имя")),
    ["name", "имя"], on_set_name_ru, is_prefix=True, is_arg_current=True
))
handlers.append(util.CommandHandler(
    "-name",
    util.re_ignore_case(util.re_pat_starts_with("-name")),
    ["name", "имя"], on_reset_name_en
))
handlers.append(util.CommandHandler(
    "-имя",
    util.re_ignore_case(util.re_pat_starts_with("-имя")),
    ["name", "имя"], on_reset_name_ru
))
handlers.append(util.CommandHandler(
    "+pn",
    util.re_ignore_case(util.re_pat_starts_with("\\+pn")),
    ["name", "имя"], on_set_gender_en, is_prefix=True, is_arg_current=True
))
handlers.append(util.CommandHandler(
    "+мест",
    util.re_ignore_case(util.re_pat_starts_with("\\+мест")),
    ["name", "имя"], on_set_gender_ru, is_prefix=True, is_arg_current=True
))
handlers.append(util.CommandHandler(
    "-pn",
    util.re_ignore_case(util.re_pat_starts_with("-pn")),
    ["name", "имя"], on_reset_gender_en
))
handlers.append(util.CommandHandler(
    "-мест",
    util.re_ignore_case(util.re_pat_starts_with("-мест")),
    ["name", "имя"], on_reset_gender_ru
))
