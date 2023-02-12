import util

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


async def on_prob_ru(cm: util.CommandMessage):
    await cm.int_cur.reply(f"{random.choice(prefs_ru)} {random.randint(0, 100)}%")


async def on_prob_en(cm: util.CommandMessage):
    await cm.int_cur.reply(f"{random.choice(prefs_en)} {random.randint(0, 100)}%")


async def on_choose_ru(cm: util.CommandMessage):
    opts = re.split('(?i)(^|\\s)(or|или)($|\\s)', cm.arg)[::4]
    await cm.int_cur.reply(f"{random.choice(prefs_ru)} {random.choice(opts).strip()}")


async def on_choose_en(cm: util.CommandMessage):
    opts = re.split('(?i)(^|\\s)(or|или)($|\\s)', cm.arg)[::4]
    await cm.int_cur.reply(f"{random.choice(prefs_en)} {random.choice(opts).strip()}")


handlers.append(util.CommandHandler(
    name='шанс',
    pattern=util.re_ignore_case(util.re_pat_starts_with(
        util.re_prefix() + util.re_unite('инфа', 'шанс', 'вер' + util.re_optional('оятность'))
    )),
    help_message='Найти вероятность события (случайная!)',
    handler_impl=on_prob_ru
))

handlers.append(util.CommandHandler(
    name='prob',
    pattern=util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('prob', 'chance'))),
    help_message='Find probability of given string (random!)',
    handler_impl=on_prob_en
))

handlers.append(util.CommandHandler(
    name='выбери',
    pattern=util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + 'выбери')),
    help_message='Выбрать что-нибудь случайное из "или"-разделенного списка',
    handler_impl=on_choose_ru,
    is_prefix=True
))

handlers.append(util.CommandHandler(
    name='choose',
    pattern=util.re_ignore_case(util.re_pat_starts_with(util.re_prefix() + util.re_unite('choose', 'select'))),
    help_message='Choose something random from "or"-separated list',
    handler_impl=on_choose_en,
    is_prefix=True
))
