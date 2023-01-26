import util

import re

handlers = []


async def on_layout(cm: util.CommandMessage):
    await cm.int_cur.reply(util.change_layout(cm.arg))


handlers.append(util.CommandHandler(
    name='layout',
    pattern=re.compile(util.re_pat_starts_with('/?kb|ли|layout|дфнщге|раскладка|hfcrkflrf|рас|hfc')),
    help_message='Change keyboard layout (qwerty <-> йцукен)',
    author='@yuki_the_girl',
    version=1,
    handler_impl=on_layout,
    is_prefix=True
))


