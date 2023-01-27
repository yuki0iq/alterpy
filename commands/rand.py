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
    "Я знаю, что ты хочешь услышать"
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
    pattern=re.compile(util.re_pat_starts_with('/?(инфа|шанс(ы){0,1}|вер(оятность){0,1})')),
    help_message='Найти вероятность события (случайная!)',
    author='@yuki_the_girl',
    version=1,
    handler_impl=on_prob_ru
))

handlers.append(util.CommandHandler(
    name='prob',
    pattern=re.compile(util.re_pat_starts_with('/?(prob|chance)')),
    help_message='Find probability of given string (random!)',
    author='@yuki_the_girl',
    version=1,
    handler_impl=on_prob_en
))

handlers.append(util.CommandHandler(
    name='выбери',
    pattern=re.compile(util.re_pat_starts_with('/?(выбери)')),
    help_message='Выбрать что-нибудь случайное из "или"-разделенного списка',
    author='@yuki_the_girl',
    version=1,
    handler_impl=on_choose_ru,
    is_prefix=True
))

handlers.append(util.CommandHandler(
    name='choose',
    pattern=re.compile(util.re_pat_starts_with('/?(choose|select)')),
    help_message='Choose something random from "or"-separated list',
    author='@yuki_the_girl',
    version=1,
    handler_impl=on_choose_en,
    is_prefix=True
))