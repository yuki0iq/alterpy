import inspect
import re
import random
import pytomlpp
import logging
import traceback
# import time
import datetime
import typing
import os

import telethon.tl.custom
import telethon.events


def get_config(name):
    """get config by filename"""
    return pytomlpp.load(name)


def set_config(name, conf):
    """save config by filename"""
    pytomlpp.dump(conf, name)


def re_pat_starts_with(s):
    """wrap regex pattern into "Case insensitive; Starts with and ends with whitespace or end of string\""""
    return f"(?i)^({s})($|\\s)"


def list_files(path):
    """list files in given folder"""
    # https://stackoverflow.com/a/3207973
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def rand_or_null_fun(s: str, p: int, q: int):
    return lambda: (s if random.randint(1, q) <= p else '')


def change_layout(s):
    """alternate between QWERTY and JCUKEN"""
    en = r"""`~!@#$^&qwertyuiop[]\QWERTYUIOP{}|asdfghjkl;'ASDFGHJKL:"zxcvbnm,./ZXCVBNM<>?"""
    ru = r"""ёЁ!"№;:?йцукенгшщзхъ\ЙЦУКЕНГШЩЗХЪ/фывапролджэФЫВАПРОЛДЖЭячсмитьбю.ЯЧСМИТЬБЮ,"""
    fr, to = en + ru, ru + en

    res = []
    for c in s:
        if c in fr:
            res.append(to[fr.index(c)])
        else:
            res.append(c)
    return ''.join(res)


logging_formatter = logging.Formatter("%(asctime)s: %(name)s [%(levelname)s]:  %(message)s")
logging.basicConfig(format="%(asctime)s: %(name)s [%(levelname)s]:  %(message)s", level=logging.INFO)


def get_log(name="unknown"):
    """create log with given name"""
    log = logging.getLogger(name)
    # TODO log.setLevel(logging.DEBUG if bot_debug else logging.INFO)
    log.setLevel(logging.DEBUG)

    # ti = time.ctime().replace(":", " ").replace("  ", " ")
    # ti = ti.split(" ")
    # ti = "_".join(ti[1:3])

    h_file = logging.FileHandler(f"log/{name}.log", encoding="utf-8")
    h_file.setFormatter(logging_formatter)
    log.addHandler(h_file)
    # log.addHandler(logging_handler_stderr)

    return log


def log_fail(log, text):
    log.error(f"{text}\n{traceback.format_exc()}")


class MessageInteractor(typing.NamedTuple):
    message: telethon.tl.custom.message.Message

    async def reply(self, text, media=None):
        """Reply to message"""
        try:
            await self.message.reply(text, file=media)
        except:
            log_fail(get_log("telethon"), "Could not reply")

    async def respond(self, text, media=None):
        """Respond to message (without replying)"""
        try:
            await self.message.respond(text, file=media)
        except:
            log_fail(get_log("telethon"), "Could not respond")

    async def delete(self):
        """Delete the message"""
        try:
            await self.message.delete()
        except:
            await self.reply(f"Error occurred:\n```\n{traceback.format_exc()}\n```")  # TODO fix message


class User:
    def is_admin(self):  # check if in admins list
        return False  # TODO

    async def get_displayname(self):
        pass  # TODO

    def get_mention(self):
        pass  # TODO


class CommandMessage(typing.NamedTuple):
    arg: str  # message text
    rep: str  # message text with reply attached
    media: typing.Any  # media if exist
    time: datetime.datetime  # UTC time when sent
    local_time: datetime.datetime  # UTC time wher recv
    sender: User  # sender
    reply_sender: User  # reply sender if applicable
    # chat: Chat  # chat object --- unneeded for now
    int_cur: MessageInteractor  # for current message
    int_prev: MessageInteractor  # for attached reply


def cm_apply(cm: CommandMessage, pattern: re.Pattern):
    arg = re.sub(pattern, '', cm.arg)
    if not len(arg):
        arg = cm.rep
    return cm._replace(arg=arg)


async def to_command_message(event: telethon.events.NewMessage):
    """Construct CommandMessage from telethon NewMessage event"""

    msg_cur = event.message
    msg_prev = await msg_cur.get_reply_message()
    has_reply = msg_prev is not None

    # TODO handle replies PROPERLY --- should media and text from replies be taken and when
    arg = msg_cur.message
    rep = f"{msg_prev.message}" if has_reply else None
    media = None  # event.message.get_media TODO
    time = msg_cur.date
    local_time = datetime.datetime.now(datetime.timezone.utc)
    sender = User()  # User(event.message.get_sender)
    reply_sender = None  # User(event.message.reply.get_sender)
    # self.chat = Chat(??)
    int_cur = MessageInteractor(msg_cur)
    int_prev = MessageInteractor(msg_prev) if has_reply else None

    return CommandMessage(arg, rep, media, time, local_time, sender, reply_sender, int_cur, int_prev)


class CommandHandler(typing.NamedTuple):
    name: str  # command name
    pattern: re.Pattern  # regex pattern
    help_message: str  # short help about command
    author: str
    version: int
    handler_impl: typing.Callable[[CommandMessage], typing.Awaitable]
    is_prefix: bool = False  # should a command be deleted from its message when passed to handler
    is_elevated: bool = False  # should a command be invoked only if user is admin

    async def invoke(self, cm: CommandMessage):
        if not self.is_elevated or cm.sender.is_admin():
            await self.handler_impl(cm)
        else:
            await cm.int_cur.reply("Only bot admins can run elevated commands")  # TODO fix text


def get_handler_simple_reply(
    msg: str,
    ans: typing.Any,
    author: str,
    version: int,
    help_message: str = "Simple reply command",
    pattern: typing.Any = ""
) -> CommandHandler:
    """
    Simple reply handler. [In]msg -> [Out]ans

    ans: str -- simple replier
    ans: Callable[[], Awaitable] -- call before reply

    pattern: str OR re.Pattern
    """

    if type(ans) == str:
        async def on_simple_reply_str(cm: CommandMessage):
            await cm.int_cur.reply(ans)
        on_simple_reply = on_simple_reply_str
    elif inspect.iscoroutinefunction(ans):
        async def on_simple_reply_async(cm: CommandMessage):
            ret = await ans()
            if ret:
                await cm.int_cur.reply(ret)
        on_simple_reply = on_simple_reply_async
    elif inspect.isfunction(ans):
        async def on_simple_reply_fun(cm: CommandMessage):
            ret = ans()
            if ret:
                await cm.int_cur.reply(ret)
        on_simple_reply = on_simple_reply_fun
    else:
        async def on_simple_reply(cm: CommandMessage):
            await cm.int_cur.reply("Broken handler!")
        log_fail(get_log("handler"), "Wrong reply answer passed")

    if pattern is None or not len(pattern):
        pattern = re_pat_starts_with(msg)
    if type(pattern) == str:
        pattern = re.compile(pattern)
    return CommandHandler(
        name=msg,
        pattern=pattern,
        help_message=help_message,
        author=author,
        version=version,
        handler_impl=on_simple_reply,
        is_prefix=False,
        is_elevated=False
    )
