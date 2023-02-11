import util

import random
import requests
import json

handlers = []


async def advice(cm: util.CommandMessage):
    try:
        adv_json = requests.get(
            'http://fucking-great-advice.ru/api/random',
            headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'
            }
        ).text
        adv = json.loads(adv_json)['text']
    except:
        await cm.int_cur.reply("Advice API down")
        util.log_fail(util.get_log("adv"), "API down")

    await cm.int_cur.reply(f'{random.choice(["Охуенный", "Хуёвый"])} блять совет{" " + cm.arg if cm.arg else ""}: {adv}')


handlers.append(
    util.CommandHandler(
        name='advice',
        pattern=util.re_ignore_case(util.re_pat_starts_with(util.re_only_prefix() + util.re_unite('adv', 'совет'))),
        help_message=
                    "Fucking great advice from fucking-great-advice.ru\n" +
                    "Based on: github.com/Catware-Foundation/Catpy-Software/blob/main/advice.py",
        author='@yuki_the_girl',
        handler_impl=advice,
        is_prefix=True
    )
)
