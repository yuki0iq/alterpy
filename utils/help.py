import utils.file
import utils.cm
import utils.ch
import utils.regex

import typing


def on_help_impl(arg: str, name: str, cname: str, gname: str, general: str, is_eng: bool) -> str:
    dir = f"./help/{gname}/"
    fn = f"{arg or ('summary' if is_eng else 'кратко')}.md"
    help_entries = utils.file.list_files(dir)
    if arg in ['list', 'список']:
        header = f"Available help entries for {name}:\n" if is_eng else f"Доступные справочные страницы для {name}:\n"
        return header + ', '.join(sorted(f"`{entry[:-3]}`" for entry in help_entries))
    if fn in help_entries:
        return open(dir + fn).read() + [f"\n\n{general}", ""][int(bool(arg))]
    return f"No help entry for `{arg}` found" if is_eng else f"Справочная страница для `{arg}` не найдена"


def handler(name: str = "Unnamed help",
            cname: str = "help",
            gname: str = ".",
            general: str = "For list of available topics, type `help list`",
            is_eng: bool = True):
    if not general:
        if is_eng:
            general = f"For list of available topics, type `{cname} list`"
        else:
            general = f"Список доступных справочных страниц `{cname} список`"

    async def on_help(cm: utils.cm.CommandMessage):
        await cm.int_cur.reply(on_help_impl(cm.arg, name, cname, gname, general, is_eng))
    return on_help


def add(handlers: typing.List,
        name: str = "Unnamed help",
        cname: str = "help",
        gname: str = ".",
        general: str = "",
        is_eng: bool = True):
    handlers.append(utils.ch.CommandHandler(
        name=f"help-{cname}-{'en' if is_eng else 'ru'}",
        pattern=utils.regex.command(cname),
        help_page=cname,
        handler_impl=handler(name, cname, gname, general, is_eng),
        is_prefix=True,
        is_arg_current=True
    ))

