import pytomlpp
import logging
import traceback
# import time
import datetime
import typing

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
    return f"(?i)({s})($|\\s)"


logging_formatter = logging.Formatter("%(asctime)s: %(name)s [%(levelname)s]:  %(message)s")
logging.basicConfig(format="%(asctime)s: %(name)s [%(levelname)s]:  %(message)s", level=logging.DEBUG)


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
        except Exception as e:
            log_fail(get_log("telethon message interactor"), "Could not reply")

    async def respond(self, text, media=None):
        """Respond to message (without replying)"""
        try:
            await self.message.respond(text, file=media)
        except Exception as e:
            log_fail(get_log("telethon message interactor"), "Could not respond")

    async def delete(self):
        """Delete the message"""
        try:
            await self.message.delete()
        except Exception as e:
            await self.reply(f"Error occurred:\n```\n{traceback.format_exc()}\n```")  # TODO fix message


class User:
    def is_admin(self):  # check if in admins list
        pass  # TODO

    async def get_displayname(self):
        pass  # TODO

    def get_mention(self):
        pass  # TODO


class CommandMessage(typing.NamedTuple):
    arg: str  # message text
    arg_rep: str  # message text with reply attached
    media: typing.Any  # media if exist
    time: datetime.datetime  # UTC time when sent
    local_time: datetime.datetime  # UTC time wher recv
    sender: User  # sender
    reply_sender: User  # reply sender if applicable
    # chat: Chat  # chat object --- unneeded for now
    int_cur: MessageInteractor  # for current message
    int_prev: MessageInteractor  # for attached reply

    async def CommandMessage(self, event: telethon.events.NewMessage):
        """Construct CommandMessage from telethon NewMessage event"""

        msg_cur = event.message
        msg_prev = await msg_cur.get_reply_message()
        has_reply = msg_prev is not None

        # TODO handle replies PROPERLY --- should media and text from replies be taken and when
        self.arg = msg_cur.message
        self.arg_rep = f"{msg_cur.message}\n{msg_prev.message}" if has_reply else self.arg
        self.media = None  # event.message.get_media TODO
        self.time = msg_cur.date
        self.local_time = datetime.datetime.now(datetime.timezone.utc)
        self.sender = None  # User(event.message.get_sender)
        self.reply_sender = None  # User(event.message.reply.get_sender)
        # self.chat = Chat(??)
        self.int_cur = MessageInteractor(msg_cur)
        self.int_prev = MessageInteractor(msg_prev) if has_reply else None


class CommandHandler(typing.NamedTuple):
    name: str  # command name
    pattern: str  # regex pattern
    help_message: str  # short help about command
    author: str
    version: int
    handler_impl: typing.Callable[[CommandMessage], typing.Awaitable]
    is_elevated: bool = True  # should a command be invoked only if user is admin
    is_replaceable: bool = False  # should a matched command pattern be replaced with nothing

    async def invoke(self, cm: CommandMessage):
        await self.handler_impl(cm)
