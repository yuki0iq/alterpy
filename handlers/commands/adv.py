import utils.cm
import utils.ch
import utils.log
import utils.regex
import utils.str

import random
import requests
import json

handler_list = []


async def advice(cm: utils.cm.CommandMessage):
    await cm.int_cur.reply(r"@yuki\_the\_girl temporarily disabled this")
    return

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
        utils.log.get("adv").exception("API down")

    await cm.int_cur.reply(f'{random.choice(["Охуенный", "Хуёвый"])} блять совет{" " + utils.str.escape(cm.arg) if cm.arg else ""}: {adv}')


handler_list.append(
    utils.ch.CommandHandler(
        name='advice',
        pattern=utils.regex.pre(utils.regex.unite('adv', 'совет')),
        help_page='advice',
        handler_impl=advice,
        is_prefix=True
    )
)
