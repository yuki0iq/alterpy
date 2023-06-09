import utils.cm
import utils.ch
import utils.log
import utils.regex
import utils.str
import alterpy.context

import aiohttp
import json

handler_list = []


async def calend_ru(cm: utils.cm.CommandMessage) -> None:
    if isinstance(alterpy.context.session, aiohttp.ClientSession):
        async with alterpy.context.session.get('https://www.calend.ru/img/export/informer.png') as response:
            await cm.int_cur.reply('Праздники сегодня', await response.read())


handler_list.append(
    utils.ch.CommandHandler(
        name='calend_ru',
        pattern=utils.regex.cmd(utils.regex.unite('holidays', 'праздники')),
        help_page='calend',
        handler_impl=calend_ru,
        is_prefix=True
    )
)
