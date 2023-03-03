import utils

handlers = []


async def on_set_name_en(cm: utils.cm.CommandMessage):
    if cm.arg:
        cm.sender.set_name(cm.arg)
        await cm.int_cur.reply(f"Name set to {cm.arg}")
    else:
        await cm.int_cur.reply(f"Your name is {cm.sender.get_name() or 'not set'}")


async def on_set_name_ru(cm: utils.cm.CommandMessage):
    if cm.arg:
        cm.sender.set_name(cm.arg)
        await cm.int_cur.reply(f"Установлено имя {cm.arg}")
    else:
        await cm.int_cur.reply(f"Ваше имя — {cm.sender.get_name() or 'не установлено'}")


async def on_get_name_en(cm: utils.cm.CommandMessage):
    user = cm.reply_sender or cm.sender
    await cm.int_cur.reply(f"{await user.get_display_name()}'s name is {user.get_name() or 'not set'}")


async def on_get_name_ru(cm: utils.cm.CommandMessage):
    user = cm.reply_sender or cm.sender
    await cm.int_cur.reply(f"Имя пользователя {await user.get_display_name()} — {user.get_name() or 'не установлено'}")


async def on_reset_name_en(cm: utils.cm.CommandMessage):
    cm.sender.reset_name()
    await cm.int_cur.reply("Name is not set now")


async def on_reset_name_ru(cm: utils.cm.CommandMessage):
    cm.sender.reset_name()
    await cm.int_cur.reply("Имя сброшено")


async def on_set_gender_en(cm: utils.cm.CommandMessage):
    if cm.arg:
        g = utils.pronouns.from_str(cm.arg)
        cm.sender.set_pronouns(g)
        await cm.int_cur.reply(f"Pronoun set is {utils.pronouns.to_str_en(g)}")
    else:
        await cm.int_cur.reply(f"Your pronoun set is {utils.pronouns.to_str_en(cm.sender.get_pronouns())}")


async def on_set_gender_ru(cm: utils.cm.CommandMessage):
    if cm.arg:
        g = utils.pronouns.from_str(cm.arg)
        cm.sender.set_pronouns(g)
        await cm.int_cur.reply(f"Установлен набор местоимений {utils.pronouns.to_str_en(g)}")
    else:
        await cm.int_cur.reply(f"Ваш набор местоимений — {utils.pronouns.to_str_ru(cm.sender.get_pronouns())}")


async def on_get_gender_en(cm: utils.cm.CommandMessage):
    user = cm.reply_sender or cm.sender
    await cm.int_cur.reply(f"{await user.get_display_name()}'s pronoun set is {utils.pronouns.to_str_en(cm.sender.get_pronouns())}")


async def on_get_gender_ru(cm: utils.cm.CommandMessage):
    user = cm.reply_sender or cm.sender
    await cm.int_cur.reply(f"Набор местоимений {await user.get_display_name()} — {utils.pronouns.to_str_ru(cm.sender.get_pronouns())}")


async def on_reset_gender_en(cm: utils.cm.CommandMessage):
    cm.sender.reset_pronouns()
    await cm.int_cur.reply("Prounon set is unset now")


async def on_reset_gender_ru(cm: utils.cm.CommandMessage):
    cm.sender.reset_pronouns()
    await cm.int_cur.reply("Набор местоимений сброшен")


handlers.append(utils.ch.CommandHandler(
    "+name",
    utils.regex.raw_command("\\+name"),
    ["name", "имя"], on_set_name_en, is_prefix=True, is_arg_current=True
))
handlers.append(utils.ch.CommandHandler(
    "+имя",
    utils.regex.raw_command("\\+имя"),
    ["name", "имя"], on_set_name_ru, is_prefix=True, is_arg_current=True
))
handlers.append(utils.ch.CommandHandler(
    "?name",
    utils.regex.raw_command("\\?name"),
    ["name", "имя"], on_get_name_en
))
handlers.append(utils.ch.CommandHandler(
    "?имя",
    utils.regex.raw_command("\\?имя"),
    ["name", "имя"], on_get_name_ru
))
handlers.append(utils.ch.CommandHandler(
    "-name",
    utils.regex.raw_command("-name"),
    ["name", "имя"], on_reset_name_en
))
handlers.append(utils.ch.CommandHandler(
    "-имя",
    utils.regex.raw_command("-имя"),
    ["name", "имя"], on_reset_name_ru
))
handlers.append(utils.ch.CommandHandler(
    "+pn",
    utils.regex.raw_command("\\+pn"),
    ["name", "имя"], on_set_gender_en, is_prefix=True, is_arg_current=True
))
handlers.append(utils.ch.CommandHandler(
    "+мест",
    utils.regex.raw_command("\\+мест"),
    ["name", "имя"], on_set_gender_ru, is_prefix=True, is_arg_current=True
))
handlers.append(utils.ch.CommandHandler(
    "?pn",
    utils.regex.raw_command("\\?pn"),
    ["name", "имя"], on_get_gender_en
))
handlers.append(utils.ch.CommandHandler(
    "?мест",
    utils.regex.raw_command("\\?мест"),
    ["name", "имя"], on_get_gender_ru
))
handlers.append(utils.ch.CommandHandler(
    "-pn",
    utils.regex.raw_command("-pn"),
    ["name", "имя"], on_reset_gender_en
))
handlers.append(utils.ch.CommandHandler(
    "-мест",
    utils.regex.raw_command("-мест"),
    ["name", "имя"], on_reset_gender_ru
))
