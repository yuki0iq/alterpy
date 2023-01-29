import util

import datetime
import re

handlers = []

start_time = datetime.datetime.now(datetime.timezone.utc)
tzMSK = datetime.timezone(datetime.timedelta(seconds=3 * 3600))
tzMSK4 = datetime.timezone(datetime.timedelta(seconds=7 * 3600))


async def on_ping(cm: util.CommandMessage):
    cur_time = datetime.datetime.now(datetime.timezone.utc)

    ping = cm.local_time - cm.time
    handle = cur_time - cm.local_time
    up = cur_time - start_time

    ping_s = util.timedelta_to_str(ping, short=True)
    handle_s = util.timedelta_to_str(handle, short=True)
    up_s = util.timedelta_to_str(up)

    await cm.int_cur.reply(
        f"**PONG**. Ping is {ping_s}, handled in {handle_s}\n"
        + f"Up for {up_s}\n"
        + f"\n"
        + f"__Current time is__\n"
        + f"(MSK+0) {cur_time.astimezone(tzMSK).strftime('%Y-%m-%d, %H:%M:%S')}\n"
        + f"(MSK+4) {cur_time.astimezone(tzMSK4).strftime('%Y-%m-%d, %H:%M:%S')}\n"
        + f"__Started at__\n"
        + f"(MSK+0) {start_time.astimezone(tzMSK).strftime('%Y-%m-%d, %H:%M:%S')}\n"
        + f"(MSK+4) {start_time.astimezone(tzMSK4).strftime('%Y-%m-%d, %H:%M:%S')}\n"
    )


handlers.append(util.CommandHandler(
    name='ping',
    pattern=re.compile(util.re_pat_starts_with('/?(ping|пинг)$')),
    help_message='Measure ping',
    author='@yuki_the_girl',
    handler_impl=on_ping,
    is_elevated=False
))

handlers.extend(
    util.get_handler_simple_reply(msg, ans, '@yuki_the_girl', 'Simple ping replier', pat)
    for msg, ans, pat in [
        ("bot", "I'm here!", util.re_pat_starts_with("bot$")),
        ("бот", "На месте!", util.re_pat_starts_with("бот$")),
        ("ты где", "Я тут", util.re_pat_starts_with("(ты где)|(где ты)$")),
        ("сдох", "Ты тоже.", util.re_pat_starts_with("сдох\\?$")),
        ("слава партии", "Слава Партии!", util.re_pat_starts_with("слава партии[?!]*")),
        ("кто здесь власть", "ПАРТИЯ!", util.re_pat_starts_with("кто здесь власть")),
    ]
)
