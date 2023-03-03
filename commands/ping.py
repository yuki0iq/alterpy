import utils.cm
import utils.time
import utils.system
import utils.ch
import utils.regex

import datetime
import zoneinfo

handlers = []

start_time = datetime.datetime.now(datetime.timezone.utc)

tzMSK = zoneinfo.ZoneInfo("Europe/Moscow")
tzMSK2 = zoneinfo.ZoneInfo("Asia/Yekaterinburg")
tzMSK4 = zoneinfo.ZoneInfo("Asia/Krasnoyarsk")

time_format = "(%Z) %Y-%m-%d, %H:%M:%S"


def get_ping_times(cm: utils.cm.CommandMessage):
    """return ping, handle and up formatted times"""
    cur_time = datetime.datetime.now(datetime.timezone.utc)

    ping = cm.local_time - cm.time
    handle = cur_time - cm.local_time
    up = cur_time - start_time

    ping_s = utils.time.timedelta_to_str(ping, is_short=True)
    handle_s = utils.time.timedelta_to_str(handle, is_short=True)
    up_s = utils.time.timedelta_to_str(up)
    return ping_s, handle_s, up_s


def on_ping_wrapper(rep: str):
    async def on_ping(cm: utils.cm.CommandMessage):
        ping, handle, up = get_ping_times(cm)
        await cm.int_cur.reply(f"**{rep}**. Ping is {ping}, handled in {handle}\nUp for {up}")
    return on_ping


async def on_stat(cm: utils.cm.CommandMessage):
    cur_time = datetime.datetime.now(datetime.timezone.utc)
    ping, handle, up = get_ping_times(cm)
    speed = utils.system.perf_test_compute()
    system_info = utils.system.system_info()

    await cm.int_cur.reply('\n'.join([
        f'```--- AlterPy ---',
        f'Running on {system_info}',
        f'Ping is {ping}, handled in {handle}',
        f'Up for {up}',
        f'Compute speed is {speed}M operations per second',
        f'This chat ID is {cm.sender.chat_id}',
        f'',
        f'--- Current time is ---',
        f'{cur_time.astimezone(tzMSK).strftime(time_format)}',
        f'{cur_time.astimezone(tzMSK2).strftime(time_format)}',
        f'{cur_time.astimezone(tzMSK4).strftime(time_format)}',
        f'--- Started at ---',
        f'{start_time.astimezone(tzMSK).strftime(time_format)}',
        f'{start_time.astimezone(tzMSK2).strftime(time_format)}',
        f'{start_time.astimezone(tzMSK4).strftime(time_format)}```',
    ]))


handlers.extend(
    utils.ch.CommandHandler(
        name=msg,
        pattern=utils.regex.command(msg + '$'),
        help_page=["ping", "пинг"],
        handler_impl=on_ping_wrapper(ans),
        is_elevated=False
    ) for msg, ans in [
        ("ping", "PONG"),
        ("пинг", "ПОНГ"),
        ("test", "PASSED"),
        ("тест", "ПРОЙДЕН")
    ]
)

handlers.append(utils.ch.CommandHandler(
    name='stat',
    pattern=utils.regex.command(utils.regex.unite('stat', 'стат')),
    help_page=["stat", "стат"],
    handler_impl=on_stat
))

handlers.extend(
    utils.ch.simple_reply(msg, ans, help_page=["ping", "пинг"], pattern=utils.regex.ignore_case(pat))
    for msg, ans, pat in [
        ("bot", "I'm here!", utils.regex.pat_starts_with("bot$")),
        ("бот", "На месте!", utils.regex.pat_starts_with("бот$")),
        ("ты где", "Я тут", utils.regex.pat_starts_with("(ты где)|(где ты)$")),
        ("сдох", "Ты тоже.", utils.regex.pat_starts_with("сдох\\?$")),
        ("слава партии", "Слава Партии!", utils.regex.pat_starts_with("слава партии[?!]*")),
        ("кто здесь власть", "ПАРТИЯ!", utils.regex.pat_starts_with("кто здесь власть")),
    ]
)
