import utils.user
import utils.interactor
import utils.media

import typing
import datetime
import telethon.tl.custom
import telethon.tl.types
import telethon.client


class CommandMessage(typing.NamedTuple):
    arg: str  # message text
    rep: str  # message text with reply attached
    media: utils.media.Media  # media if exist
    reply_media: utils.media.Media # reply media if exist
    time: datetime.datetime  # UTC time when sent
    local_time: datetime.datetime  # UTC time when recv
    sender: utils.user.User  # sender
    reply_sender: utils.user.User  # reply sender if applicable
    int_cur: utils.interactor.MessageInteractor  # for current message
    int_prev: utils.interactor.MessageInteractor  # for attached reply
    client: telethon.client.telegramclient.TelegramClient
    id: int
    reply_id: int  # -1 if no reply
    msg: telethon.tl.custom.message.Message
    lang: str


async def from_message(msg_cur: telethon.tl.custom.message.Message) -> CommandMessage:
    msg_prev = await msg_cur.get_reply_message()
    has_reply = msg_prev is not None
    chat_obj = await msg_cur.get_chat()

    client = msg_cur.client
    id = msg_cur.id
    reply_id = msg_prev.id if msg_prev else -1

    # TODO handle markdownv2 properly
    def unmd2(s: str, es) -> str:
        if not s: return ""
        s = s.replace('\\_', '_').replace('\\(', '(').replace('\\)', ')').replace('\\|', '|')
        mentions = []
        for e in es or []:
            if type(e) == telethon.tl.types.MessageEntityMentionName:
                i, l, uid = e.offset, e.length, e.user_id
                mentions.append((-i, i, l, uid))
        for k, i, l, uid in sorted(mentions):
            s = s[:i] + '{' + str(uid) + '|' + str(l) + '}' + s[i:]
        return s

    # .text? .message?
    arg = unmd2(msg_cur.message, msg_cur.entities)
    rep = unmd2(msg_prev.message, msg_prev.entities) if has_reply and msg_prev.message else None

    # if no media is given then Media(None)
    media = utils.media.Media(msg_cur)
    reply_media = utils.media.Media(msg_prev)

    time = msg_cur.date

    sender = await utils.user.from_telethon(await msg_cur.get_sender(), chat_obj, client)
    reply_sender = await utils.user.from_telethon(await msg_prev.get_sender(), chat_obj, client) if has_reply else None

    lang = sender.get_lang()

    # self.chat = Chat(??)
    int_cur = utils.interactor.MessageInteractor(msg_cur)
    int_prev = utils.interactor.MessageInteractor(msg_prev) if has_reply else None

    local_time = datetime.datetime.now(datetime.timezone.utc)

    return CommandMessage(arg, rep, media, reply_media, time, local_time, sender, reply_sender, int_cur, int_prev, client, id, reply_id, msg_cur, lang)


async def from_event(event: telethon.events.NewMessage) -> CommandMessage:
    return await from_message(event.message)
