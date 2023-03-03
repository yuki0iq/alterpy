import typing
import datetime
import utils
import telethon.tl.custom


class CommandMessage(typing.NamedTuple):
    arg: str  # message text
    rep: str  # message text with reply attached
    media: typing.Any  # media if exist
    reply_media: typing.Any # reply media if exist
    time: datetime.datetime  # UTC time when sent
    local_time: datetime.datetime  # UTC time when recv
    sender: utils.user.User  # sender
    reply_sender: utils.user.User  # reply sender if applicable
    # chat: Chat  # chat object --- unneeded for now
    int_cur: utils.interactor.MessageInteractor  # for current message
    int_prev: utils.interactor.MessageInteractor  # for attached reply


async def from_message(msg_cur: telethon.tl.custom.message.Message) -> CommandMessage:
    msg_prev = await msg_cur.get_reply_message()
    has_reply = msg_prev is not None
    chat_obj = await msg_cur.get_chat()

    # TODO handle markdownv2 properly
    def unmd2(s: str) -> str:
        return s.replace('\\\\', '').replace('\\_', '_').replace('\\(', '(').replace('\\)', ')').replace('\\|', '|')

    arg = unmd2(msg_cur.text)
    rep = unmd2(msg_prev.text) if has_reply and msg_prev.mesage else None

    # if no media is given then Media(None)
    media = utils.media.Media(msg_cur) if msg_cur.media else utils.media.Media(msg_prev)
    reply_media = utils.media.Media(msg_prev)

    time = msg_cur.date

    sender = utils.user.from_telethon(await msg_cur.get_sender(), chat_obj)
    reply_sender = utils.user.from_telethon(await msg_prev.get_sender(), chat_obj) if has_reply else None

    # self.chat = Chat(??)
    int_cur = utils.interactor.MessageInteractor(msg_cur)
    int_prev = utils.interactor.MessageInteractor(msg_prev) if has_reply else None

    local_time = datetime.datetime.now(datetime.timezone.utc)

    return CommandMessage(arg, rep, media, reply_media, time, local_time, sender, reply_sender, int_cur, int_prev)


async def from_event(event: telethon.events.NewMessage) -> CommandMessage:
    return from_message(event.message)
