import utils.cm
import utils.ch
import utils.regex

import random
import re

handler_list = []

prefs_en = [
    "Yuki said",
    "Our Government thinks",
    "Cats selected",
    "I was forced to say",
    "Ryijik meowed",
    "You'd like to hear"
]

prefs_ru = [
    "Звёзды говорят",
    "Юки сказала",
    "Правительство нашептало",
    "Карты таро передали",
    "Котики выбрали",
    "Меня заставили сказать",
    "Осинка мяукнула",
    "Я знаю, что ты хочешь услышать",
    "Проверяй,",
    "Ставлю сотку,",
    "Древние оракулы выбрали",
    "Пусть будет",
    "Как знать,",
    "Рандом выбрал",
    "Я выбрала",
    "Сова выбрала",
    "Разрабам альтерпая нефиг делать и они решили",
    "Питон передаёт",
    "Справедливый выбор —",
    "Птичка нашептала"
]


async def on_prob_ru(cm: utils.cm.CommandMessage) -> None:
    await cm.int_cur.reply(f"{random.choice(prefs_ru)} {random.randint(0, 100)}%")


async def on_prob_en(cm: utils.cm.CommandMessage) -> None:
    await cm.int_cur.reply(f"{random.choice(prefs_en)} {random.randint(0, 100)}%")


async def on_choose_ru(cm: utils.cm.CommandMessage) -> None:
    opts = re.split('(?i)(^|\\s)(or|или)($|\\s)', cm.arg)[::4]
    await cm.int_cur.reply(f"{random.choice(prefs_ru)} {random.choice(opts).strip()}")


async def on_choose_en(cm: utils.cm.CommandMessage) -> None:
    opts = re.split('(?i)(^|\\s)(or|или)($|\\s)', cm.arg)[::4]
    await cm.int_cur.reply(f"{random.choice(prefs_en)} {random.choice(opts).strip()}")


async def on_poll(cm: utils.cm.CommandMessage) -> None:
    await cm.int_cur.reply(f"{random.choice(prefs_ru)} {utils.str.escape(random.choice(list(x.text for x in cm.media.poll().poll.answers)).strip())}")


handler_list.append(utils.ch.CommandHandler(
    name='шанс',
    pattern=utils.regex.cmd(utils.regex.unite('инфа', 'шанс', 'вер' + utils.regex.optional('оятность'))),
    help_page="random",
    handler_impl=on_prob_ru
))

handler_list.append(utils.ch.CommandHandler(
    name='prob',
    pattern=utils.regex.cmd(utils.regex.unite('prob', 'chance')),
    help_page="random",
    handler_impl=on_prob_en
))

handler_list.append(utils.ch.CommandHandler(
    name='выбери',
    pattern=utils.regex.cmd('выбери'),
    help_page="random",
    handler_impl=on_choose_ru,
    is_prefix=True
))

handler_list.append(utils.ch.CommandHandler(
    name='choose',
    pattern=utils.regex.cmd(utils.regex.unite('choose', 'select')),
    help_page="random",
    handler_impl=on_choose_en,
    is_prefix=True
))

handler_list.append(utils.ch.CommandHandler(
    name='poll-choose-ru',
    pattern=utils.regex.ignore_case(""),
    help_page="random",
    handler_impl=on_poll,
    required_media_type={"poll"},
    is_arg_current=True
))
