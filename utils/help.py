import utils.file
import utils.cm
import utils.ch
import utils.regex
import utils.str

import re


def on_help_impl(arg: str, name: str, path: str, is_eng: bool) -> str:
    dir = f"./help/{path}/"
    fn = f"{arg or ('summary' if is_eng else 'кратко')}.md"
    help_entries = utils.file.list_files(dir)
    if not arg or arg in ['list', 'список']:
        header = f"Available help entries for {name}:\n" if is_eng else f"Доступные справочные страницы для {name}:\n"
        return header + ', '.join(sorted(f"`{entry[:-3]}`" for entry in help_entries))
    if fn in help_entries:
        return open(dir + fn).read()
    return f"No help entry for `{arg}` found" if is_eng else f"Справочная страница для `{arg}` не найдена"


def forward_handler(name: str = "Unnamed help", cmd: str = "help", path: str = ".", is_eng: bool = True):
    async def on_help(cm: utils.cm.CommandMessage):
        await cm.int_cur.reply(on_help_impl(cm.arg, name, path, is_eng))
    return on_help


def on_reverse_help_impl(handlers: list, arg: str, cmd: str, path: str, is_eng: bool) -> str:
    if not arg:
        if is_eng:
            return f"Type `{cmd} [command]` to view help page for command"
        else:
            return f"Чтобы посмотреть справочную страницу, соответствующую команде, введите `{cmd} [команда]`"

    dir = f"./help/{path}/"
    help_entries = utils.file.list_files(dir)

    help_pages_list = [
        handler.help_page
        for handler in filter(
            lambda handler:
                bool(re.search(handler.pattern, arg))
                and not bool(re.search(handler.pattern, '')),
            handlers
        )
    ]

    help_pages = []
    for hp in help_pages_list:
        help_pages.extend(hp)

    help_pages = list(filter(lambda hp: is_eng == utils.str.is_eng(hp), help_pages))

    if not help_pages:
        return f"No command `{arg}` found" if is_eng else f"Команда `{arg}` не найдена"

    help_page = help_pages[0]
    fn = f"{help_page}.md"
    if fn in help_entries:
        return open(dir + fn).read()
    return f"No help entry for command `{arg}` found (`{dir+fn}`)" if is_eng else f"Справочная страница для команды `{arg}` не найдена (`{dir+fn}`)"


def reverse_handler(handlers: list, cmd: str = "which", help_cmd: str = "help", path: str = ".", is_eng: bool = True):
    async def on_help(cm: utils.cm.CommandMessage):
        await cm.int_cur.reply(on_reverse_help_impl(handlers, cm.arg, cmd, path, is_eng))
    return on_help


def add(handlers: list, name: str = "Unnamed help", cmd: str = "help", find_cmd: str = "which", path: str = ".", is_eng: bool = True):
    handlers.append(utils.ch.CommandHandler(
        name=f"help-{cmd}-{'en' if is_eng else 'ru'}",
        pattern=utils.regex.command(cmd),
        help_page=["help", "справка"],
        handler_impl=forward_handler(name, cmd, path, is_eng),
        is_prefix=True,
        is_arg_current=True
    ))
    handlers.append(utils.ch.CommandHandler(
        name=f"which-{cmd}-{'en' if is_eng else 'ru'}",
        pattern=utils.regex.command(find_cmd),
        help_page=["help", "справка"],
        handler_impl=reverse_handler(handlers, cmd, find_cmd, path, is_eng),
        is_prefix=True,
        is_arg_current=True
    ))

