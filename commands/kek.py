import util

handlers = [
    util.get_handler_simple_reply('да', util.rand_or_null_fun('пизда', 1, 3),
                                  '@yuki_the_girl', "simple reply command", "(?i)\\bда$"),
    util.get_handler_simple_reply('нет', util.rand_or_null_fun('солнышка ответ', 1, 3),
                                  '@yuki_the_girl', "simple reply command", "(?i)\\bнет$"),
    util.get_handler_simple_reply('дура', util.rand_or_null_fun('а может ты 🤨?', 1, 3),
                                  '@yuki_the_girl', "simple reply command", "(?i)\\bдура$"),

    util.get_handler_simple_reply('спокойной ночи', 'Cладких снов 🥺',
                                  '@yuki_the_girl', "simple reply command", "(?i)^((всем ){0,1}спокойной ночи)")
]

