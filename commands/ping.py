import util

import datetime
import zoneinfo

handlers = []

start_time = datetime.datetime.now(datetime.timezone.utc)

tzMSK = zoneinfo.ZoneInfo("Europe/Moscow")
tzMSK4 = zoneinfo.ZoneInfo("Asia/Krasnoyarsk")

time_format = "(%Z) %Y-%m-%d, %H:%M:%S"


def on_ping_wrapper(rep: str):
    async def on_ping(cm: util.CommandMessage):
        cur_time = datetime.datetime.now(datetime.timezone.utc)

        ping = cm.local_time - cm.time
        handle = cur_time - cm.local_time
        up = cur_time - start_time

        ping_s = util.timedelta_to_str(ping, is_short=True)
        handle_s = util.timedelta_to_str(handle, is_short=True)
        up_s = util.timedelta_to_str(up)

        await cm.int_cur.reply(
            f"**{rep}**. Ping is {ping_s}, handled in {handle_s}\n"
            + f"Up for {up_s}\n"
            + f"\n"
            + f"__Current time is__\n"
            + f"{cur_time.astimezone(tzMSK).strftime(time_format)}\n"
            + f"{cur_time.astimezone(tzMSK4).strftime(time_format)}\n"
            + f"__Started at__\n"
            + f"{start_time.astimezone(tzMSK).strftime(time_format)}\n"
            + f"{start_time.astimezone(tzMSK4).strftime(time_format)}\n"
        )
    return on_ping


handlers.extend(
    util.CommandHandler(
        name=msg,
        pattern=util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + f'{msg}$')),
        help_message='Measure ping',
        author='@yuki_the_girl',
        handler_impl=on_ping_wrapper(ans),
        is_elevated=False
    ) for msg, ans in [
        ("ping", "PONG"),
        ("пинг", "ПОНГ"),
        ("test", "PASSED"),
        ("тест", "ПРОЙДЕН")
    ]
)

handlers.extend(
    util.get_handler_simple_reply(msg, ans, '@yuki_the_girl', 'Simple ping replier', util.re_ignore_case(pat))
    for msg, ans, pat in [
        ("bot", "I'm here!", util.re_pat_starts_with("bot$")),
        ("бот", "На месте!", util.re_pat_starts_with("бот$")),
        ("ты где", "Я тут", util.re_pat_starts_with("(ты где)|(где ты)$")),
        ("сдох", "Ты тоже.", util.re_pat_starts_with("сдох\\?$")),
        ("слава партии", "Слава Партии!", util.re_pat_starts_with("слава партии[?!]*")),
        ("кто здесь власть", "ПАРТИЯ!", util.re_pat_starts_with("кто здесь власть")),
    ]
)
