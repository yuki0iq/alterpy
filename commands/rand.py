import utils

import random
import re

handlers = []

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


async def on_prob_ru(cm: utils.cm.CommandMessage):
    await cm.int_cur.reply(f"{random.choice(prefs_ru)} {random.randint(0, 100)}%")


async def on_prob_en(cm: utils.cm.CommandMessage):
    await cm.int_cur.reply(f"{random.choice(prefs_en)} {random.randint(0, 100)}%")


async def on_choose_ru(cm: utils.cm.CommandMessage):
    opts = re.split('(?i)(^|\\s)(or|или)($|\\s)', cm.arg)[::4]
    await cm.int_cur.reply(f"{random.choice(prefs_ru)} {random.choice(opts).strip()}")


async def on_choose_en(cm: utils.cm.CommandMessage):
    opts = re.split('(?i)(^|\\s)(or|или)($|\\s)', cm.arg)[::4]
    await cm.int_cur.reply(f"{random.choice(prefs_en)} {random.choice(opts).strip()}")


handlers.append(utils.ch.CommandHandler(
    name='шанс',
    pattern=utils.regex.command(utils.regex.unite('инфа', 'шанс', 'вер' + utils.regex.optional('оятность'))),
    help_page=["random", "случайность"],
    handler_impl=on_prob_ru
))

handlers.append(utils.ch.CommandHandler(
    name='prob',
    pattern=utils.regex.command(utils.regex.unite('prob', 'chance')),
    help_page=["random", "случайность"],
    handler_impl=on_prob_en
))

handlers.append(utils.ch.CommandHandler(
    name='выбери',
    pattern=utils.regex.command('выбери'),
    help_page=["random", "случайность"],
    handler_impl=on_choose_ru,
    is_prefix=True
))

handlers.append(utils.ch.CommandHandler(
    name='choose',
    pattern=utils.regex.command(utils.regex.unite('choose', 'select')),
    help_page=["random", "случайность"],
    handler_impl=on_choose_en,
    is_prefix=True
))
