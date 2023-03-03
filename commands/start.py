import utils.ch
import utils.regex

handlers = [utils.ch.simple_reply(
    "start",
    "Привет! На связи alterpy - быстрый, потому что никому не нужный телеграм-бот!\n" +
    "\n" +
    "Пока что я нахожусь в стадии разработки. Если вы нашли баги - вы можете сообщить разработчикам или присоединиться в ряды тестеров.\n" +
    "Как catpy и forkpy, только по-другому\n" +
    "Разработано для t.me/theyukichat\n" +
    "Список команд __пока не поддерживается__\n" +
    "Пинг до бота: `/ping`\n" +
    "\n" +
    "В разработке принимали участие: t.me/yuki_the_girl",
    ["start", "начало"],
    utils.regex.raw_command("/start(@alterpy_bot)?")
)]

