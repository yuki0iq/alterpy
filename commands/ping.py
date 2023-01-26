import util

import datetime


async def on_ping(cm: util.CommandMessage):
    cur_time = datetime.datetime.now(datetime.timezone.utc)
    await cm.int_cur.reply(f"PONG.\nPing: {str(cm.local_time - cm.time)}\nHandle: {str(cur_time - cm.local_time)}")


def on_bot(s):
    async def on_bot_handler(cm: util.CommandMessage):
        await cm.int_cur.reply(s)

    return on_bot_handler


append_handler(
    name='ping',
    pattern=util.re_pat_starts_with('/?(ping|пинг)'),
    help_message='Measure ping',
    author='@yuki_the_girl',
    version=1,
    handler_impl=on_ping,
    is_elevated=False
)

for msg, ans in [
    ("bot", "I'm here!"),
    ("бот", "На месте!"),
    ("ты где", "Я тут"),
    ("где ты", "Я тут"),
    ("сдох?", "Ты тоже.")
]:
    append_handler(
        name=msg,
        pattern=util.re_pat_starts_with(msg),
        help_message='Simple ping replier',
        author='@yuki_the_girl',
        version=1,
        handler_impl=on_bot(ans),
        is_elevated=False
    )
