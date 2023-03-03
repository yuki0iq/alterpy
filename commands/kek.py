import utils.ch
import utils.rand

handlers = [
    utils.ch.simple_reply(
        'да',
        utils.rand.weighted_fun([
            (1, 'сковорода'),
            (1, 'лабуда'),
            (1, 'винда'),
            (1, 'ерунда'),
            (7, '')
        ]),
        ["кеки", "kek"],
        pattern="(?i)\\bда$"
    ),
    utils.ch.simple_reply(
        'нет',
        utils.rand.weighted_fun([
            (1, 'солнышка ответ'),
            (1, 'лунышка ответ'),
            (3, '')
        ]),
        ["кеки", "kek"],
        pattern="(?i)\\bнет$"
    ),
    utils.ch.simple_reply('дура', utils.rand.rand_or_null_fun('а может ты 🤨?', 1, 3),
        ["кеки", "kek"], pattern="(?i)\\bдура$"),

    utils.ch.simple_reply('спокойной ночи', 'Cладких снов 🥺',
        ["кеки", "kek"], pattern="(?i)^((всем ){0,1}спокойной ночи)")
]

