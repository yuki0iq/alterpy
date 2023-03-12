import telethon.tl.custom.message
import utils.user
import zoneinfo


tzMSK = zoneinfo.ZoneInfo("Europe/Moscow")
time_format = "(%Z) %Y-%m-%d, %H:%M:%S"


async def create(messages: list[telethon.tl.custom.message.Message], chat_id: int) -> str:
    res = []
    for msg in messages:
        user = utils.user.User(msg.sender, chat_id)
        res.append(f"#{msg.id} {await user.get_display_name()} {['написал(а)', 'написал', 'написала'][user.get_pronouns()]} в {msg.date.astimezone(tzMSK).strftime(time_format)}\n{msg.text}")
    return '\n\n'.join(res)