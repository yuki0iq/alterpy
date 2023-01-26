import util

import random
import requests
import json

handlers = []


async def advice():
    adv_json = requests.get(
        'http://fucking-great-advice.ru/api/random',
        headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'
        }
    ).text
    adv = json.loads(adv_json)['text']
    return f'{random.choice(["Охуенный", "Хуёвый"])} блять совет: {adv}'


handlers.append(
    util.get_handler_simple_reply(
        msg='advice',
        ans=advice,
        author='@yuki_the_girl',
        version=1,
        help_message=
            "Fucking great advice from fucking-great-advice.ru\n" +
            "Based on: github.com/Catware-Foundation/Catpy-Software/blob/main/advice.py",
        pattern='/?adv|совет'
    )
)
