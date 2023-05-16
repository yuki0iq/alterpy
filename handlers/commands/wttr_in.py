import utils.cm
import utils.ch
import utils.log
import utils.regex
import utils.str
import utils.lang.ru
import context

import aiohttp
import json

handler_list = []


async def weather_ru(cm: utils.cm.CommandMessage):
    if not cm.arg:
        await cm.int_cur.reply('В пустоте погоды нет')
        return
    first_word = cm.arg.split()[0].lower()
    other = cm.arg[len(first_word):].strip()
    if first_word == 'в':
        arg = other
    elif first_word == 'у':
        arg = '~' + other
    else:
        arg = cm.arg
    async with context.session.get(f'https://v2.wttr.in/{arg.replace(" ", "+")}_lang=ru.png') as v2:
        data_v2 = await v2.read()
    await cm.int_cur.reply(f'Погода {utils.str.escape(cm.arg)}', data_v2) 


handler_list.append(
    utils.ch.CommandHandler(
        name='weather_ru',
        pattern=utils.regex.ignore_case(utils.regex.pat_starts_with(utils.regex.prefix() + utils.regex.unite('weather', 'погода'))),
        help_page=['weather', 'погода'],
        handler_impl=weather_ru,
        is_prefix=True
    )
)
