import utils.cm
import utils.ch
import utils.log
import utils.regex
import utils.str
import utils.locale
import context

import aiohttp
import json

handler_list = []


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
    }
}
LOC = utils.locale.Localizator(translations)


def weather(lang: str):
    async def weather_impl(cm: utils.cm.CommandMessage):
        if not cm.arg:
            await cm.int_cur.reply(LOC.obj('no', lang))
            return
        await cm.int_cur.reply(LOC.obj('wait', lang))
        words = ' '.join(cm.arg.split()).lower()
        other_dic = {True: cm.arg} | dict([(words.startswith(w), words[len(w):]) for w in LOC.obj('in', lang)]) | dict([(words.startswith(w), '~' + words[len(w):]) for w in LOC.obj('near', lang)])
        arg = other_dic[True]
        argp = arg.strip().replace(' ', '+')
        error_str = '>>>   404'
        async with context.session.get(f'https://v1.wttr.in/{argp}?T0') as v1:
            data_v1 = await v1.read()
        if error_str in data_v1.decode():
            await cm.int_cur.reply(LOC.obj('err', lang))
            return
        async with context.session.get(f'https://v2.wttr.in/{argp}_lang={lang}.png') as v2:
            data_v2 = await v2.read()
        await cm.int_cur.reply(' '.join([LOC.obj('weather', lang), utils.str.escape(cm.arg)]), data_v2) 
    return weather_impl


handler_list.extend(
    utils.ch.CommandHandler(
        name=f'weather-{lang}',
        pattern=utils.regex.ignore_case(utils.regex.pat_starts_with(utils.regex.prefix() + command)),
        help_page='wttrin',
        handler_impl=weather(lang),
        is_prefix=True
    )
    for lang, command in [
        ('ru', 'погода'),
        ('en', 'weather'),
    ]
)
