import pytomlpp
import logging
import traceback
import time
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



logging_formatter = logging.Formatter("%(asctime)s: %(name)s [%(levelname)s]:  %(message)s")
logging.basicConfig(format="%(asctime)s: %(name)s [%(levelname)s]:  %(message)s", level=logging.DEBUG)

def get_log(name="unknown"):
    '''create log with given name'''
    log = logging.getLogger(name)
    # TODO log.setLevel(logging.DEBUG if bot_debug else logging.INFO)
    log.setLevel(logging.DEBUG)

    ti = time.ctime().replace(":", " ").replace("  ", " ")
    ti = ti.split(" ")
    ti = "_".join(ti[1:3])

    h_file = logging.FileHandler(f"log/{name}.log", encoding="utf-8")
    h_file.setFormatter(logging_formatter)
    log.addHandler(h_file)
    # log.addHandler(logging_handler_stderr)

    return log

def log_fail(log, text):
    log.error(f"{text}\n{traceback.format_exc()}")



class MessageInteractor(typing.NamedTuple):
    message: telethon.tl.custom.message.Message

    async def reply(self, text, media):  #send reply
        try:
            await self.message.reply(text=text, media=media)
        except Exception as e:
            log_fail(get_log("telethon message interactor"), "Could not reply")

    async def respond(self, text, media):
        try:
            await self.message.respond(text=text, media=media)
        except Exception as e:
            log_fail(get_log("telethon message interactor"), "Could not respond")

    async def delete(self):  #just delete message
        try:
            await self.message.delete()
        except Exception as e:
            await self.reply(f"Error occurred:\n```\n{traceback.format_exc()}\n```")  # TODO fix message


class User:
    def is_admin(self):  #check if in admins list
        pass  # TODO
    async def get_displayname(self):
        pass  # TODO
    def get_mention(self):
        pass  # TODO


class CommandMessage(typing.NamedTuple):
    arg: str  # message text
    media: typing.Any  # media if exist
    time: datetime  # UTC time when sent
    local_time: datetime  # UTC time wher recv
    sender: User  # sender
    reply_sender: User  # reply sender if applicable
    # chat: Chat  # chat object --- unneeded for now
    int_cur: MessageInteractor  # for current message
    int_prev: MessageInteractor  # for attached reply

    def CommandMessage(self, event: telethon.events.NewMessage):
        """Construct CommandMessage from telethon NewMessage event"""
        # TODO
        pass


class CommandHandler(typing.NamedTuple):
    is_elevated: bool  # should a command be invoked only if user is admin
    is_replaceable: bool  # should a matched command pattern be replaced with nothing
    help_message: str  # short help about command
    name: str  # command name
    pattern: str  # regex pattern
    author: str
    version: int
    handler_impl: typing.Callable[[CommandMessage], typing.Awaitable]

    async def invoke(self, cm: CommandMessage):
        await self.handler_impl(cm)
