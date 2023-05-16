import utils.cm
import utils.ch
import utils.log
import utils.regex
import utils.str
import context

import aiohttp
import json

handler_list = []


async def weather_ru(cm: utils.cm.CommandMessage):
    if not cm.arg:
        await cm.int_cur.reply('В пустоте погоды нет')
        return
    async with context.session.get(f'https://v2.wttr.in/{cm.arg.replace(" ", "+")}_lang=ru.png') as v2:
        data_v2 = await v2.read()
    await cm.int_cur.reply(f'Погода в {utils.str.escape(cm.arg)}', data_v2) 


handler_list.append(
    utils.ch.CommandHandler(
        name='weather_ru',
        pattern=utils.regex.ignore_case(utils.regex.pat_starts_with(utils.regex.prefix() + utils.regex.unite('weather', 'погода'))),
        help_page=['weather', 'погода'],
        handler_impl=weather_ru,
        is_prefix=True
    )
)
