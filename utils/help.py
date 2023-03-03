import utils.file
import utils.cm
import utils.ch
import utils.regex

import typing


def on_help_impl(arg: str, name: str, cmd: str, path: str, default_message: str, is_eng: bool) -> str:
    dir = f"./help/{path}/"
    fn = f"{arg or ('summary' if is_eng else 'кратко')}.md"
    help_entries = utils.file.list_files(dir)
    if not arg or arg in ['list', 'список']:
        header = f"Available help entries for {name}:\n" if is_eng else f"Доступные справочные страницы для {name}:\n"
        return header + ', '.join(sorted(f"`{entry[:-3]}`" for entry in help_entries))
    if fn in help_entries:
        return open(dir + fn).read()
    return f"No help entry for `{arg}` found" if is_eng else f"Справочная страница для `{arg}` не найдена"


def handler(name: str = "Unnamed help",
            cmd: str = "help",
            path: str = ".",
            is_eng: bool = True):
    if is_eng:
        default_message = f"For list of available topics, type `{cmd} list`"
    else:
        default_message = f"Список доступных справочных страниц `{cmd} список`"

    async def on_help(cm: utils.cm.CommandMessage):
        await cm.int_cur.reply(on_help_impl(cm.arg, name, cmd, path, default_message, is_eng))
    return on_help


def add(handlers: typing.List,
        name: str = "Unnamed help",
        cmd: str = "help",
        path: str = ".",
        is_eng: bool = True):
    handlers.append(utils.ch.CommandHandler(
        name=f"help-{cmd}-{'en' if is_eng else 'ru'}",
        pattern=utils.regex.command(cmd),
        help_page=cmd,
        handler_impl=handler(name, cmd, path, is_eng),
        is_prefix=True,
        is_arg_current=True
    ))

