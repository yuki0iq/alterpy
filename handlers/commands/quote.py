import utils.cm
import utils.ch
import utils.regex
import utils.quote
import utils.common
import handlers.qdb


async def on_quote(cm: utils.cm.CommandMessage):
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


handler_list = [utils.ch.CommandHandler(
    name="quote",
    pattern=utils.regex.command(utils.regex.unite('q', 'й')),
    help_page=["quote", "цитатник"],
    handler_impl=on_quote,
    is_arg_current=True,
    is_prefix=True,
)]
