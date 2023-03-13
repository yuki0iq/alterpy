import typing

import PIL.Image
import telethon.tl.custom.message
import telethon.client
import utils.user
import utils.str
import utils.textwrap


class Message(typing.NamedTuple):
    name: str
    avatar: PIL.Image.Image | None  # TODO
    id: int
    reply_id: int | None
    media: None  # TODO
    message: str | None


def message_to_string(message: Message, max_name: int, max_id: int) -> str:
    # <max_name> | <max_id> | text
    # rjust name | rjust#id | text
    name = utils.str.rjust(message.name, max_name)
    m_id = f"#{message.id}".rjust(max_id)
    initial_indent = f"{name} | {m_id} | "
    subsequent_indent = " "*max_name + " | " + " "*max_id + " | "
    text = message.message
    r_id = message.reply_id
    if r_id:
        if text.count('\n') == 0:
            text = f"[>>{r_id}] {text}"
        else:
            text = f"[>>{r_id}]\n{text}"
    return utils.textwrap.text(text, 120, initial_indent=initial_indent, subsequent_indent=subsequent_indent)


def merge(messages: list[Message]) -> str:
    max_name = len(max(messages, key=(lambda x: len(x.name))).name)
    max_id = 1 + len(str(max(messages, key=(lambda x: len(str(x.id)))).id))
    return '\n'.join(message_to_string(message, max_name, max_id) for message in messages)


async def create(messages: list[telethon.tl.custom.message.Message], chat_id: int, client: telethon.client.TelegramClient) -> str:
    res = []
    for msg in messages:
        user = utils.user.User(msg.sender, chat_id, client)
        r_id = None
        msg_prev = await msg.get_reply_message()
        if msg_prev:
            r_id = msg_prev.id
        res.append(Message(await user.get_display_name(), None, msg.id, r_id, None, msg.message))
    return merge(res)

