import utils.log

import typing
import telethon.tl.custom
import traceback


class MessageInteractor(typing.NamedTuple):
    message: telethon.tl.custom.message.Message

    async def reply(self, text, file=None):
        """Reply to message"""
        try:
            return MessageInteractor(await self.message.reply(text, file=file))
        except:
            try:
                await self.message.reply(f"```{traceback.format_exc()}```")
            except:
                pass
            utils.log.fail(utils.log.get("telethon"), "Could not reply")

    async def respond(self, text, file=None):
        """Respond to message (without replying)"""
        try:
            return MessageInteractor(await self.message.respond(text, file=file))
        except:
            try:
                await self.message.reply(f"```{traceback.format_exc()}```")
            except:
                pass
            utils.log.fail(utils.log.get("telethon"), "Could not respond")

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
            try:
                await self.message.reply(f"```{traceback.format_exc()}```")
            except:
                pass
            utils.log.fail(utils.log.get("telethon"), "Could not send file")

    async def delete(self):
        """Delete the message"""
        await self.message.delete()