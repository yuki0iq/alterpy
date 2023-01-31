import inspect
import re
import random
import pytomlpp
import logging
import traceback
import datetime
import typing
import os
import telethon.tl.custom
import telethon.tl.types
import telethon.events


def get_config(name: str) -> typing.Dict[typing.Any, typing.Any]:
    """get config by filename"""
    return pytomlpp.load(name)


def set_config(name: str, conf: typing.Dict[typing.Any, typing.Any]):
    """save config by filename"""
    pytomlpp.dump(conf, name)


def re_pat_starts_with(s: str) -> str:
    """
    wrap regex pattern into "Case insensitive; Starts with and ends with whitespace or end of string"
    """
    return f"(?i)^({s})($|\\s)"


def list_files(path: str) -> typing.List[str]:
    """list files in given folder"""
    # https://stackoverflow.com/a/3207973
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def rand_or_null_fun(s: str, p: int, q: int, s2: str = "") -> typing.Callable[[], str]:
    return lambda: (s if random.randint(1, q) <= p else s2)


def timedelta_to_str(d: datetime.timedelta, is_short: bool = False) -> str:
    """
    15 weeks 4 days 10 hours 45 minutes 37 seconds 487.5 milliseconds, (is_short=False|default)
    15w 4d 10h 45m 37s 487.5ms, (is_short=True)
    but no more than three highest
    """

    weeks, days = divmod(d.days, 7)
    minutes, seconds = divmod(d.seconds, 60)
    hours, minutes = divmod(minutes, 60)
    ms = (d.microseconds // 100) / 10

    arr = [
        (weeks, 'w', 'weeks'),
        (days, 'd', 'days'),
        (hours, 'h', 'hours'),
        (minutes, 'm', 'minutes'),
        (seconds, 's', 'seconds'),
        (ms, 'ms', 'milliseconds')
    ]

    def is_not_null(el: typing.Tuple[int, str, str]) -> bool:
        cnt, _, _ = el
        return cnt != 0

    def stringify(el: typing.Tuple[int, str, str]) -> str:
        cnt, short_name, name = el
        return f"{cnt}{short_name}" if is_short else f"{cnt} {name}"

    idx = 0
    while idx < len(arr) - 1 and not is_not_null(arr[idx]):
        idx += 1

    arr = arr[idx:idx + 3]
    arr = list(filter(is_not_null, arr))

    return ' '.join(map(stringify, arr))


def wrap(val: typing.Any) -> typing.Callable[[], typing.Any]:
    return lambda: val


def change_layout(s: str) -> str:
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


def random_printable(n: int = 10, chars="qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890") -> str:
    return ''.join(random.choice(chars) for _ in range(n))


def temp_filename() -> str:
    return f"/tmp/alterpy-{random_printable()}"


logging_formatter = logging.Formatter("%(asctime)s: %(name)s [%(levelname)s]:  %(message)s")
logging.basicConfig(format="%(asctime)s: %(name)s [%(levelname)s]:  %(message)s", level=logging.INFO)


def get_log(name="unknown") -> logging.Logger:
    """create log with given name"""
    log = logging.getLogger(name)
    # TODO log.setLevel(logging.DEBUG if bot_debug else logging.INFO)
    log.setLevel(logging.INFO)

    # ti = time.ctime().replace(":", " ").replace("  ", " ")
    # ti = ti.split(" ")
    # ti = "_".join(ti[1:3])

    h_file = logging.FileHandler(f"log/{name}.log", encoding="utf-8")
    h_file.setFormatter(logging_formatter)
    log.addHandler(h_file)
    # log.addHandler(logging_handler_stderr)

    return log


def log_fail(log: logging.Logger, text: str) -> None:
    log.error(f"{text}\n{traceback.format_exc()}")


class MessageInteractor(typing.NamedTuple):
    message: telethon.tl.custom.message.Message

    async def reply(self, text, file=None):
        """Reply to message"""
        try:
            return MessageInteractor(await self.message.reply(text, file=file))
        except:
            try: await self.message.reply(f"```{traceback.format_exc()}```")
            except: pass
            log_fail(get_log("telethon"), "Could not reply")

    async def respond(self, text, file=None):
        """Respond to message (without replying)"""
        try:
            return MessageInteractor(await self.message.respond(text, file=file))
        except:
            try: await self.message.reply(f"```{traceback.format_exc()}```")
            except: pass
            log_fail(get_log("telethon"), "Could not respond")

    async def send_file(self, file, as_reply=False, **kwargs):
        """Send file with special parameters (for example as voice note)"""
        try:
            return MessageInteractor(await self.message.client.send_file(
                await self.message.get_input_chat(),
                file,
                reply_to=(self.message if as_reply else None),
                **kwargs
            ))
        except:
            try: await self.message.reply(f"```{traceback.format_exc()}```")
            except: pass
            log_fail(get_log("telethon"), "Could not send file")

    async def delete(self):
        """Delete the message"""
        try:
            await self.message.delete()
        except:
            await self.reply(f"Error occurred:\n```\n{traceback.format_exc()}\n```")  # TODO fix message


class User(typing.NamedTuple):
    sender: telethon.tl.types.User | telethon.tl.types.Channel | telethon.tl.types.Chat

    def is_admin(self) -> bool:  # check if in admins list
        return self.sender.id in get_config("config.toml")["admins"]

    async def get_display_name(self) -> str:
        if type(self.sender) == telethon.tl.types.Channel:
            return self.sender.title
        try:
            return self.sender.first_name
        except:
            return 'null'

    async def get_mention(self) -> str:
        return f"[{await self.get_display_name()}](tg://user?id={self.sender.id})"


def to_user(user: telethon.tl.types.User | telethon.tl.types.Channel, chat: telethon.tl.types.Chat) -> User:
    if user is not None:
        return User(user)
    return User(chat)


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


def cm_apply(cm: CommandMessage, pattern: re.Pattern) -> CommandMessage:
    arg = re.sub(pattern, '', cm.arg)
    if not len(arg):
        arg = cm.rep
    return cm._replace(arg=arg)


async def to_command_message(event: telethon.events.NewMessage) -> CommandMessage:
    """Construct CommandMessage from telethon NewMessage event"""

    msg_cur = event.message
    msg_prev = await msg_cur.get_reply_message()
    has_reply = msg_prev is not None
    chat_obj = await msg_cur.get_chat()

    # TODO handle replies PROPERLY --- should media and text from replies be taken and when
    arg = msg_cur.text
    rep = f"{msg_prev.text}" if has_reply else None
    media = None  # event.message.get_media TODO
    time = msg_cur.date
    sender = to_user(await msg_cur.get_sender(), chat_obj)
    reply_sender = to_user(await msg_prev.get_sender(), chat_obj) if has_reply else None
    # self.chat = Chat(??)
    int_cur = MessageInteractor(msg_cur)
    int_prev = MessageInteractor(msg_prev) if has_reply else None

    local_time = datetime.datetime.now(datetime.timezone.utc)

    return CommandMessage(arg, rep, media, time, local_time, sender, reply_sender, int_cur, int_prev)


class CommandHandler(typing.NamedTuple):
    name: str  # command name
    pattern: re.Pattern  # regex pattern
    help_message: str  # short help about command
    author: str
    handler_impl: typing.Callable[[CommandMessage], typing.Awaitable]
    is_prefix: bool = False  # should a command be deleted from its message when passed to handler
    is_elevated: bool = False  # should a command be invoked only if user is admin

    async def invoke(self, cm: CommandMessage):
        if not self.is_elevated or cm.sender.is_admin():
            try:
                await self.handler_impl(cm)
            except:
                await cm.int_cur.reply(f"Exception occurred.\n{traceback.format_exc()}")
                log_fail(get_log("handler"), "invoke exception")
        else:
            await cm.int_cur.reply("Only bot admins can run elevated commands")  # TODO fix text


def get_handler_simple_reply(
    msg: str,
    ans: typing.Union[str, typing.Callable[[], typing.Awaitable | str]],
    author: str,
    help_message: str = "Simple reply command",
    pattern: typing.Union[str, re.Pattern] = ""
) -> CommandHandler:
    """
    Simple reply handler. [In]msg -> [Out]ans

    ans: str -- simple replier
    ans: Callable[[], maybe Awaitable str] -- call before reply

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
        handler_impl=on_simple_reply,
        is_prefix=False,
        is_elevated=False
    )
