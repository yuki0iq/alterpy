import utils.cm
import utils.ch
import utils.log
import utils.regex

import random
import requests
import json

handlers = []


async def advice(cm: utils.cm.CommandMessage):
    adv = "Не досупен"
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
        utils.log.fail(utils.log.get("adv"), "API down")

    await cm.int_cur.reply(f'{random.choice(["Охуенный", "Хуёвый"])} блять совет{" " + cm.arg if cm.arg else ""}: {adv}')


handlers.append(
    utils.ch.CommandHandler(
        name='advice',
        pattern=utils.regex.ignore_case(utils.regex.pat_starts_with(utils.regex.only_prefix() + utils.regex.unite('adv', 'совет'))),
        help_page=['advice', 'совет'],
        handler_impl=advice,
        is_prefix=True
    )
)
