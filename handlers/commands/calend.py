import utils.cm
import utils.ch
import utils.log
import utils.regex
import utils.str

import aiohttp
import json

handler_list = []
session = None


async def init():
    global session
    session = aiohttp.ClientSession()


async def calend_ru(cm: utils.cm.CommandMessage):
    async with session.get('https://www.calend.ru/img/export/informer.png') as response:
        await cm.int_cur.reply('Праздники сегодня', await response.read())


handler_list.append(
    utils.ch.CommandHandler(
        name='calend_ru',
        pattern=utils.regex.ignore_case(utils.regex.pat_starts_with(utils.regex.prefix() + utils.regex.unite('holidays', 'праздники'))),
        help_page=['holidays', 'праздники'],
        handler_impl=calend_ru,
        is_prefix=True
    )
)
