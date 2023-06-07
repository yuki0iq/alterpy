import utils.log

import typing
import telethon.tl.custom
import traceback


class MessageInteractor(typing.NamedTuple):
    message: telethon.tl.custom.message.Message

    async def reply(self, text: str, file: typing.Any = None, link_preview: bool = True) -> typing.Optional[MessageInteractor]:
        """Reply to message"""
        try:
            return MessageInteractor(await self.message.reply(text, file=file, link_preview=link_preview))
        except:
            try:
                await self.message.reply(f"```{traceback.format_exc()}```")
            except:
                pass
            utils.log.get("telethon").exception("Could not reply")
        return None

    async def respond(self, text: str, file: typing.Any = None, link_preview: bool = True) -> typing.Optional[MessageInteractor]:
        """Respond to message (without replying)"""
        try:
            return MessageInteractor(await self.message.respond(text, file=file, link_preview=link_preview))
        except:
            try:
                await self.message.reply(f"```{traceback.format_exc()}```")
            except:
                pass
            utils.log.get("telethon").exception("Could not respond")
        return None

    async def send_file(self, file: typing.Any, as_reply: bool = False, **kwargs: typing.Any) -> typing.Optional[MessageInteractor]:
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
            utils.log.get("telethon").exception("Could not send file")
        return None

    async def delete(self) -> None:
        """Delete the message"""
        await self.message.delete()
