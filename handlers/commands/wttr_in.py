import utils.cm
import utils.ch
import utils.log
import utils.regex
import utils.str
import utils.locale
import utils.wttrin_png
import alterpy.context
import typing
import aiohttp
import asyncio
import json


translations = {
    'in': {
        'ru': ['в'],
        'en': ['in'],
    },
    'near': {
        'ru': ['рядом с', 'у'],
        'en': ['near'],
    },
    'no': {
        'ru': 'В пустоте погоды нет',
        'en': 'Location is required',
    },
    'weather': {
        'ru': 'Погода',
        'en': 'Weather',
    },
    'err': {
        'ru': 'Место не найдено',
        'en': 'Place not found',
    },
    'wait': {
        'ru': 'Запрос обрабатывается, подождите...',
        'en': 'Please wait for weather report to generate...',
    },
    'off': {
        'ru': 'wttr.in, кажется, упал',
        'en': 'wttr.in is probably down',
    },
}
LOC = utils.locale.Localizator(translations)


async def weather(cm: utils.cm.CommandMessage) -> None:
    if not isinstance(alterpy.context.session, aiohttp.ClientSession):
        return

    if not cm.arg:
        await cm.int_cur.reply(LOC.obj('no', cm.lang))
        return

    await cm.int_cur.reply(LOC.obj('wait', cm.lang))

    words = ' '.join(cm.arg.split()).lower()
    other_dic = {True: cm.arg} | dict([(words.startswith(w), words[len(w):]) for w in LOC.obj('in', cm.lang)]) | dict([
        (words.startswith(w), '~' + words[len(w):]) for w in LOC.obj('near', cm.lang)])

    arg = other_dic[True]
    argp = arg.strip().replace(' ', '+')

    try:
        error_str = '>>>   404'
        async with alterpy.context.session.get(f'https://v1.wttr.in/{argp}') as v1:
            data_v1 = await v1.read()

        if error_str in data_v1.decode():
            await cm.int_cur.reply(LOC.obj('err', cm.lang))
            return

        # async with alterpy.context.session.get(f'https://v2.wttr.in/{argp}_lang={cm.lang}') as v2:
        #     data_v2 = await v2.read()
        data_v2 = utils.wttrin_png.render_ansi(data_v1.decode('utf-8'))

        await cm.int_cur.reply(' '.join([LOC.obj('weather', cm.lang), utils.str.escape(cm.arg)]), data_v2)
    except asyncio.TimeoutError:
        await cm.int_cur.reply(LOC.obj('off', cm.lang))


handler_list = [
    utils.ch.CommandHandler(
        name=f'weather',
        pattern=utils.regex.cmd(utils.regex.unite("погода", "weather")),
        help_page='wttrin',
        handler_impl=weather,
        is_prefix=True
    )
]
