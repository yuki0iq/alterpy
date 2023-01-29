import util

handlers = [util.get_handler_simple_reply(
    "start",
    "Привет! На связи alterpy - переделанный catpy для Telegram!\n" +
    "\n" +
    "Пока что я нахожусь в стадии разработки. Если вы нашли баги - вы можете сообщить разработчикам или присоединиться в ряды тестеров.\n" +
    "Разработано для t.me/theyukichat\n" +
    "Список команд __пока не поддерживается__\n" +
    "Пинг до бота: `/ping`\n" +
    "\n" +
    "В разработке принимали участие: t.me/yuki_the_girl",
    "@yuki_the_girl",
    1,
    "Start message",
    util.re_pat_starts_with("/start")
)]

