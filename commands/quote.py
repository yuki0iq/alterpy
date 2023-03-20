import sortedcollections
import utils.cm
import utils.ch
import utils.regex
import utils.quote


handlers = []

# chat_id -> [(msg_id, telethon message)] no more than 50
message_database: dict[int, sortedcollections.SortedDict] = {}
message_database_limit = 50


def add_message(message):
    msg_id = message.id
    chat_id = message.chat.id
    if chat_id not in message_database:
        message_database[chat_id] = sortedcollections.SortedDict()

    message_database[chat_id][msg_id] = message
    while len(message_database[chat_id]) > message_database_limit:
        message_database[chat_id].popitem(0)


async def on_quote(cm: utils.cm.CommandMessage):
    if not cm.reply_sender:
        await cm.int_cur.reply("Команде необходим прикрепленный ответ")
    else:
        cnt = int((cm.arg or '1').split()[0])
        start = message_database[cm.sender.chat_id].index(cm.reply_id)
        if cnt >= 0:
            le, ri = start, start + cnt
        else:
            le, ri = start + cnt + 1, start + 1
        messages = message_database[cm.sender.chat_id].values()[le:ri]
        quote_text = await utils.quote.create(messages, cm.sender.chat_id, cm.client)
        if quote_text[0] == ' ': quote_text = '.' + quote_text[1:]
        # .replace('(', '\\(').replace(')', '\\)').replace('[', '\\[').replace(']', '\\]')
        await cm.int_cur.reply('```' + quote_text + '```')


async def on_quote_database(cm: utils.cm.CommandMessage):
    add_message(cm.msg)
    if cm.reply_id != -1:
        add_message(await cm.msg.get_reply_message())


handlers.append(utils.ch.CommandHandler(
    name="quote",
    pattern=utils.regex.command(utils.regex.unite('q', 'й')),
    help_page=["quote", "цитатник"],
    handler_impl=on_quote,
    is_arg_current=True,
    is_prefix=True,

    is_elevated=True
))

handlers.append(utils.ch.CommandHandler(
    name="quote-database-handler",
    pattern=utils.regex.ignore_case(""),
    help_page=["quote", "цитатник"],
    handler_impl=on_quote_database,
))

