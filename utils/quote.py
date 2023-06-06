import typing

import PIL.Image
import telethon.tl.custom.message
import telethon.tl.types
import telethon.client
import utils.user
import utils.str
import utils.textwrap
import utils.media
import typing


class Message(typing.NamedTuple):
    name: str
    avatar: typing.Optional[PIL.Image.Image]  # TODO use
    id: int
    reply_id: typing.Optional[int]
    media: utils.media.Media  # TODO use
    message: typing.Optional[str]


def message_to_string(message: Message, max_name: int, max_id: int) -> str:
    # <max_name> | <max_id> | text
    # rjust name | rjust#id | text
    name = utils.str.rjust(message.name, max_name)
    m_id = f"#{message.id}".rjust(max_id)
    initial_indent = f"{name} | {m_id} | "
    subsequent_indent = " "*max_name + " | " + " "*max_id + " | "

    text = message.message or ''
    r_id = message.reply_id
    mty = message.media.type()
    single_line = text.count('\n') == 0 and not mty
    combined = []

    if r_id:
        combined.append(f"[>>{r_id}]")
    if mty:
        combined.append(f"[media:{mty}]")
    if text:
        combined.append(text)

    return utils.textwrap.text((' ' if single_line else '\n').join(combined), 120, initial_indent=initial_indent, subsequent_indent=subsequent_indent)


def merge(messages: list[Message]) -> str:
    max_name = len(max(messages, key=(lambda x: len(x.name))).name)
    max_id = 1 + len(str(max(messages, key=(lambda x: len(str(x.id)))).id))
    return '\n'.join(message_to_string(message, max_name, max_id) for message in messages)


async def create(messages: list[telethon.tl.custom.message.Message], chat_id: int, client: telethon.client.telegramclient.TelegramClient) -> str:
    res = []
    for msg in messages:
        # TODO handle reply headers
        user = (await utils.user.from_telethon(msg.sender, chat_id, client))
        media = utils.media.Media(msg)
        r_id = None
        msg_prev = await msg.get_reply_message()
        if msg_prev:
            r_id = msg_prev.id
        avatar = None
        if msg.fwd_from:
            from_id = msg.fwd_from.from_id
            if from_id:
                fid = 0
                if type(from_id) == telethon.tl.types.PeerUser: fid = from_id.user_id
                if type(from_id) == telethon.tl.types.PeerChat: fid = from_id.chat_id
                if type(from_id) == telethon.tl.types.PeerChannel: fid = from_id.channel_id
                sender = await utils.user.from_telethon(fid, chat_id, client)
                name = await sender.get_display_name()
                avatar = await sender.userpic()
            else:
                name = msg.fwd_from.from_name
            pa = msg.fwd_from.post_author
            if pa:
                name = f"{name} ({pa})"
        else:
            name = await user.get_display_name()
            avatar = await user.userpic()
        res.append(Message(name + (" AV" if avatar else ""), avatar, msg.id, r_id, media, msg.message))
    return merge(res)

