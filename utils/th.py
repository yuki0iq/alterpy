import telethon.tl.custom.message
import utils.log
import typing


class TelethonHandler(typing.NamedTuple):
    name: str  # command name
    handler_impl: typing.Callable[[telethon.tl.custom.message.Message], typing.Awaitable]

    async def invoke(self, msg: telethon.tl.custom.message.Message):
        try:
            await self.handler_impl(msg)
        except:
            utils.log.get("telethon handler").exception("invoke exception")
