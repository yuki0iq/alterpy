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
    pattern=re.compile(util.re_pat_starts_with('/?(ping|пинг)')),
    help_message='Measure ping',
    author='@yuki_the_girl',
    version=1,
    handler_impl=on_ping,
    is_elevated=False
))

handlers.extend(
    util.get_handler_simple_reply(msg, ans, '@yuki_the_girl', 1, 'Simple ping replier')
    for msg, ans in [
        ("bot$", "I'm here!"),
        ("бот$", "На месте!"),
        ("ты где", "Я тут"),
        ("где ты", "Я тут"),
        ("сдох\\?$", "Ты тоже.")
    ]
)
