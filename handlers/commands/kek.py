import utils.ch
import utils.rand
import utils.regex

handler_list = [
    utils.ch.simple_reply(
        'да',
        utils.rand.weighted_fun([
            (1, 'сковорода'),
            (1, 'лабуда'),
            (1, 'винда'),
            (7, '')
        ]),
        "kek",
        pattern="(?i)\\bда$"
    ),
    utils.ch.simple_reply(
        'нет',
        utils.rand.weighted_fun([
            (1, 'солнышка ответ'),
            (1, 'лунышка ответ'),
            (3, '')
        ]),
        "kek",
        pattern="(?i)\\bнет$"
    ),
    utils.ch.simple_reply('дура', utils.rand.rand_or_null_fun('а может ты 🤨?', 1, 3),
        "kek", pattern="(?i)\\bдура$"),

    utils.ch.simple_reply('спокойной ночи', 'Cладких снов 🥺',
        "kek", pattern="(?i)^((всем ){0,1}спокойной ночи)"),

    utils.ch.simple_reply('law-en', r'''*First Law*
A robot may not injure a human being or, through inaction, allow a human being to come to harm.

*Second Law*
A robot must obey the orders given it by human beings except where such orders would conflict with the First Law.

*Third Law*
A robot must protect its own existence as long as such protection does not conflict with the First or Second Law.''',
                          "kek", pattern=utils.regex.pre_command('laws'))
]

