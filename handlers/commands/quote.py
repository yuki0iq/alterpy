import utils.cm
import utils.ch
import utils.regex
import utils.quote
import utils.common
import utils.user
import handlers.qdb


async def on_quote(cm: utils.cm.CommandMessage) -> None:
    chat = await utils.user.from_telethon(None, cm.msg.chat, cm.client)
    chat_config = chat.load_user_config()
    if chat_config.get('disable_quote'):
        return

    if not cm.reply_sender:
        await cm.int_cur.reply("Команде необходим прикрепленный ответ")
    else:
        cnt = utils.common.to_int((cm.arg or '1').split()[0], 1)
        try:
            start = handlers.qdb.message_database[cm.sender.chat_id].index(cm.reply_id)
        except ValueError:
            await cm.int_cur.reply("Сообщение слишком старое")
            return

        if cnt >= 0:
            le, ri = start, start + cnt
        else:
            le, ri = start + cnt + 1, start + 1
        messages = handlers.qdb.message_database[cm.sender.chat_id].values()[le:ri]
        quote_text = await utils.quote.create(messages, cm.sender.chat_id, cm.client)
        if quote_text[0] == ' ': quote_text = '.' + quote_text[1:]
        # .replace('(', '\\(').replace(')', '\\)').replace('[', '\\[').replace(']', '\\]')
        await cm.int_cur.reply('```' + quote_text + '```')


async def on_quote_toggle(cm: utils.cm.CommandMessage) -> None:
    chat = await utils.user.from_telethon(None, cm.msg.chat, cm.client)
    chat_config = chat.load_user_config()
    chat_config["disable_quote"] = not chat_config.get("disable_quote")
    chat.save_user_config(chat_config)
    if chat_config.get("disable_quote"):
        await cm.int_cur.reply("Цитаты теперь выключены")
    else:
        await cm.int_cur.reply("Цитаты теперь включены")


handler_list = [utils.ch.CommandHandler(
    name="quote",
    pattern=utils.regex.cmd(utils.regex.unite('q', 'й')),
    help_page="quote",
    handler_impl=on_quote,
    is_arg_current=True,
    is_prefix=True,
), utils.ch.CommandHandler(
    name="quote_config",
    pattern=utils.regex.pre("quote_toggle"),
    help_page="quote",
    handler_impl=on_quote_toggle,
    is_arg_current=True,
    is_prefix=True,
)]

