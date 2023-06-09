import aiohttp
import typing
import utils.th

the_bot_id = 0
admins: set[int] = set()
session: typing.Optional[aiohttp.ClientSession] = None
message_handlers: list[utils.th.TelethonHandler] = []

