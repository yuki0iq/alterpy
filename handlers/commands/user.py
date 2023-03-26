import utils.cm
import utils.ch
import utils.pronouns
import utils.regex
import utils.str
import utils.locale
import utils.user

handler_list = []

translations = {
    'set_name_empty': {
        'en': 'Can not set name to empty one. To reset name use `-name`',
        'ru': 'Невозможно установить пустое имя. Для сброса используйте `-имя`',
    },
    'set_name': {
        'en': 'Name set to {name}',
        'ru': 'Установлено имя {name}',
    },
    'reset_name': {
        'en': 'Name is now unset',
        'ru': 'Имя сброшено',
    },
    'set_pronouns_empty': {
        'en': 'To set pronouns to empty, use `+pn void`. To reset pronouns, use `-pn`',
        'ru': 'Чтобы использовать пустые местоимения, используйте `+мест нет`. Чтобы сбросить местоимения, используйте `-мест`',
    },
    'set_pronouns': {
        'en': 'Pronouns set to {pns}',
        'ru': 'Установлены местоимения {pns}',
    },
    'reset_pronouns': {
        'en': 'Pronouns are now unset',
        'ru': 'Местоимения сброшены',
    },
    'set_redirect_empty': {
        'en': 'Can not set mention redirect to empty. To reset use `-redir`',
        'ru': 'Невозможно установить пустое перенаправление. Для сброса используйте `-напр`',
    },
    'set_redirect': {  # TODO
        'en': 'Mention redirect set to {rid}',
        'ru': 'Перенаправление упоминаний установлено на {rid}',
    },
    'get': {  # TODO
        'en': "{name}'s pronouns are {pns}. Name set? {has_name}. Redirect? {rid}",
        'ru': "Набор местоимений {name} — {pns}. Установлено имя? {has_name}. Перенаправление? {rid}",
    }
}

LOC = utils.locale.Localizator(translations)


def on_set_name(lang: str = "en"):
    async def impl(cm: utils.cm.CommandMessage):
        if not cm.arg:
            await cm.int_cur.reply(LOC.obj('set_name_empty', lang))
            return
        name = cm.arg
        cm.sender.set_name(name)
        await cm.int_cur.reply(eval(LOC.get('set_name', lang)))
    return impl


def on_reset_name(lang: str = "en"):
    async def impl(cm: utils.cm.CommandMessage):
        cm.sender.reset_name()
        await cm.int_cur.reply(LOC.obj('reset_name', lang))
    return impl


def on_set_pronouns(lang: str = "en"):
    async def impl(cm: utils.cm.CommandMessage):
        if not cm.arg:
            await cm.int_cur.reply(LOC.obj('set_pronouns_empty', lang))
            return
        pns_s = cm.arg
        pns_i = utils.pronouns.from_str(pns_s)
        pns = utils.pronouns.to_str(pns_i)
        cm.sender.set_pronouns(pns_i)
        await cm.int_cur.reply(eval(LOC.get('set_pronouns', lang)))
    return impl


def on_reset_pronouns(lang: str = "en"):
    async def impl(cm: utils.cm.CommandMessage):
        cm.sender.reset_pronouns()
        await cm.int_cur.reply(LOC.obj('reset_pronouns', lang))
    return impl


def on_set_redirect(lang: str = "en"):
    async def impl(cm: utils.cm.CommandMessage):
        _, mentioned, _, _ = await utils.user.from_str(cm.arg, cm.sender.chat_id, cm.client)
        user = mentioned or cm.reply_sender
        if not user:
            await cm.int_cur.reply(LOC.obj('set_redirect_empty', lang))
            return
        rid = user.sender.id
        cm.sender.set_redirect(rid)
        await cm.int_cur.reply(eval(LOC.get('set_redirect', lang)))
    return impl


def on_reset_redirect(lang: str = "en"):
    async def impl(cm: utils.cm.CommandMessage):
        cm.sender.reset_redirect()
        await cm.int_cur.reply(LOC.obj('reset_redirect', lang))
    return impl


def on_get(lang: str = "en"):
    async def impl(cm: utils.cm.CommandMessage):
        _, mentioned, _, _ = await utils.user.from_str(cm.arg, cm.sender.chat_id, cm.client)
        user = mentioned or cm.reply_sender or cm.sender
        name = await user.get_display_name()
        has_name = bool(user.get_name())
        pns = utils.pronouns.to_str(user.get_pronouns())
        rid = user.get_redirect() or 'NOT SET'
        await cm.int_cur.reply(eval(LOC.get('get', lang)))
    return impl


handler_list.append(utils.ch.CommandHandler("+name",  utils.regex.raw_command(r"\+name"),  "name", on_set_name('en'), is_prefix=True, is_arg_current=True))
handler_list.append(utils.ch.CommandHandler("+имя",   utils.regex.raw_command(r"\+имя"),   "имя",  on_set_name('ru'), is_prefix=True, is_arg_current=True))
handler_list.append(utils.ch.CommandHandler("-name",  utils.regex.raw_command("-name"),    "name", on_reset_name('en')))
handler_list.append(utils.ch.CommandHandler("-имя",   utils.regex.raw_command("-имя"),     "имя",  on_reset_name('ru')))
handler_list.append(utils.ch.CommandHandler("+pn",    utils.regex.raw_command(r"\+pn"),    "name", on_set_pronouns('en'), is_prefix=True, is_arg_current=True))
handler_list.append(utils.ch.CommandHandler("+мест",  utils.regex.raw_command(r"\+мест"),  "имя",  on_set_pronouns('ru'), is_prefix=True, is_arg_current=True))
handler_list.append(utils.ch.CommandHandler("-pn",    utils.regex.raw_command(r"-pn"),     "name", on_reset_pronouns('en')))
handler_list.append(utils.ch.CommandHandler("-мест",  utils.regex.raw_command(r"-мест"),   "имя",  on_reset_pronouns('ru')))
handler_list.append(utils.ch.CommandHandler("+redir", utils.regex.raw_command(r"\+redir"), "name", on_set_redirect('en'), is_prefix=True, is_arg_current=True))
handler_list.append(utils.ch.CommandHandler("+напр",  utils.regex.raw_command(r"\+напр"),  "имя",  on_set_redirect('ru'), is_prefix=True, is_arg_current=True))
handler_list.append(utils.ch.CommandHandler("-redir", utils.regex.raw_command(r"-redir"),  "name", on_reset_redirect('en')))
handler_list.append(utils.ch.CommandHandler("-напр",  utils.regex.raw_command(r"-напр"),   "имя",  on_reset_redirect('ru')))

handler_list.append(utils.ch.CommandHandler("?name", utils.regex.raw_command(r"\?name"), "name", on_get('en'), is_prefix=True, is_arg_current=True))
handler_list.append(utils.ch.CommandHandler("?имя",  utils.regex.raw_command(r"\?имя"),  "имя",  on_get('ru'), is_prefix=True, is_arg_current=True))
handler_list.append(utils.ch.CommandHandler("?pn",   utils.regex.raw_command(r"\?pn"),   "name", on_get('en'), is_prefix=True, is_arg_current=True))
handler_list.append(utils.ch.CommandHandler("?мест", utils.regex.raw_command(r"\?мест"), "имя",  on_get('ru'), is_prefix=True, is_arg_current=True))
