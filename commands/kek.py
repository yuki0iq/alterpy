import util

handlers = []

handlers.append(util.get_handler_simple_reply('да', 'пизда', '@yuki_the_girl', 1, "simple reply command", "(?i)да$"))
handlers.append(util.get_handler_simple_reply('нет', 'солнышка ответ', '@yuki_the_girl', 1, "simple reply command", "(?i)нет$"))
handlers.append(util.get_handler_simple_reply('дура', 'а может ты 🤨?', '@yuki_the_girl', 1, "simple reply command", "(?i)дура$"))
