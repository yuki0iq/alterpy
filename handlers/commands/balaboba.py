import utils.cm
import utils.ch
import utils.log
import utils.regex
import utils.str

import utils.aiobalaboba
import aiohttp


handler_list = []

bbsession = aiohttp.ClientSession()
bb = utils.aiobalaboba.Balaboba(bbsession)
text_types = []


async def init():
    global text_types
    text_types = await bb.get_text_types(language="ru")
    utils.log.get("balaboba").info(f"Got types: {chr(10).join(map(str, text_types))}")


async def balaboba(cm: utils.cm.CommandMessage):
    if not cm.arg:
        await cm.int_cur.reply("Пустой запрос не хорошо")
        return
    await cm.int_cur.reply("Запрос обрабатывается, подождите...")
    try:
        res = await bb.balaboba(cm.arg, text_type=text_types[0])
    except aiohttp.ClientResponseError as e:
        res = "Балабоба не отвечает, наверное хочет ткнуть капчей в альтерпая"
        utils.log.get("balaboba").exception("balaboba request failed")
    await cm.int_cur.reply(utils.str.escape(res))


handler_list.append(
    utils.ch.CommandHandler(
        name='yalm-ru',
        pattern=utils.regex.pre(utils.regex.unite('yalm', 'бб')),
        help_page='yalm',
        handler_impl=balaboba,
        is_prefix=True
    )
)
