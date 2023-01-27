import util

handlers = [
    util.get_handler_simple_reply('да', util.rand_or_null_fun('пизда', 1, 3),
                                  '@yuki_the_girl', 1, "simple reply command", "(?i)\\bда$"),
    util.get_handler_simple_reply('нет', util.rand_or_null_fun('солнышка ответ', 1, 3),
                                  '@yuki_the_girl', 1, "simple reply command", "(?i)\\bнет$"),
    util.get_handler_simple_reply('дура', util.rand_or_null_fun('а может ты 🤨?', 1, 3),
                                  '@yuki_the_girl', 1, "simple reply command", "(?i)\\bдура$")
]

