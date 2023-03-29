import utils.th
import telethon.tl.custom.message
import telethon.client
import context


async def on_autoban(msg: telethon.tl.custom.message.Message):
    client: telethon.client.TelegramClient = msg.client
    chat, sender = msg.chat_id, msg.sender_id
    if sender in context.banned:
        # try banning if permissions are
        try:
            await client.edit_permissions(chat, sender, view_messages=False)
        except:
            pass


handler_list = [utils.th.TelethonHandler("autoban", on_autoban)]
