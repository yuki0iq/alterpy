import util

import re
import iuliia

handlers = []


async def on_layout(cm: util.CommandMessage):
    await cm.int_cur.reply(util.change_layout(cm.arg))


async def on_trl(cm: util.CommandMessage):
    if cm.arg:
        await cm.int_cur.reply(iuliia.translate(cm.arg, iuliia.WIKIPEDIA))


handlers.append(util.CommandHandler(
    name='layout',
    pattern=re.compile(util.re_pat_starts_with('/?(kb|ли|layout|дфнщге|раскладка|hfcrkflrf|рас|hfc)')),
    help_message='Change keyboard layout (qwerty <-> йцукен)',
    author='@yuki_the_girl',
    handler_impl=on_layout,
    is_prefix=True
))

handlers.append(util.CommandHandler(
    name='iuliia',
    pattern=re.compile(util.re_pat_starts_with('/?(trl|translit|iuliia|трл|транслит|йуля)')),
    help_message='wikipedia-style iuliia transliterate (привет -> privet), habr.com/post/499574',
    author='@yuki_the_girl',
    handler_impl=on_trl,
    is_prefix=True
))
