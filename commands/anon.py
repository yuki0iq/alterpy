import utils.cm
import utils.common
import utils.ch
import utils.regex

handlers = []


async def on_set_anon_en(cm: utils.cm.CommandMessage):
    g = cm.sender.chat_id
    if cm.arg:
        g = utils.common.to_int(cm.arg, 0)
        if not g:
            await cm.int_cur.reply(f"Could not parse Chat ID")
            return
    cm.sender.add_anon_chat(g)
    await cm.int_cur.reply(f"Turned ON anon mode for chat {g}")


async def on_set_anon_ru(cm: utils.cm.CommandMessage):
    g = cm.sender.chat_id
    if cm.arg:
        g = utils.common.to_int(cm.arg, 0)
        if not g:
            await cm.int_cur.reply(f"Не получилось распознать ID чата")
            return
    cm.sender.add_anon_chat(g)
    await cm.int_cur.reply(f"Режим анонимности ВКЛЮЧЁН для чата с ID {g}")


async def on_get_anon_en(cm: utils.cm.CommandMessage):
    await cm.int_cur.reply(f"Anon mode is ON for {', '.join(map(str, cm.sender.get_anon_chats()))}")


async def on_get_anon_ru(cm: utils.cm.CommandMessage):
    await cm.int_cur.reply(f"Режим анонимности ВКЛЮЧЁН на чатах с ID {', '.join(map(str, cm.sender.get_anon_chats()))}")


async def on_reset_anon_en(cm: utils.cm.CommandMessage):
    cm.sender.reset_anon_chats()
    await cm.int_cur.reply("Anon chats are unset now")


async def on_del_anon_en(cm: utils.cm.CommandMessage):
    g = cm.sender.chat_id
    if cm.arg:
        g = utils.common.to_int(cm.arg, 0)
        if not g:
            await cm.int_cur.reply(f"Could not parse Chat ID")
            return
    cm.sender.del_anon_chat(g)
    await cm.int_cur.reply(f"Turned OFF anon mode for chat {g}")


async def on_del_anon_ru(cm: utils.cm.CommandMessage):
    g = cm.sender.chat_id
    if cm.arg:
        g = utils.common.to_int(cm.arg, 0)
        if not g:
            await cm.int_cur.reply(f"Не получилось распознать ID чата")
            return
    cm.sender.del_anon_chat(g)
    await cm.int_cur.reply(f"Режим анонимности ВЫКЛЮЧЕН для чата с ID {g}")


async def on_reset_anon_ru(cm: utils.cm.CommandMessage):
    cm.sender.reset_anon_chats()
    await cm.int_cur.reply("Список чатов с анонимностью сброшен")


handlers.append(utils.ch.CommandHandler(
    "+anon",
    utils.regex.raw_command("\\+anon"),
    ["anon", "анон"], on_set_anon_en, is_prefix=True, is_arg_current=True
))
handlers.append(utils.ch.CommandHandler(
    "+анон",
    utils.regex.raw_command("\\+анон"),
    ["anon", "анон"], on_set_anon_ru, is_prefix=True, is_arg_current=True
))
handlers.append(utils.ch.CommandHandler(
    "?anon",
    utils.regex.raw_command("\\?anon"),
    ["anon", "анон"], on_get_anon_en
))
handlers.append(utils.ch.CommandHandler(
    "?анон",
    utils.regex.raw_command("\\?анон"),
    ["anon", "анон"], on_get_anon_ru
))
handlers.append(utils.ch.CommandHandler(
    "!anon",
    utils.regex.raw_command("\\!anon"),
    ["anon", "анон"], on_reset_anon_en
))
handlers.append(utils.ch.CommandHandler(
    "!анон",
    utils.regex.raw_command("\\!анон"),
    ["anon", "анон"], on_reset_anon_ru
))
handlers.append(utils.ch.CommandHandler(
    "-anon",
    utils.regex.raw_command("-anon"),
    ["anon", "анон"], on_del_anon_en, is_prefix=True, is_arg_current=True
))
handlers.append(utils.ch.CommandHandler(
    "-анон",
    utils.regex.raw_command("-анон"),
    ["anon", "анон"], on_del_anon_ru, is_prefix=True, is_arg_current=True
))
