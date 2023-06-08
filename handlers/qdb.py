import sortedcollections
import telethon.tl.custom.message
import utils.th


# chat_id -> [(msg_id, telethon message)] no more than `message_database_limit`
message_database: dict[int, sortedcollections.SortedDict] = {}
message_database_limit = 50


def add_message(message: telethon.tl.custom.message.Message) -> None:
    msg_id = message.id
    chat_id = message.chat.id
    if chat_id not in message_database:
        message_database[chat_id] = sortedcollections.SortedDict()

    message_database[chat_id][msg_id] = message
    while len(message_database[chat_id]) > message_database_limit:
        message_database[chat_id].popitem(0)


async def on_quote_database(msg: telethon.tl.custom.message.Message) -> None:
    add_message(msg)
    rep = await msg.get_reply_message()
    if rep:
        add_message(rep)


handler_list = [utils.th.TelethonHandler("quote-database-handler", on_quote_database)]
