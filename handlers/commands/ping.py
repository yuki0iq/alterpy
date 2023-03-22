import utils.cm
import utils.time
import utils.system
import utils.ch
import utils.regex
import utils.locale
import utils.lang.ru
import utils.common

import datetime
import zoneinfo

handler_list = []

start_time = datetime.datetime.now(datetime.timezone.utc)

tzMSK = zoneinfo.ZoneInfo("Europe/Moscow")
tzMSK2 = zoneinfo.ZoneInfo("Asia/Yekaterinburg")
tzMSK4 = zoneinfo.ZoneInfo("Asia/Krasnoyarsk")

time_format = "(%Z) %Y-%m-%d, %H:%M:%S"

translations = {
    'ping_message': {
        'en': '**{rep}**. Ping is {ping}, handled in {handle}\nUp for {up}',
        'ru': '**{rep}**. Пинг — {ping}, обработка — {handle}\nНе падает, работает {up}!',
    },
    'ping_reply': {
        'en': 'PONG',
        'ru': 'ПОНГ',
    },
    'test_reply': {
        'en': 'PASSED',
        'ru': 'ПРОЙДЕН',
    },
    'stat_message': {
        'en': '''——— AlterPy ———
Running on `{system_info}`
Ping is _{ping}_, handled in _{handle}_
Up for _{up}_
Compute speed is _{speed}M_ operations per second
This chat ID is `{cm.sender.chat_id}`

— Current time is —
`{cur_time.astimezone(tzMSK).strftime(time_format)}`
`{cur_time.astimezone(tzMSK2).strftime(time_format)}`
`{cur_time.astimezone(tzMSK4).strftime(time_format)}`
— Started at —
`{start_time.astimezone(tzMSK).strftime(time_format)}`
`{start_time.astimezone(tzMSK2).strftime(time_format)}`
`{start_time.astimezone(tzMSK4).strftime(time_format)}`''',
        'ru': '''——— АльтерПай ———
Запущена на `{system_info}`
Пинг — _{ping}_, обработка — _{handle}_
Не падает, работает _{up}_
Скорость вычислений — _{speed}M_ операций в секунду
ID чата — `{cm.sender.chat_id}`

— Текущее время —
`{cur_time.astimezone(tzMSK).strftime(time_format)}`
`{cur_time.astimezone(tzMSK2).strftime(time_format)}`
`{cur_time.astimezone(tzMSK4).strftime(time_format)}`
— Время запуска —
`{start_time.astimezone(tzMSK).strftime(time_format)}`
`{start_time.astimezone(tzMSK2).strftime(time_format)}`
`{start_time.astimezone(tzMSK4).strftime(time_format)}`''',
    }
}
LOC = utils.locale.Localizator(translations)


def get_ping_times(cm: utils.cm.CommandMessage, lang: str):
    """return ping, handle and up formatted times"""
    cur_time = datetime.datetime.now(datetime.timezone.utc)

    ping = cm.local_time - cm.time
    handle = cur_time - cm.local_time
    up = cur_time - start_time

    ping_s = utils.time.timedelta_to_str(ping, is_short=True, lang=lang)
    handle_s = utils.time.timedelta_to_str(handle, is_short=True, lang=lang)
    up_s = utils.time.timedelta_to_str(up, lang=lang, form={"accs"})
    return ping_s, handle_s, up_s


def on_ping_wrapper(s: str, lang: str):
    async def on_ping(cm: utils.cm.CommandMessage):
        ping, handle, up = get_ping_times(cm, lang)
        rep = eval(LOC.get(s + '_reply', lang))
        msg = eval(LOC.get('ping_message', lang))
        await cm.int_cur.reply(msg)
    return on_ping


def on_stat_wrapper(lang: str):
    async def on_stat(cm: utils.cm.CommandMessage):
        cur_time = datetime.datetime.now(datetime.timezone.utc)
        ping, handle, up = get_ping_times(cm, lang=lang)
        speed = utils.system.perf_test_compute()
        system_info = utils.system.system_info()
        msg = eval(LOC.get('stat_message', lang))
        await cm.int_cur.reply(msg)
    return on_stat


handler_list.extend(
    utils.ch.CommandHandler(
        name=msg,
        pattern=utils.regex.command(msg + '$'),
        help_page=["ping", "пинг"],
        handler_impl=on_ping_wrapper(s, lang),
        is_elevated=False
    ) for msg, s, lang in [
        ("ping", "ping", 'en'),
        ("пинг", "ping", 'ru'),
        ("test", "test", 'en'),
        ("тест", "test", 'ru')
    ]
)

handler_list.extend(
    utils.ch.CommandHandler(
        name=msg,
        pattern=utils.regex.command(msg + '$'),
        help_page=["stat", "стат"],
        handler_impl=on_stat_wrapper(lang),
        is_elevated=False
    ) for msg, lang in [
        ("stat", 'en'),
        ("стат", 'ru'),
    ]
)

handler_list.extend(
    utils.ch.simple_reply(msg, ans, help_page=["ping", "пинг"], pattern=utils.regex.ignore_case(pat))
    for msg, ans, pat in [
        ("bot", "I'm here!", utils.regex.pat_starts_with("bot$")),
        ("бот", "На месте!", utils.regex.pat_starts_with("бот$")),
        ("ты где", "Я тут", utils.regex.pat_starts_with("(ты где)|(где ты)$")),
        ("сдох", "Ты тоже.", utils.regex.pat_starts_with("сдох\\?$")),
        ("слава партии", "Слава Партии!", utils.regex.pat_starts_with("слава партии[\\?!]*")),
        ("кто здесь власть", "ПАРТИЯ!", utils.regex.pat_starts_with("кто здесь власть[\\?]*")),
    ]
)
