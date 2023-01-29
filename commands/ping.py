import util

import datetime
import re

handlers = []

start_time = datetime.datetime.now(datetime.timezone.utc)


async def on_ping(cm: util.CommandMessage):
    cur_time = datetime.datetime.now(datetime.timezone.utc)

    ping = cm.local_time - cm.time
    handle = cur_time - cm.local_time
    up = cur_time - start_time

    ping_s = util.timedelta_to_str(ping, short=True)
    handle_s = util.timedelta_to_str(handle, short=True)
    up_s = util.timedelta_to_str(up)

    await cm.int_cur.reply(
        f"PONG.\n"
        + f"Ping: {ping_s}\n"
        + f"Handle: {handle_s}\n"
        + f"Up: {up_s}\n"
        + f"UTC time: {cur_time.strftime('%Y-%m-%d, %H:%M:%S')}\n"
        + f"Started at: {start_time.strftime('%Y-%m-%d, %H:%M:%S')}\n"
    )


handlers.append(util.CommandHandler(
    name='ping',
    pattern=re.compile(util.re_pat_starts_with('/?(ping|пинг)$')),
    help_message='Measure ping',
    author='@yuki_the_girl',
    version=1,
    handler_impl=on_ping,
    is_elevated=False
))

handlers.extend(
    util.get_handler_simple_reply(msg, ans, '@yuki_the_girl', 1, 'Simple ping replier', pat)
    for msg, ans, pat in [
        ("bot", "I'm here!", util.re_pat_starts_with("bot$")),
        ("бот", "На месте!", util.re_pat_starts_with("бот$")),
        ("ты где", "Я тут", util.re_pat_starts_with("(ты где)|(где ты)$")),
        ("сдох", "Ты тоже.", util.re_pat_starts_with("сдох\\?$"))
    ]
)
