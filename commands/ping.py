import util

import datetime
import re

handlers = []


async def on_ping(cm: util.CommandMessage):
    cur_time = datetime.datetime.now(datetime.timezone.utc)
    await cm.int_cur.reply(f"PONG.\n"
                           + f"Ping: {str(cm.local_time - cm.time)}\n"
                           + f"Handle: {str(cur_time - cm.local_time)}\n"
                           + f"UTC time: {str(cur_time)}")


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
